"""Modules for loading a state's data from saved files."""
import os

import pandas as pd
import geopandas as gpd

from . import config_parsing
from . import data_acquisition
from . import data_processing


def load_state_census_blocks(fips: int) -> gpd.GeoDataFrame:
    """Load the census blocks for a state.

    Parameters
    ----------
    fips : int
        The FIPS identifier for the state

    Returns
    -------
    geopandas.DataFrame
        A state's census blocks

    """
    data_acquisition.ensure_state_census_blocks(fips)
    return gpd.read_file(config_parsing.census_blocks_location(fips))


def load_state_shape(fips: int) -> gpd.GeoDataFrame:
    """Load a state shape from the state shapes file.

    Parameters
    ----------
    fips : int
        The FIPS identifier for the state

    Returns
    -------
    geopandas.DataFrame
        A state's shape information

    """
    data_acquisition.ensure_state_shapes()
    state_shapes_raw = gpd.read_file(config_parsing.state_shapes_location())
    state_shape = state_shapes_raw[state_shapes_raw["STATEFP"] == str(fips)]
    assert isinstance(state_shape, gpd.GeoDataFrame)
    return state_shape


def load_state_data() -> pd.DataFrame:
    """Load the state data table.

    Returns
    -------
    pandas.core.frame.DataFrame
        The data table for US states and territories

    """
    state_data_location = config_parsing.state_data_location()
    if not os.path.isfile(state_data_location):
        data_processing.create_state_data()
    return pd.read_csv(state_data_location)


def load_country_data() -> pd.DataFrame:
    """Load the country data table.

    Returns
    -------
    pandas.core.frame.DataFrame
        The data table for the US population

    """
    country_data_location = config_parsing.country_data_location()
    if not os.path.isfile(country_data_location):
        data_processing.create_country_data()
    return pd.read_csv(country_data_location)
