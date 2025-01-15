"""Utilities for downloading census files"""

import urllib
import tomllib
import os.path

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


def download_state_boundaries():
    """
    Downloads the state boundary file from the census.
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    url_directory_template = config["census_urls"]["state_boundaries"]["directory_template"]
    directory_year = config["census_urls"]["state_boundaries"]["directory_year"]
    url_directory = url_directory_template.format(
        directory_year=directory_year
    )

    filename_template = config["census_urls"]["state_boundaries"]["filename_template"]
    filename = filename_template.format(
        directory_year=directory_year,
        boundary_resolution=config["census_urls"]["state_boundaries"]["boundary_resolution"],
    )

    url = f"{url_directory}/{filename}"

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    destination = os.path.join(data_directory, downloads_directory, filename)

    download_file(url, destination)


def download_fips_identifiers():
    """
    Downloads the FIPS identification file from the census.
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    url_directory = config["census_urls"]["FIPS_identifiers"]["directory"]
    filename = config["census_urls"]["FIPS_identifiers"]["filename"]
    url = f"{url_directory}/{filename}"

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    destination = os.path.join(data_directory, downloads_directory, filename)

    download_file(url, destination)


def download_state_population_table():
    """
    Downloads the state population table from the census
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    census_year = config["census_urls"]["census_year"]

    url_directory_template = config["census_urls"]["apportionment_population"]["directory_template"]
    url_directory = url_directory_template.format(
        census_year = census_year
    )

    filename_template = config["census_urls"]["apportionment_population"]["states_filename_template"]
    filename = filename_template.format(
        census_year = census_year
    )

    url = f"{url_directory}/{filename}"

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    destination = os.path.join(data_directory, downloads_directory, filename)

    download_file(url, destination)


def ensure_state_census_blocks(fips_id):
    """
    Checks whether we already have the census blocks, downloads them if not.

    :param fips_id: The two digit FIPS identifier for a particular state.
    :type fips_id: int or str
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    census_block_directory = os.path.join(
        config["saved_data"]["directory"],
        config["saved_data"]["state_census_blocks"]["directory"]
    )

    try:
        os.makedirs(census_block_directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {census_block_directory}")

    census_block_config = config["census_urls"]["census_blocks"]
    filename_template = census_block_config["filename_template"]
    filename = filename_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"],
        state_fips = f"{fips_id:02}",
    )

    destination = os.path.join(census_block_directory, filename)
    if os.path.isfile(destination):
        redownload_input = input(f"{destination} exists. Redownload? [y/n]")
        if redownload_input not in ["y", "Y", "Yes", "yes"]:
            return
    print(f"Downloading {destination}")
    download_state_census_blocks(fips_id)


def download_state_census_blocks(fips_id):
    """
    Downloads the shapefile containing a state's census data at the block level.
    
    :param fips_id: The two digit FIPS identifier for a particular state.
    :type fips_id: int or str
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    census_block_config = config["census_urls"]["census_blocks"]

    url_directory_template = census_block_config["directory_template"]
    url_directory = url_directory_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"]
    )

    filename_template = census_block_config["filename_template"]
    filename = filename_template.format(
        directory_year = census_block_config["directory_year"],
        census_year_short = config["census_urls"]["census_year_short"],
        state_fips = f"{fips_id:02}",
    )

    url = f"{url_directory}/{filename}"

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["state_census_blocks"]["directory"]
    destination = os.path.join(data_directory, downloads_directory, filename)

    download_file(url, destination)
