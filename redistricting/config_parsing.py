"""Functions to parse complicated config options that are used in multiple places."""

import os
import tomllib
import urllib.parse


CONFIG = "config.toml"


def ensure_config(config=None):
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
    if not config:
        with open(CONFIG, "rb") as config_file:
            config = tomllib.load(config_file)
    return config


def downloads_directory(config=None):
    """Return configured downloads directory for project.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary
    
    Returns
    -------
    str
        Configured directory for project downloads
    
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def state_shapes_directory(config=None):
    """Return the directory for the census state shape file.
    
    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary
    
    Returns
    -------
    str
        Configured directory for the state shapes
    
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"]
    )
    return directory


def state_shapes_filename(config=None):
    """Return the filename the census state shape file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary
    
    Returns
    -------
    str
        Configured filename for the state shapes
    
    """
    config = ensure_config(config)
    filename_template = config["census_urls"]["state_shapes"]["filename_template"]
    filename = filename_template.format(
        directory_year=config["census_urls"]["state_shapes"]["directory_year"],
        shape_resolution=config["census_urls"]["state_shapes"]["shape_resolution"],
    )
    return filename


def state_shapes_url(config=None):
    """Return the census URL for the census state shape file.

    Parameters
    ----------
    config : Optional[dict]
        Optional configuration dictionary
    
    Returns
    -------
    str
        Configured URL for the Census' state shapes file
    
    """
    config = ensure_config(config)
    url_directory_template = config["census_urls"]["state_shapes"]["directory_template"]
    url_directory = url_directory_template.format(
        directory_year = config["census_urls"]["state_shapes"]["directory_year"]
    )
    filename = state_shapes_filename()
    url = urllib.parse.urljoin(url_directory,filename)
    return url


def state_shapes_location(config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        state_shapes_directory(config),
        state_shapes_filename(config)
    )
    return location


def state_population_directory(config=None):
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
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def state_population_filename(config=None):
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
    config = ensure_config(config)
    filename_template = config["census_urls"]["apportionment_population"]\
                                             ["states_filename_template"]
    filename = filename_template.format(
        census_year = config["census_urls"]["census_year"]
    )
    return filename


def state_population_url(config=None):
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
    config = ensure_config(config)
    url_directory_template = config["census_urls"] \
                                   ["apportionment_population"] \
                                   ["directory_template"]
    url_directory = url_directory_template.format(
        census_year = config["census_urls"]["census_year"]
    )
    filename = state_population_filename()
    url = urllib.parse.urljoin(url_directory,filename)
    return url


def state_population_location(config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        state_population_directory(config),
        state_population_filename(config)
    )
    return location


def fips_identifiers_directory(config=None):
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
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def fips_identifiers_filename(config=None):
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
    config = ensure_config(config)
    filename = config["census_urls"]["FIPS_identifiers"]["filename"]
    return filename


def fips_identifiers_url(config=None):
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
    config = ensure_config(config)
    url_directory = config["census_urls"]["FIPS_identifiers"]["directory"]
    filename = fips_identifiers_filename()
    url = urllib.parse.urljoin(url_directory,filename)
    return url


def fips_identifiers_location(config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        fips_identifiers_directory(config),
        fips_identifiers_filename(config)
    )
    return location


def census_blocks_directory(config=None):
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
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["state_census_blocks"]["directory"]
    )
    return directory


def census_blocks_filename(fips_id, config=None):
    """Return the filename for the census block file of a state.
    
    Parameters
    ----------
    fips_id : str or int
        FIPS id of the state whose block is requested
    config : Optional[dict]
        Optional configuration dictionary
    
    Returns
    -------
    str
        Configured filename for the census block file
    
    """
    config = ensure_config(config)
    census_block_config = config["census_urls"]["census_blocks"]
    filename_template = census_block_config["filename_template"]
    filename = filename_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"],
        state_fips = f"{fips_id:02}",
    )
    return filename


def census_blocks_url(fips_id, config=None):
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
    config = ensure_config(config)
    census_block_config = config["census_urls"]["census_blocks"]
    url_directory_template = census_block_config["directory_template"]
    url_directory = url_directory_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"],
    )
    filename = census_blocks_filename(fips_id)
    url = urllib.parse.urljoin(url_directory,filename)
    return url


def census_blocks_location(fips_id, config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        census_blocks_directory(config),
        census_blocks_filename(fips_id, config)
    )
    return location


def state_data_directory(config=None):
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
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["cleaned_tables"]["directory"],
    )
    return directory


def state_data_filename(config=None):
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
    config = ensure_config(config)
    filename = os.path.join(
        config["saved_data"]["cleaned_tables"]["state_data"]["filename"],
    )
    return filename

def state_data_location(config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        state_data_directory(config),
        state_data_filename(config)
    )
    return location


def country_data_directory(config=None):
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
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["cleaned_tables"]["directory"],
    )
    return directory


def country_data_filename(config=None):
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
    config = ensure_config(config)
    filename = os.path.join(
        config["saved_data"]["cleaned_tables"]["country_data"]["filename"],
    )
    return filename


def country_data_location(config=None):
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
    config = ensure_config(config)
    location = os.path.join(
        country_data_directory(config),
        country_data_filename(config)
    )
    return location
