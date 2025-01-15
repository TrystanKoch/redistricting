"""Functions to parse complicated config options that are used in multiple places."""

import os
import tomllib


CONFIG = "config.toml"


def ensure_config(config=None):
    """
    Check if config dictionary already defined. Otherwise, open config file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    if not config:
        with open(CONFIG, "rb") as config_file:
            config = tomllib.load(config_file)
    return config


def downloads_directory(config=None):
    """Return configured downloads directory for project.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def state_boundary_directory(config=None):
    """
    Return directory for the census state boundary file.
    
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"]
    )
    return directory


def state_boundary_filename(config=None):
    """
    Return filename the census state boundary file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    filename_template = config["census_urls"]["state_boundaries"]["filename_template"]
    filename = filename_template.format(
        directory_year=config["census_urls"]["state_boundaries"]["directory_year"],
        boundary_resolution=config["census_urls"]["state_boundaries"]["boundary_resolution"],
    )
    return filename


def state_boundary_url(config=None):
    """
    Return census URL for the census state boundary file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    url_directory_template = config["census_urls"]["state_boundaries"]["directory_template"]
    url_directory = url_directory_template.format(
        directory_year = config["census_urls"]["state_boundaries"]["directory_year"]
    )
    filename = state_boundary_filename()
    url = f"{url_directory}/{filename}"
    return url


def state_population_directory(config=None):
    """
    Return directory for census state population file.
    
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def state_population_filename(config=None):
    """
    Return filename for census state population file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    filename_template = config["census_urls"]["apportionment_population"]\
                                             ["states_filename_template"]
    filename = filename_template.format(
        census_year = config["census_urls"]["census_year"]
    )
    return filename


def state_population_url(config=None):
    """Return census url for census state population file.
    
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    url_directory_template = config["census_urls"]["apportionment_population"]["directory_template"]
    url_directory = url_directory_template.format(
        census_year = config["census_urls"]["census_year"]
    )
    filename = state_population_filename()
    url = f"{url_directory}/{filename}"
    return url


def fips_identifiers_directory(config=None):
    """
    Return directory for census state FIPS identification file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["downloads"]["directory"],
    )
    return directory


def fips_identifiers_filename(config=None):
    """
    Return directory for census state FIPS identification file.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    filename = config["census_urls"]["FIPS_identifiers"]["filename"]
    return filename


def fips_identifiers_url(config=None):
    """
    Return directory for census state FIPS identification file.
    
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    url_directory = config["census_urls"]["FIPS_identifiers"]["directory"]
    filename = fips_identifiers_filename()
    url = f"{url_directory}/{filename}"
    return url


def census_block_directory(config=None):
    """
    Return directory for census block files.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["state_census_blocks"]["directory"]
    )
    return directory


def census_block_filename(fips_id, config=None):
    """
    Return filename for census block file of state with given id.
    
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
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


def census_block_url(fips_id, config=None):
    """
    Return url for census block file of state with given id.

    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = ensure_config(config)
    census_block_config = config["census_urls"]["census_blocks"]
    url_directory_template = census_block_config["directory_template"]
    url_directory = url_directory_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"],
    )
    filename = census_block_filename(fips_id)
    url = f"{url_directory}/{filename}"
    return url
