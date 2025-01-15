"""All functions relating to parsing command line arguments."""

import sys
import logging


def parse_state(state_arg, state_df):
    """
    Determine which state the user wants.

    :param state_arg: A string representing user input.
    :type state_arg: str
    :param state_df: A dataframe where we can look up a state's FIPS id.
    :type state_df: pandas.DataFrame
    """
    state_arg = " ".join(state_arg)

    if state_arg.isdigit() and len(state_arg) <= 2:
        state_entry = state_df[state_df.FIPS == int(state_arg)]
    elif len(state_arg) == 2:
        state_entry = state_df[state_df.ABBR == state_arg.upper()]
    else:
        state_entry = state_df[state_df.STATE == state_arg.title()]

    if not state_entry.empty:
        state_id = str(state_entry["FIPS"].iloc[0]).zfill(2)
        return state_id
    logging.error("State '%s' not found", state_arg)
    sys.exit(1)
