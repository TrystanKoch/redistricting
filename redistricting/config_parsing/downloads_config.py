"""Utilities for parsing download configuration."""

import os

from typing import Optional

from .config import Config, ConfigParseError, ensure_config

def downloads_directory(config: Optional[Config] = None) -> str:
    """Return configured downloads directory for project.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for project downloads

    Raises
    ------
    ConfigParseError
        There is a mismatch between the keys expected and the config file

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
        raise ConfigParseError("downloads directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory
