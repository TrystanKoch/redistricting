"""Functions to turn the census files into cleaner tables."""

import os
import pandas as pd

from . import data_acquisition
from . import config_parsing


def create_state_data() -> None:
    """Processs census files to a single state population lookup table.

    Notes
    -----
    Creates a file.

    """
    data_acquisition.ensure_state_population_table()
    data_acquisition.ensure_fips_identifiers()

    pops_raw = pd.read_excel(
        config_parsing.state_population_location(),
        header=4,
        usecols=[0,2,3],
        skipfooter = 1,
        names = ["STATE", "RESPOP20", "OVSPOP20"],
        na_values ="X",
    )

    pops = (pops_raw
        .assign(
            POP20 = lambda df_: (
                df_["RESPOP20"] + df_["OVSPOP20"].fillna(0)
            )
            .astype("int64")
        )
        .drop(["RESPOP20", "OVSPOP20"], axis=1)
    )

    fips_raw = pd.read_csv(
        config_parsing.fips_identifiers_location(),
        delimiter = "|",
    )

    fips = (fips_raw
        .drop("STATENS", axis=1)
        .rename(
            columns={
                "STATE": "FIPS",
                "STATE_NAME":"STATE",
                "STUSAB":"ABBR"
            }
        )
    )

    state_data_full = pops.merge(
        fips,
        how="inner",
        on="STATE",
    )

    state_data = state_data_full[["FIPS", "ABBR", "STATE", "POP20"]]

    directory = config_parsing.state_data_directory()
    try:
        os.makedirs(directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {directory}")

    state_data.to_csv(config_parsing.state_data_location(), index=False)


def create_country_data() -> None:
    """Processs census files to a single country-wide population lookup table.

    Notes
    -----
    Creates a file.

    """
    data_acquisition.ensure_state_population_table()

    pops_raw = pd.read_excel(
        config_parsing.state_population_location(),
        header=4,
        usecols=[0,2,3],
        skipfooter = 1,
        names = ["STATE", "RESPOP20", "OVSPOP20"],
        na_values ="X",
    )

    pops = (
        pops_raw
        .assign(
            POP20 = lambda df_: (
                df_["RESPOP20"] + df_["OVSPOP20"].fillna(0)
            )
            .astype("int64")
        )
        .drop(["RESPOP20", "OVSPOP20"], axis=1)
    )

    dc_total = (
        pops
        .loc[pops["STATE"] == "District of Columbia"]
        .iloc[0,1]
    )
    us_dc_total = (
        pops
        .loc[pops["STATE"] == "U.S. Total"]
        .iloc[0,1]
    )
    us_dc_pr_total = (
        pops
        .loc[pops["STATE"] == "U.S. Total and Puerto Rico"]
        .iloc[0,1]
    )

    if not (
        isinstance(us_dc_total, int)
        and isinstance(dc_total, int)
        and isinstance(us_dc_pr_total, int)
    ):
        raise TypeError
    us_total = us_dc_total - dc_total

    country_data = pd.DataFrame({
        "REGION": ["US", "US_DC", "US_DC_PR"],
        "POP20" : [us_total, us_dc_total, us_dc_pr_total]
    })

    directory = config_parsing.country_data_directory()
    try:
        os.makedirs(directory)
    except OSError:
        pass
    else:
        print(f"Created directory: {directory}")

    country_data.to_csv(config_parsing.country_data_location(), index=False)
