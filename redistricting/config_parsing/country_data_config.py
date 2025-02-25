"""Utilities for parsing country data configuration."""

import os

from typing import Optional

from .config import Config, ConfigParseError, ensure_config


def country_data_directory(config: Optional[Config] = None) -> str:
    """Return directory for processed US population lookup table.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the US population lookup table

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
            config["saved_data"]["cleaned_tables"]["directory"],
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(directory, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("country data directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def country_data_filename(config: Optional[Config] = None) -> str:
    """Return filename for processed US population lookup table.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the US population lookup table

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        filename = os.path.join(
            config["saved_data"]["cleaned_tables"]["country_data"]["filename"],
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("country data filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename


def country_data_location(config: Optional[Config] = None) -> str:
    """Return relative filename for processed US population lookup table.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured relative pathname for the state population lookup table

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # The location of the file is a join of two other configured strings.
    # Any errors will be raised within these functions.
    location = os.path.join(
        country_data_directory(config),
        country_data_filename(config)
    )
    return location
