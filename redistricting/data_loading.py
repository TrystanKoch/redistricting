"""Modules for loading a state's data from saved files."""
import os

import pandas as pd
import geopandas as gpd

from . import config_parsing
from . import data_acquisition
from . import data_processing


def load_state_census_blocks(fips):
    """
    Load the census blocks for a state. Does not make sure the file is there

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's census blocks.
    :rtype: geopandas.DataFrame
    """
    data_acquisition.ensure_state_census_blocks(fips)
    return load_state_census_blocks_unchecked(fips)


def load_state_census_blocks_unchecked(fips):
    """
    Load the census blocks for a state. Does not check for file.

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's census blocks.
    :rtype: geopandas.DataFrame
    """
    return gpd.read_file(config_parsing.census_blocks_location(fips))


def load_state_shape(fips):
    """
    Load a state shape from the state shapes file.

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's shape.
    :rtype: geopandas.DataFrame
    """
    data_acquisition.ensure_state_shapes()
    return load_state_shape_unchecked(fips)


def load_state_shape_unchecked(fips):
    """
    Load a state shape from the state shapes file. Does not check for file.

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's shape.
    :rtype: geopandas.DataFrame
    """
    state_shapes_raw = gpd.read_file(config_parsing.state_shapes_location())
    return state_shapes_raw[state_shapes_raw["STATEFP"] == str(fips)]


def load_state_data():
    """
    Load state data table.
    """
    state_data_location = config_parsing.state_data_location()
    if not os.path.isfile(state_data_location):
        data_processing.create_state_data()
    return pd.read_csv(state_data_location)


def load_country_data():
    """
    Load the country data table.
    """
    country_data_location = config_parsing.country_data_location()
    if not os.path.isfile(country_data_location):
        data_processing.create_country_data()
    return pd.read_csv(country_data_location)
