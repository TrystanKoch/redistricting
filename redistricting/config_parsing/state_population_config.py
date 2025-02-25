"""Utilities for parsing state population configuration."""

import os
import urllib.parse

from typing import Optional

from .config import Config, ConfigParseError, ensure_config


def state_population_directory(config: Optional[Config] = None) -> str:
    """Return directory for the census state population file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the state populations

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
            config["saved_data"]["downloads"]["directory"],
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(directory, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state population directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def state_population_filename(config: Optional[Config] = None) -> str:
    """Return the directory for the census state population file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the state populations

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        filename_template = \
            config["census_urls"]\
                  ["apportionment_population"]\
                  ["states_filename_template"]
        filename = filename_template.format(
            census_year = config["census_urls"]["census_year"]
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state population filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename


def state_population_url(config: Optional[Config] = None) -> str:
    """Return the census url for the census state population file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured URL for the Census' state population file

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        url_directory_template = config["census_urls"] \
                                       ["apportionment_population"] \
                                       ["directory_template"]
        url_directory = url_directory_template.format(
            census_year = config["census_urls"]["census_year"]
        )
        filename = state_population_filename()
        url = urllib.parse.urljoin(url_directory,filename)

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(url, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state population url") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return url


def state_population_location(config: Optional[Config] = None) -> str:
    """Return full relative filename for the census state population file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured relative pathname for the state populations.

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # The location of the file is a join of two other configured strings.
    # Any errors will be raised within these functions.
    location = os.path.join(
        state_population_directory(config),
        state_population_filename(config)
    )
    return location
