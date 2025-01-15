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


def ensure_state_boundaries(redownload=False):
    """
    Downloads the state boundary file from the census.
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    state_boundaries_directory = os.path.join(data_directory, downloads_directory)

    try:
        os.makedirs(state_boundaries_directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {state_boundaries_directory}")

    filename_template = config["census_urls"]["state_boundaries"]["filename_template"]
    directory_year = config["census_urls"]["state_boundaries"]["directory_year"]
    filename = filename_template.format(
        directory_year=directory_year,
        boundary_resolution=config["census_urls"]["state_boundaries"]["boundary_resolution"],
    )

    destination = os.path.join(data_directory, downloads_directory, filename)
    if not os.path.isfile(destination) or redownload:
        print(f"Downloading {destination}")

        url_directory_template = config["census_urls"]["state_boundaries"]["directory_template"]
        url_directory = url_directory_template.format(
            directory_year=directory_year
        )
        url = f"{url_directory}/{filename}"

        download_file(url, destination)


def ensure_fips_identifiers(redownload=False):
    """
    Checks whether we have the fips identifier table from the census. Downloads them if not.
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    fips_directory = os.path.join(data_directory, downloads_directory)

    try:
        os.makedirs(fips_directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {fips_directory}")

    filename = config["census_urls"]["FIPS_identifiers"]["filename"]
    destination = os.path.join(fips_directory, filename)
    if not os.path.isfile(destination) or redownload:
        print(f"Downloading {destination}")

        url_directory = config["census_urls"]["FIPS_identifiers"]["directory"]
        filename = config["census_urls"]["FIPS_identifiers"]["filename"]
        url = f"{url_directory}/{filename}"

        download_file(url, destination)


def ensure_state_population_table(redownload=False):
    """
    Checks whether we have the state population table from the census. Downloads it if not.
    """
    with open(CONFIG, "rb") as config_file:
        config = tomllib.load(config_file)

    census_year = config["census_urls"]["census_year"]

    data_directory = config["saved_data"]["directory"]
    downloads_directory = config["saved_data"]["downloads"]["directory"]
    pop_table_directory = os.path.join(data_directory, downloads_directory)

    try:
        os.makedirs(pop_table_directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {pop_table_directory}")

    filename_template = config["census_urls"]["apportionment_population"]["states_filename_template"]
    filename = filename_template.format(
        census_year = census_year
    )

    destination = os.path.join(data_directory, downloads_directory, filename)
    if not os.path.isfile(destination) or redownload:
        print(f"Downloading {destination}")

        url_directory_template = config["census_urls"]["apportionment_population"]["directory_template"]
        url_directory = url_directory_template.format(
            census_year = census_year
        )
        url = f"{url_directory}/{filename}"

        download_file(url, destination)


def ensure_state_census_blocks(fips_id, redownload=False):
    """
    Checks whether we already have the census blocks for a given state, downloads them if not.

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
    if not os.path.isfile(destination) or redownload:
        print(f"Downloading {destination}")

        url_directory_template = census_block_config["directory_template"]
        url_directory = url_directory_template.format(
            directory_year = census_block_config["directory_year"],
            census_year_short = config["census_urls"]["census_year_short"],
        )
        url = f"{url_directory}/{filename}"

        download_file(url, destination)
