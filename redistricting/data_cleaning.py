"""For the tranformation of raw geographical data into working dataframes."""

import geopandas as gpd
import pandas as pd

import pyproj


def census_block_centroids(
        census_blocks: gpd.GeoDataFrame,
        gnomonic_crs: pyproj.CRS
    ) -> gpd.GeoDataFrame:
    """Turn the Census' very large dataframe into a more usable dataframe.

    Specifically, all of our processing will only require a central internal
    point of each block, so we change the geometry of our census block data
    to only include this information. We keep the GEOID information for
    the blocks so that we can join our districts to the original blocks
    later.

    Parameters
    ----------
    census_blocks : geopandas.geodataframe.GeoDataFrame
        A dataframe of census blocks for a given state
    gnomonic_crs : pyproj.crs.crs.CRS
        A gnomonic CRS centered on that state.
    :type census_blocks: pyproj.crs.crs.CRS

    Returns
    -------
    geopandas.geodataframe.GeoDataFrame
        Census_block centroids with GEOID, population, and gnomonic locations

    """
    census_crs = census_blocks.crs
    census_block_centroid_df =  (
        # The Census already calculates an internal central point
        # for all census blocks. Let's turn this information into
        # our new geometry. Each block is now represented by this
        # point in NAD83.
        census_blocks.assign(
            geometry=gpd.points_from_xy(
                census_blocks["INTPTLON20"],
                census_blocks["INTPTLAT20"],
            )
        )
    )

    census_block_centroid_df = (
        # We only want to keep a few of the columns. GEOID is the
        # key, which will let us join with the original census
        # block data later.
        census_block_centroid_df
        [["GEOID20", "POP20", "geometry"]]

        # Our ultimate goal! We want to group these blocks into
        # districts, so we need a column to put them in. 0 will
        # mean that we have not yet assigned the block to a
        # district.
        .assign(district=0)
    )

    # Bug in GeoPandas Mypy support requires us to assert that the
    # type has not changed to DataFrame
    assert isinstance(census_block_centroid_df, gpd.GeoDataFrame)

    census_block_centroid_df = (
        census_block_centroid_df

        # The splitline processing will be done in the gnomonic
        # crs, so we will store this information for later. It's
        # easiest to convert our whole dataframe to our new CRS
        # then store the results for later.
        .to_crs(gnomonic_crs)
        .assign(x=lambda gdf_: gdf_.geometry.x)
        .assign(y=lambda gdf_: gdf_.geometry.y)
    )

    # Bug in GeoPandas Mypy support requires us to assert that the
    # type has not changed to DataFrame
    assert isinstance(census_block_centroid_df, gpd.GeoDataFrame)

    census_block_centroid_df = (
        census_block_centroid_df
        # Ultimately, we want to store the centroid geometry in
        # NAD83's latitude and longitude to facilitate further
        # processing. So we need to convert back.
        .to_crs(census_crs)
    )
    return census_block_centroid_df


def state_boundary(state_shape: gpd.GeoDataFrame) -> gpd.GeoSeries:
    """Find the boundary of a given state from its geographical shape.

    Parameters
    ----------
    state_shape : geopandas.geodataframe.GeoDataFrame
        Shape information for a state

    Returns
    -------
    geopandas.geodataframe.GeoSeries
        Boundary information for a state

    """
    return state_shape.geometry.boundary


def apportionment_drop_pr(states: pd.DataFrame) -> pd.DataFrame:
    """Drop Puerto Rico from a list of 'state' populations.

    Parameters
    ----------
    states : pandas.core.frame.DataFrame
        Cleaned state populations table

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned state populations table without Puerto Rico

    """
    return (
        states
        [~states["ABBR"].isin(["PR"])]
    )


def apportionment_drop_dc(states: pd.DataFrame) -> pd.DataFrame:
    """Drop DC from a list of 'state' populations.

    Parameters
    ----------
    states : pandas.core.frame.DataFrame
        Cleaned state populations table

    Returns
    -------
    pandas.core.frame.DataFrame
        Cleaned state populations table without DC

    """
    return (
        states
        [~states["ABBR"].isin(["DC"])]
    )
