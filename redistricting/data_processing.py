"""Functions to turn the census files into cleaner tables."""

import pandas as pd

from data_acquisition import ensure_state_population_table, ensure_fips_identifiers
import config_parsing


def create_state_data():
    """
    Process and the census population files to a single lookup file.
    """
    ensure_state_population_table()
    ensure_fips_identifiers()

    pops_raw = pd.read_excel(
        config_parsing.state_population_location(),
        header=4,
        usecols=[0,2,3],
        skipfooter = 1,
        names = ["STATE", "RESPOP20", "OVSPOP20"],
        na_values ="X",
    )

    pops = (pops_raw
        .assign(POP20 = lambda df_: (df_["RESPOP20"] + df_["OVSPOP20"].fillna(0))
                .astype("int64"))
        .drop(["RESPOP20", "OVSPOP20"], axis=1)
    )

    fips_raw = pd.read_csv(
        config_parsing.fips_identifiers_location(),
        delimiter = "|",
    )

    fips = (fips_raw
        .drop("STATENS", axis=1)
        .rename(columns={"STATE": "FIPS", "STATE_NAME":"STATE", "STUSAB":"ABBR"})
    )

    state_data_full = pd.merge(
        pops, fips,
        how="inner",
        on="STATE",
    )

    state_data = state_data_full[["FIPS", "ABBR", "STATE", "POP20"]]

    state_data.to_csv(config_parsing.state_data_location(), index=False)
