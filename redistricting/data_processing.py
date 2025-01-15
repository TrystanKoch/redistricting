"""Functions to turn the census files into cleaner tables."""

import pandas as pd

from data_acquisition import ensure_state_population_table, ensure_fips_identifiers


def create_state_table():
    """
    Create a cleaned state population table from separate census files.
    """
    ensure_state_population_table()
    ensure_fips_identifiers()

    state_pop_table = pd.read_excel(
        "data/downloads/apportionment-2020-table01.xlsx",
        header = 3,
        usecols = [0, 1],
        names = ["STATE", "POP20"],
        skipfooter = 2,
    )

    fips_table_raw = pd.read_csv("data/downloads/state.txt", delimiter='|')
    fips_table = (fips_table_raw
        .drop("STATENS", axis=1)
        .rename(columns={"STATE": "FIPS", "STATE_NAME":"STATE", "STUSAB":"ABBR"})
    )

    state_table = pd.merge(state_pop_table, fips_table, how="inner", on="STATE")[["FIPS", "ABBR","STATE", "POP20"]]

    state_table.to_csv("data/prepared/states.csv", index=False)
