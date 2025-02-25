"""Utilities for parsing census_blocks configuration."""

import os
import urllib.parse

from typing import Optional

from .config import Config, ConfigParseError, ensure_config


def census_blocks_directory(config: Optional[Config] = None) -> str:
    """Return the directory for census block files.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the census block files

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        directory = os.path.join(
            config["saved_data"]["directory"],
            config["saved_data"]["state_census_blocks"]["directory"]
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(directory, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("census blocks directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def census_blocks_filename(
        fips_id: int,
        config: Optional[Config] = None
    ) -> str:
    """Return the filename for the census block file of a state.

    Parameters
    ----------
    fips_id : int
        FIPS id of the state whose block is requested
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the census block file

    """
   # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        census_block_config = config["census_urls"]["census_blocks"]
        filename_template = census_block_config["filename_template"]
        filename = filename_template.format(
            directory_year = census_block_config["directory_year"],
            census_year_short = config["census_urls"]["census_year_short"],
            state_fips = f"{fips_id:02}",
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("census blocks filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename


def census_blocks_url(
        fips_id: int,
        config: Optional[Config] = None
    ) -> str:
    """Return the url for the census block file of a state.

    Parameters
    ----------
    fips_id : str or int
        FIPS id of the state whose block is requested
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured URL for the Census' block file

    """
   # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        census_block_config = config["census_urls"]["census_blocks"]
        url_directory_template = census_block_config["directory_template"]
        url_directory = url_directory_template.format(
            directory_year = census_block_config["directory_year"],
            census_year_short = config["census_urls"]["census_year_short"],
        )
        filename = census_blocks_filename(fips_id)
        url = urllib.parse.urljoin(url_directory,filename)

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(url, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("census blocks url") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return url


def census_blocks_location(
        fips_id: int,
        config: Optional[Config] = None
    ) -> str:
    """Return the full relative filename for the census block file of a state.

    Parameters
    ----------
    fips_id : str or int
        FIPS id of the state whose block is requested
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured relative pathname for the census block file

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # The location of the file is a join of two other configured strings.
    # Any errors will be raised within these functions.
    location = os.path.join(
        census_blocks_directory(config),
        census_blocks_filename(fips_id, config)
    )
    return location
