"""All functions relating to parsing command line arguments."""

import sys

FIPS="FIPS"
ABBR="ABBR"
STATE="STATE"
FIPS_LEN=2

def parse_state(state_arg, state_df):
    """Determine which state the user wants.

    While most of the functions in this project require a FIPS code to
    determine a state or territory, it would be helpful to look this
    information up for an end user. So this function lets you search for a
    state's FIPS code by name or abbreviation.

    Parameters
    ----------
    state_arg: str
        A string representing user input
    state_df: pandas.core.frame.DataFrame
        A dataframe where we can look up a state's FIPS id

    """
    state_arg = " ".join(state_arg)

    if state_arg.isdigit() and len(state_arg) <= FIPS_LEN:
        state_entry = state_df[state_df[FIPS] == int(state_arg)]
    elif len(state_arg) == FIPS_LEN:
        state_entry = state_df[state_df[ABBR] == state_arg.upper()]
    else:
        state_entry = state_df[state_df[STATE] == state_arg.title()]

    if not state_entry.empty:
        state_id = str(state_entry[FIPS].iloc[0]).zfill(2)
        return state_id
    sys.exit(1)
