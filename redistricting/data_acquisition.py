"""Utilities for downloading census files."""

import urllib.request
import os.path

from typing import Optional

from . import config_parsing


def download_file(url: str, destination: str) -> None:
    """Download a web file's data into a local file.

    Parameters
    ----------
    url : str
        URL of the desired file
    destination : str
        Filename to save project to

    """
    with (
        open(destination, "wb+") as local_file,
        urllib.request.urlopen(url) as web_file,
    ):
        local_file.write(web_file.read())


def ensure_census_file(
        directory: str,
        filename: str,
        url: str,
        redownload: bool = False,
        interactive: bool = False
    ) -> bool:
    """Ensure that a file exists.

    Checks whether a file exists in a given directory. If not, downloads it.

    Parameters
    ----------
    directory : str
        The directory we want a given file to be in
    filename : str
        The census filename for the given file
    url : str
        The census url for the given file
    redownload : bool
        Whether we want to redownload the file if it already exists
    interactive : bool
        Whether to ask the user to download a missing file

    Returns
    -------
    bool
        Whether the specified file exists now

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
            download_wanted = input(
                f"{destination} not found. Download it? [y/n]? "
            )
            if download_wanted not in ["y", "Y", "yes", "Yes", "YES"]:
                return False
        print(f"Downloading {destination}.")
        download_file(url, destination)
    return True


def ensure_state_shapes(
        redownload: bool = False,
        config: Optional[config_parsing.Config] = None
    ) -> None:
    """Ensure we have the state shape file from the census.

    Parameters
    ----------
    redownload : bool
        Whether we want to redownload the file if it already exists
    config : Optional[dict]
        Optional configuration dictionary

    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.state_shapes_directory(config),
        config_parsing.state_shapes_filename(config),
        config_parsing.state_shapes_url(config),
        redownload=redownload
    )

def ensure_fips_identifiers(
        redownload: bool = False,
        config: Optional[config_parsing.Config] = None
    ) -> None:
    """Ensure we have the fips identifier table from the census.

    Parameters
    ----------
    redownload : bool
        Whether we want to redownload the file if it already exists
    config : Optional[dict]
        Optional configuration dictionary

    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.fips_identifiers_directory(config),
        config_parsing.fips_identifiers_filename(config),
        config_parsing.fips_identifiers_url(config),
        redownload=redownload
    )


def ensure_state_census_blocks(
        fips_id: int,
        redownload: bool = False,
        config: Optional[config_parsing.Config] = None
    ) -> None:
    """Ensure we have the census block file for a state.

    Parameters
    ----------
    fips_id : int or str
        The two digit FIPS identifier for a particular state
    redownload : bool
        Whether we want to redownload the file if it already exists
    config : Optional[dict]
        Optional configuration dictionary

    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.census_blocks_directory(config),
        config_parsing.census_blocks_filename(fips_id, config),
        config_parsing.census_blocks_url(fips_id, config),
        redownload=redownload
    )

def ensure_state_population_table(
        redownload: bool = False,
        config: Optional[config_parsing.Config] = None
    ) -> None:
    """Ensure we have the state population table from the census.

    Parameters
    ----------
    redownload : bool
        Whether we want to redownload the file if it already exists
    config : Optional[dict]
        Optional configuration dictionary

    """
    config = config_parsing.ensure_config(config)
    ensure_census_file(
        config_parsing.state_population_directory(config),
        config_parsing.state_population_filename(config),
        config_parsing.state_population_url(config),
        redownload=redownload
    )
