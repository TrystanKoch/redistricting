"""Utilities for downloading census files"""

import urllib
import os.path

import config_parsing

CONFIG = "config.toml"

def download_file(url, destination):
    """
    Downloads a web file's data into a local file.

    :param url: URL of the desired file.
    :type url: str
    :param dest: Filename to save project to.
    :type dest: str  
    """
    with (
        open(destination, "wb+") as local_file,
        urllib.request.urlopen(url) as web_file,
    ):
        local_file.write(web_file.read())


def ensure_census_file(directory, filename, url, redownload=False, interactive=False):
    """
    Check whether a file exists in a given directory, or else download it.

    :param directory: The directory we want a given file to be in.
    :type directory: str
    :param filename: The census filename for the given file.
    :type filename: str
    :param url: The census url for the given file.
    :type url: str
    :param redownload: Whether we want to redownload the file if it already exists.
    :type redownload: bool
    :param interactive: Whether to ask the user to download a missing file.
    :type interactive: bool
    :return: Whether the specified file exists.
    :rtype: bool
    """
    # Check if directory exists already. If not, make it.
    try:
        os.makedirs(directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {directory}")

    # Check if file exists. If not, or if redownload is wanted, download it.
    destination = os.path.join(directory, filename)
    if not os.path.isfile(destination) or redownload:
        if interactive and not redownload:
            download_wanted = input(f"{destination} not found. Download it? [y/n]? ")
            if download_wanted not in ["y", "Y", "yes", "Yes", "YES"]:
                return False
        print(f"Downloading {destination}.")
        download_file(url, destination)
    return True


def ensure_state_boundaries(redownload=False, config=None):
    """
    Ensures we have the state boundary file from the census.

    :param redownload: Whether we want to redownload the file if it already exists.
    :type redownload: bool
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.state_boundary_directory(config),
        config_parsing.state_boundary_filename(config),
        config_parsing.state_boundary_url(config),
        redownload=redownload
    )

def ensure_fips_identifiers(redownload=False, config=None):
    """
    Ensures we have the fips identifier table from the census.

    :param redownload: Whether we want to redownload the file if it already exists.
    :type redownload: bool
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.fips_identifiers_directory(config),
        config_parsing.fips_identifiers_filename(config),
        config_parsing.fips_identifiers_url(config),
        redownload=redownload
    )


def ensure_state_census_blocks(fips_id, redownload=False, config=None):
    """
    Ensures we have the census block file for the state with the given fips_id.

    :param fips_id: The two digit FIPS identifier for a particular state.
    :type fips_id: int or str
    :param redownload: Whether we want to redownload the file if it already exists.
    :type redownload: bool
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.census_blocks_directory(config),
        config_parsing.census_blocks_filename(fips_id, config),
        config_parsing.census_blocks_url(fips_id, config),
        redownload=redownload
    )

def ensure_state_population_table(redownload=False, config=False):
    """
    Ensures we have the state population table from the census.

    :param redownload: Whether we want to redownload the file if it already exists.
    :type redownload: bool
    :param config: Optional configuration dictionary.
    :type config: Optional[dict]
    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.state_population_directory(config),
        config_parsing.state_population_filename(config),
        config_parsing.state_population_url(config),
        redownload=redownload
    )
