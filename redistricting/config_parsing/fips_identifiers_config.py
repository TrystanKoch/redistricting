"""Utilities for parsing fips information configuration."""

import os
import urllib.parse

from typing import Optional

from .config import Config, ConfigParseError, ensure_config


def fips_identifiers_directory(config: Optional[Config] = None) -> str:
    """Return directory for the census state FIPS identification file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the state FIPS identification file.

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
        raise ConfigParseError("fips file directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def fips_identifiers_filename(config: Optional[Config] = None) -> str:
    """Return filename for the census state FIPS identification file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the state FIPS identification file

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        filename = config["census_urls"]["FIPS_identifiers"]["filename"]

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("fips filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename


def fips_identifiers_url(config: Optional[Config] = None) -> str:
    """Return URL for census state FIPS identification file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured URL for the Census' state FIPS identification file

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        url_directory = config["census_urls"]["FIPS_identifiers"]["directory"]
        filename = fips_identifiers_filename()
        url = urllib.parse.urljoin(url_directory,filename)

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(url, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("fips file url") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return url


def fips_identifiers_location(config: Optional[Config] = None) -> str:
    """Return the relative filename for the state FIPS identification file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured relative pathname for the state FIPS identification file

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # The location of the file is a join of two other configured strings.
    # Any errors will be raised within these functions.
    location = os.path.join(
        fips_identifiers_directory(config),
        fips_identifiers_filename(config)
    )
    return location
