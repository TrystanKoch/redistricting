"""For splitting regions into districts recursively."""

from __future__ import annotations

from typing import cast

import shapely.ops
import numpy as np
import geopandas as gpd
import pandas as pd
import pyproj

from . import flat_geometry
from . import spherical_geometry
from .. import data_loading
from .. import data_cleaning

def horizontal_splitter(
        region_block_centroids: pd.DataFrame,
        max_small_district_population: int
    ) -> pd.Series[bool]:
    """Split a region in two, by population, horizontally.

    Splits a region into two, horizontally. The smaller region will have a
    population that is as large as possible while still being less than a
    given population.

    Parameters
    ----------
    region_block_centroids : pandas.core.frame.DataFrame
        A dataframe that corresponds to a region
    max_small_district_population : int
        A population maximum for the smaller of the resulting districts

    Returns
    -------
    pandas.core.frame.DataFrame
        A mask that is true for all blocks part of the smaller region

    """
    # This naive test function only splits the state in horizontal lines.
    # Because of this, the angular step is always 0, corresponding to
    # lines that are horizontal in our gnomonic CRS.
    # Note: this IS a great circle. This IS NOT a line of latitude.
    step = 0

    return (
        # This should be one of our cleaned centroid blocks.
        region_block_centroids

        # Sort by the column that corresponds to distance along a specified
        # direction. The directions are labeled by the angular step we are on.
        .sort_values([str(step)])

        # Find the cumulative sum of the population. This is equivalent to
        # slowly moving our dividing line in the direction normal to the
        # angluar step we chose, then finding how much of our population is
        # behind that line.
        ["POP20"].cumsum()

        # Finally, create a mask which is true only if that cumulative sum is
        # less than our specified maximum population
        < max_small_district_population
    )


def split_district(
        cb_blocks: gpd.GeoDataFrame,
        region_mask: pd.Series[bool],
        num_districts: int,
        district_count: int,
        region_shape: gpd.GeoDataFrame
    ) -> int:
    """Recursively split a region into districts of almost equal population.

    Recursively split a region into districts with populations in proportion
    to an even split of districts.

    Parameters
    ----------
    cb_blocks : geopandas.geodataframe.GeoDataFrame
        A (mutating!) dataframe representing census blocks
    region_mask : pandas.core.frame.DataFrame
        A mask over the census blocks, indicating the current region to split
    num_districts : int
        The total number of districts we want to split the state into
    district_count : int
        The number of districts we have created so far

    Returns
    -------
    int
        District count after running the function.
    """
    # Find the total population of the district
    total_population = cb_blocks.mask(~region_mask)["POP20"].sum()

    # If there's only one district to label, label it using the latest label.
    # Tell the user that we found it. Our recursive base case.
    if num_districts == 1:
        district_count += 1
        cb_blocks.loc[region_mask, "district"] = district_count
        print(
            f"Created district {district_count},",
            f"population {total_population}."
        )
        return district_count

    # At this point, we know that we have to split our current region at least
    # one time. Determine how many divisions will need to be made in each
    # branch after the next split.
    small_district_divisions = num_districts // 2
    large_district_divisions = num_districts - (small_district_divisions)

    # We'll need this to determine the population cutoff for our split. The
    # next two regions should have populations in the same ratio as their
    # numbers of districts.
    small_district_proportion = small_district_divisions / num_districts
    small_district_population = total_population * small_district_proportion

    # Split the district with a splitting function.
    # Note that we assume our function returns a mask for the smaller of the
    # two regions.
    cur_region = cast(gpd.GeoDataFrame, cb_blocks.mask(~region_mask))
    small_district_mask, small_district_shape, big_district_shape = \
        find_min_splitline_step(
            cur_region,
            small_district_population,
            region_shape
        )

    # Recurse using the smaller district.
    district_count = split_district(
        cb_blocks,
        small_district_mask,
        small_district_divisions,
        district_count,
        small_district_shape
    )

    # Recurse using the larger district.
    district_count = split_district(
        cb_blocks,
        region_mask & ~small_district_mask,
        large_district_divisions,
        district_count,
        big_district_shape
    )

    return district_count


def min_length_split_state_with_shape(
        block_centroids: gpd.GeoDataFrame,
        num_districts: int,
        state_shape: gpd.GeoDataFrame
    ) -> None:
    """Split census blocks into districts of almost equal population.

    Recursively splits a region into districts of equal population in place.

    Parameters
    ----------
    block_centroids:geopandas.geoframe.GeoDataFrame
        A (mutating!) set of census blocks
    num_districts: int
        Total number of districts to divide the region into

    """
    district_count = 0
    region_mask = block_centroids["district"].notna()
    _ = split_district(
        block_centroids,
        region_mask,
        num_districts,
        district_count,
        state_shape
    )


def get_splitline_length(
        shape: shapely.Polygon,
        p: shapely.Point,
        theta: float,
        crs: pyproj.CRS
    ) -> float:
    """Return the great_circle length of a splitline.

    Parameters
    ----------
    shape : shapely.Polygon
        The shape corresponding to a region to be split
    p : shapely.geometry.Point
        A point on the splitline
    theta : float
        Angle of a split line at a point
    crs : pyproj.CRS
        Coordinate reference system that the points and shapes are defined in

    Returns
    -------
    float
        The great circle distance of the splitline within the shape

    Notes
    -----
    This takes a shapely Geometry, not a GeoDataFrame, so the geometry must be
    stripped from the GeoDataFrame first before calling this function.

    The distance is returned in the units of the crs that we pass in. For
    this project, this is assumed to be meters, though nothing here will
    rely on that assumption.

    """
    boundary_p1, boundary_p2 = flat_geometry.boundary_intersection_points(
        shape, p, theta
    )
    return spherical_geometry.find_great_circle_distance(
        boundary_p1, boundary_p2, crs
    )


def angle_splitter(
        region_block_centroids: pd.DataFrame,
        max_small_district_population: int,
        step: int
    ) -> pd.Series[bool]:
    r"""Split a region in two, by population, with a line at a given angle.

    Splits a region into two. The smaller region will have a population that is
    as large as possible while still being less than a given population. The
    split will occur along a line with a given angle to the horizontal.

    Parameters
    ----------
    region_block_centroids : pandas.core.frame.DataFrame
        A dataframe that corresponds to a region
    max_small_district_population : int
        A population maximum for the smaller of the resulting districts
    step : int or str
        Corresponds to an anglular step around a revolution

    Returns
    -------
    pandas.core.frame.DataFrame
        A mask that is true for all blocks part of the smaller region

    Notes
    -----
    We are taking a full revolution in some number of total anglular steps. The
    angle in radians from the horizontal can be determined from the formula

    .. math:: \theta_n = 2\pi n/N

    where :math:`n` is the step number and :math:`N` is the total number of
    steps.

    """
    return (
        # This should be one of our cleaned centroid blocks.
        region_block_centroids

        # Sort by the column that corresponds to distance along a specified
        # direction. The directions are labeled by the angular step we are on.
        .sort_values([str(step)])

        # Find the cumulative sum of the population. This is equivalent to
        # slowly moving our dividing line in the direction normal to the
        # angluar step we chose, then finding how much of our population is
        # behind that line.
        ["POP20"].cumsum()

        # Finally, create a mask which is true only if that cumulative sum is
        # less than our specified maximum population
        < max_small_district_population
    )


def find_splitline_point(
        block_centroids: gpd.GeoDataFrame,
        small_mask: pd.Series[bool],
        step: int
    ) -> shapely.Point:
    """Determine a point on which to base a splitline.

    Parameters
    ----------
    block_centroids : geopandas.GeoDataFrame
        A dataframe representing census blocks
    small_mask : pandas.core.frame.DataFrame
        A region mask having a smaller population than its complement
    step : int or str
        The angular direction we are splitting in

    Returns
    -------
    shapely.geometry.Point
        A point on the splitline between the regions.

    """
    last_small_idx = (
        # For all the centroids
        block_centroids

        # Look at only the ones in the smaller region
        .loc[small_mask]

        # Look at their directed distance from the origin
        # in a particular angular direction
        [str(step)]

        # Find the one with the mazimum directed distance
        .idxmax(axis=0)
    )

    first_big_idx = (
        # Now for all the centroids
        block_centroids

        # Look at the ones in the larger region
        .loc[~small_mask]

        # Still looking at the directed distance in a
        # particular angular direction.
        [str(step)]

        # We want to find the first element that was not
        # in the smaller region
        .idxmin(axis=0)
    )

    if isinstance(last_small_idx, str) or isinstance(first_big_idx, str):
        raise ValueError

    # Find the GeoSeries that correspond to these points
    p1_df = block_centroids.iloc[last_small_idx]
    p2_df = block_centroids.iloc[first_big_idx]

    # Return a point that is halfway between them
    # Note that this will always be a point between our two
    # regions determined by the region mask.
    return shapely.Point(
        (p1_df.x + p2_df.x) / 2,
        (p1_df.y + p2_df.y) / 2
    )


def get_split_shapes(
        shape: shapely.Polygon,
        p: shapely.Point,
        theta: float
    ) -> tuple[shapely.Polygon, shapely.Polygon]:
    """Split a geometric shape by a line.

    Parameters
    ----------
    shape : shapely.Polygon
        Polygon for the region
    p : shapely.Point
        Point on the splitline
    theta : float
        Angle in radians between splitline and horizonal

    Returns
    -------
    subshape_! : shapely.Polygon
        First Subregion
    subshape_2 : shapely.Polygon
        Second Subregion

    """
    splitline = flat_geometry.point_angle_line(p, theta)
    subshapes = shapely.ops.split(shape, splitline)

    subshape_1 = subshapes.geoms[0]
    subshape_2 = subshapes.geoms[1]

    if not (
        isinstance(subshape_1, shapely.Polygon)
        and isinstance(subshape_2, shapely.Polygon)
    ):
        raise TypeError

    return subshape_1, subshape_2


def split_region_shape(
        region: gpd.GeoDataFrame,
        p: shapely.Point,
        theta: float
    ) -> tuple[float, gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Split a region's dataframe into two by a splitline.

    Parameters
    ----------
    shape : gpd.GeoDataFrame
        Dataframe containg the polygon for the region
    p : shapely.Point
        Point on the splitline
    theta : float
        Angle in radians between splitline and horizonal

    Returns
    -------
    split_length : float

    region_1 : geopandas.DataFrame
        The first subregion of the input region
    region_2 : geopandas.DataFrame
        The second subregion of the input region
    """
    shape = region.geometry.iloc[0]
    crs = region.crs

    if not isinstance(shape, shapely.Polygon):
        raise TypeError

    if crs is None:
        raise ValueError

    subshape_1, subshape_2 = get_split_shapes(shape, p, theta)
    split_length = get_splitline_length(shape, p, theta, crs)

    region_1 = spherical_geometry.geom_with_crs(subshape_1, crs)
    region_2 = spherical_geometry.geom_with_crs(subshape_2, crs)

    return split_length, region_1, region_2


def find_min_splitline_step(
        region_block_centroids: gpd.GeoDataFrame,
        max_small_district_population: int,
        state_shape: gpd.GeoDataFrame
    ) -> tuple[pd.Series[bool], gpd.GeoDataFrame, gpd.GeoDataFrame]:
    """Recursive step for splitting the regions by the shortest splitline.

    Parameters
    ----------
    region_block_centroids : gpd.GeoDataFrame
        A dataframe containing the census data and directed distances.
    max_small_district_population : int
        A population cutoff for the smaller sub-region.
    state_shape : gpd.GeoDataFrame
        A dataframe containing our region's polygon

    Returns
    -------
    min_mask : pd.DataFrame
        A mask for a region containing the max_small_district_population
    min_subregion1 : gpd.GeoDataFrame
        The subregion of our state_shape that corresponds to the mask
    min_subregion2 : gpd.GeoDataFrame
        The complement of min_subregion1

    """
    # Initialize the values for the loop. We always need to consider the first
    # length we find, so we compare it to infinity.
    min_mask = None
    min_subregion1 = None
    min_subregion2 = None
    min_length = np.inf

    # The total number of steps is something we should pass down in the future,
    # but for now, we can read this information directly from the last column
    # of the region block centroid data frame.
    total_steps = int(region_block_centroids.columns[-1]) + 1

    # Iterate over all angular steps around a full revolution.
    for step in range(total_steps):
        # For each angular step, we want to break up the current region into
        # two regions. This splitline will be in the direction of that angular
        # step, and will go through the last point int he small region.
        small_mask = angle_splitter(
            region_block_centroids,
            max_small_district_population,
            step
        )
        # We will need that point
        p = find_splitline_point(region_block_centroids, small_mask, step)

        # We have been talking in terms of angular steps, but our shape
        # splitting algorithm uses angles in radians.
        theta = step/total_steps*np.pi*2

        # possible todo: Remove the try-except-else statement.
        # This is currently here because the algorithm does not check whether
        # our small mask corresponds to the small region shape. That is a
        # serious bug! Note: bug fixed, but try kept for now.
        try:
            # Split the region shape by the splitline through the point p at
            # the angle theta. The length of that line is given here.
            length, subregion1, subregion2 = split_region_shape(
                state_shape,
                p,
                theta
            )
        except IndexError:
            print("Oops: a region got passed wrong.")
        else:
            # Finally, store the information if we have found the shortest
            # splitline so far.
            if length < min_length:
                min_mask = small_mask
                min_length = length
                min_subregion1 = subregion1
                min_subregion2 = subregion2

    if min_mask is None:
        raise ValueError
    if min_subregion1 is None or min_subregion2 is None:
        raise ValueError

    # To ensure that the first returned shape is the region with the smaller
    # population choose a point in the smaller region from the masked centroids
    # dataframe.
    small_test_point = shapely.Point(
        region_block_centroids.loc[min_mask].iloc[10].x,
        region_block_centroids.loc[min_mask].iloc[10].y
    )

    # This if-else block ensures that the min mask corresponds to the
    # min_subregion1 dataframe.
    if shapely.within(small_test_point, min_subregion1.geometry.iloc[0]):
        return min_mask, min_subregion1, min_subregion2
    elif shapely.within(small_test_point, min_subregion2.geometry.iloc[0]):
        return min_mask, min_subregion2, min_subregion1
    else:
        #print("  Warning: check point isn't in either subregion. Defualting.")
        return min_mask, min_subregion1, min_subregion2


def min_length_split_state(
        fips_id: int,
        dist_count: int,
        steps: int = 60
    ) -> gpd.GeoDataFrame:
    """Split a state's census blocks using minimum distance splitlines.

    Parameters
    ----------
    fips_id : int
        The FIPS identification number for the state
    dist_count : int
        The number of districts to split the state into
    steps : int
        The number of angular steps to take while finding minimum splitlines

    Returns
    -------
    geopandas.GeoDataFrame
        The original census block table with district labels added

    """
    # Get the correct state polygon, use it to create a gnomonic crs, then
    # change the shape into the new crs.
    state_shape = data_loading.load_state_shape(fips_id)
    state_centered_gnomonic_crs = spherical_geometry.centered_gnomonic_crs(
        state_shape
    )
    g_state_shape = state_shape.to_crs(state_centered_gnomonic_crs)

    # Load the census blocks, ensure they are in the gnomonic crs, then
    # create directed distances for each angular step around a revolution.
    census_blocks_raw = data_loading.load_state_census_blocks(fips_id)
    block_centroids = data_cleaning.census_block_centroids(
        census_blocks_raw,
        state_centered_gnomonic_crs
    )
    block_centroid_dots = flat_geometry.position_dot_products(
        block_centroids,
        steps
    )

    if not isinstance(block_centroid_dots, gpd.GeoDataFrame):
        raise TypeError

    # Do all the work! Recursively split the state with minumum length
    # splitlines with approximately equal populations.
    # Note: block_centroid_dots is mutating here.
    min_length_split_state_with_shape(
        block_centroid_dots,
        dist_count,
        g_state_shape
    )

    # We want to get rid of all unneccessary processing information anda pply
    # our new districts directly to the original census information.
    districted_census_blocks = census_blocks_raw.merge(
        block_centroid_dots[["GEOID20", "district"]],
        on="GEOID20",
        how="right"
    )

    if not isinstance(districted_census_blocks, gpd.GeoDataFrame):
        raise TypeError

    return districted_census_blocks
