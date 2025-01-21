"""Modules for loading a state's data from saved files."""

import geopandas as gpd

from . import config_parsing
from . import data_acquisition


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
