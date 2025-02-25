"""Ultilities to support reading the configuration file."""

import tomllib
from typing import Optional, TypedDict, cast

CONFIG = "config.toml"


class CleanedTablesConfig(TypedDict):
    """A dictionary to represent the cleaned tables configuration settings."""

    directory: str
    state_data: dict[str,str]
    country_data: dict[str, str]

class SavedDataConfig(TypedDict):
    """A dictionary to represent the saved_data configuration settings."""

    directory: str
    downloads: dict[str, str]
    census_blocks: dict[str,str]
    state_census_blocks: dict[str, str]
    cleaned_tables: CleanedTablesConfig


class CensusUrlConfig(TypedDict):
    """A dictionary to represent Configuration for census data."""

    census_year: str
    census_year_short: str
    census_blocks: dict[str, str]
    state_shapes: dict[str, str]
    FIPS_identifiers: dict[str, str]
    apportionment_population: dict[str, str]

class Config(TypedDict):
    """A dictionary to represent loaded data."""

    saved_data: SavedDataConfig
    census_urls: CensusUrlConfig


class ConfigParseError(Exception):
    """Error class to suggest that the config file is misformed."""

    def __init__(self, config_key: str) -> None:
        super().__init__(
            f"Could not retrieve {config_key} from configuration file."
        )


def ensure_config(config: Optional[Config] = None) -> Config:
    """Ensure a config file is defined.

    Check if config dictionary already defined. If so, return that dictionary.
    Otherwise, open config file, read it, and return the new dictionary.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    config: dict
        Configuration dictionary

    """
    # If there is no configuration dictionary already defined, open the
    # config file for the project and parse it.
    if not config:
        with open(CONFIG, "rb") as config_file:
            # This cast a possible point of failure. However, it should pass
            # silently at runtime as it is purely for type checking. Any
            # parsing errors will be handled later on in the individual
            # parsing functions.
            config = cast(Config, tomllib.load(config_file))

    # Either pass the orignial config dictionary through, or return the newly
    # parsed configurarion dictionary.
    return config
