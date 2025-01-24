"""For splitting regions into districts recursively."""

import shapely

from . import flat_geometry
from . import spherical_geometry


def horizontal_splitter(region_block_centroids, max_small_district_population):
    """Splits a region in two, by population, horizontally.

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


def split_district(cb_blocks, region_mask, num_districts, district_count):
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
    small_district_mask = angle_splitter(
        cb_blocks.mask(~region_mask),
        small_district_population,
        step=3
    )

    # Recurse using the smaller district.
    district_count = split_district(
        cb_blocks,
        small_district_mask,
        small_district_divisions,
        district_count
    )

    # Recurse using the larger district.
    district_count = split_district(
        cb_blocks,
        region_mask & ~small_district_mask,
        large_district_divisions,
        district_count
    )

    return district_count


def split_state(block_centroids, num_districts):
    """Splits census blocks into districts of almost equal population.

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
    split_district(block_centroids, region_mask, num_districts, district_count)


def get_splitline_length(shape, p, theta, crs):
    """Returns the great_circle length of a splitline.

    Parameters
    ----------
    shape : shapely.Geometry
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


def angle_splitter(region_block_centroids, max_small_district_population, step):
    r"""Splits a region in two, by population, with a line at a given angle.

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


def find_splitline_point(block_centroids, small_mask, step):
    """Determine a point on which to base a splitline,

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
