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


def load_state_boundary(fips):
    """
    Load a state boundary from the state boundaries file.

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's boundary.
    :rtype: geopandas.DataFrame
    """
    data_acquisition.ensure_state_boundaries()
    return load_state_boundary_unchecked(fips)


def load_state_boundary_unchecked(fips):
    """
    Load a state boundary from the state boundaries file. Does not check for file.

    :param fips: The FIPS identifier for the state.
    :type fips: int or str
    :return: A state's boundary.
    :rtype: geopandas.DataFrame
    """
    state_boundaries_raw = gpd.read_file(config_parsing.state_boundaries_location())
    return state_boundaries_raw[state_boundaries_raw["STATEFP"] == str(fips)]
