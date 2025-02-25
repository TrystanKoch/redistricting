"""Functions to parse complicated config options used in multiple places."""

import os
import tomllib
import urllib.parse

from typing import Any


CONFIG = "config.toml"

class ConfigParseError(Exception):
    """Error class to suggest that the config file is misformed."""

    def __init__(self, config_key: str) -> None:
        super().__init__(
            f"Could not retrieve {config_key} from configuration file."
        )


def ensure_config(config: dict[Any, Any] | None = None) -> dict[str, Any]:
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
            config = tomllib.load(config_file)

    # Either pass the orignial config dictionary through, or return the newly
    # parsed configurarion dictionary.
    return config


def downloads_directory(config: dict[str, Any] | None = None) -> str:
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


def state_shapes_directory(config: dict[str, Any] | None = None) -> str:
    """Return the directory for the census state shape file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the state shapes

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
            config["saved_data"]["downloads"]["directory"]
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(directory, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state shapes directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def state_shapes_filename(config: dict[str, Any] | None = None) -> str:
    """Return the filename the census state shape file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the state shapes

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
        filename_template = \
            config["census_urls"]["state_shapes"]["filename_template"]
        filename = filename_template.format(
            directory_year = \
                config["census_urls"]["state_shapes"]["directory_year"],
            shape_resolution = \
                config["census_urls"]["state_shapes"]["shape_resolution"],
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state shapes filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename


def state_shapes_url(config: dict[Any, Any] | None = None) -> str:
    """Return the census URL for the census state shape file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured URL for the Census' state shapes file

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
        url_directory_template = \
            config["census_urls"]["state_shapes"]["directory_template"]
        url_directory = url_directory_template.format(
            directory_year = \
                config["census_urls"]["state_shapes"]["directory_year"]
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(url_directory, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state shapes url") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return url_directory


def state_shapes_location(config: dict[str, Any] | None = None) -> str:
    """Return full relative filename for the census state population file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured relative pathname for the state shapes

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # The location of the file is a join of two other configured strings.
    # Any errors will be raised within these functions.
    location = os.path.join(
        state_shapes_directory(config),
        state_shapes_filename(config)
    )
    return location


def state_population_directory(config: dict[str, Any] | None = None) -> str:
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


def state_population_filename(config: dict[Any, Any]| None = None) -> str:
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


def state_population_url(config: dict[Any, Any]| None = None) -> str:
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


def state_population_location(config: dict[Any, Any]| None = None) -> str:
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


def fips_identifiers_directory(config: dict[str, Any]| None = None) -> str:
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


def fips_identifiers_filename(config: dict[str, Any]| None = None) -> str:
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


def fips_identifiers_url(config: dict[Any, Any]| None = None) -> str:
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


def fips_identifiers_location(config: dict[str, Any] | None = None) -> str:
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


def census_blocks_directory(config: dict[str, Any] | None = None) -> str:
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
        config: dict[str, Any] | None = None
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
        config: dict[str, Any] | None = None
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
        config: dict[str, Any] | None = None
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


def state_data_directory(config: dict[str, Any]| None = None) -> str:
    """Return directory for processed state population lookup table.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured directory for the state population lookup table

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
        raise ConfigParseError("state data directory") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return directory


def state_data_filename(config: dict[str, Any]| None = None) -> str:
    """Return filename for processed state population lookup table.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary

    Returns
    -------
    str
        Configured filename for the state population lookup table

    """
    # Ensure there is a configuration dictionary.
    config = ensure_config(config)

    # Try to create a string from the expected configuration options.
    # If not, return an error saying which configuration option failed.
    try:
        # A KeyError may occur here if the string keys do not match the file
        # specified in the CONFIG constant above.
        filename = os.path.join(
            config["saved_data"]["cleaned_tables"]["state_data"]["filename"],
        )

        # os.path.join does not guarantee it returns a string. Assert that it
        # has done so.
        assert isinstance(filename, str)

    # If either of the two operations above failed, then there was an issue
    # parsing the configuration dictionary. The user should check that it
    # is correctly written
    except (KeyError, AssertionError) as exc:
        raise ConfigParseError("state data filename") from exc

    # If these actions have succeeded, then we have string configured from
    # our project.
    return filename

def state_data_location(config: dict[str, Any]| None = None) -> str:
    """Return relative filename for processed state population lookup table.

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
        state_data_directory(config),
        state_data_filename(config)
    )
    return location


def country_data_directory(config: dict[str, Any]| None = None) -> str:
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


def country_data_filename(config: dict[str, Any]| None = None) -> str:
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


def country_data_location(config: dict[str, Any]| None = None) -> str:
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
