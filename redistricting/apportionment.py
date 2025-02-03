"""Contains functions used in apportioning representatives."""

from enum import StrEnum
from math import sqrt

import pandas as pd

from . import data_loading
from . import data_cleaning

POP_COL = "POP20"
REPS_COL = "reps"

class ApportionmentMethod(StrEnum):
    """Possible Apportionment methods."""

    HHILL = "huntington_hill"


def apportion_representatives(
        min_total_reps: int = 435,
        min_state_reps: int = 1,
        include_dc: bool = False,
        include_pr: bool = False,
        method: ApportionmentMethod = ApportionmentMethod.HHILL
    ) -> pd.DataFrame:
    """Apportion US Representatives to the states.

    Parameters
    ----------
    min_total_reps: int
        The number of state representatives to apportion
    min_state_reps: int
        Minimum number of representatives allowed per state
    include_dc: bool
        Whether to apportion representatives to the District of Columbia
    include_pr: bool
        Whether to apportion representatives to Puerto Rico
    method : ApportionmentMethod
        Representative apportionment method

    Returns
    -------
    pd.dataFrame
        A list of states with representatives apportioned
    """
    states = data_loading.load_state_data()

    if not include_dc:
        states = data_cleaning.apportionment_drop_dc(states)

    if not include_pr:
        states = data_cleaning.apportionment_drop_pr(states)

    if method == ApportionmentMethod.HHILL:
        return huntington_hill(states, min_total_reps, min_state_reps)
    else:
        # No options for now. Unlikely to be others, as Huntington-Hill method
        # is well established and optimal. Redundancy here for potential
        # changes.
        return huntington_hill(states, min_total_reps, min_state_reps)


def huntington_hill(
        population_df: pd.DataFrame,
        min_total_reps: int,
        min_state_reps: int = 1
    ) -> pd.DataFrame:
    """Apportion representatives by Huntington-Hill method.

    Note that there will always be at least one representative per state.

    Parameters
    ----------
    population_df : pandas.core.frame.DataFrame
        A dataframe of states (and/or territories) with populations
    min_total_reps : int
        Least number of representatives to apportion
    min_state_reps : int
        Least allowable number of representatives in one state

    Returns
    -------
    pd.DataFrame
        A list of states with representatives apportioned

    """
    tmp_df = population_df.copy()
    tmp_df[REPS_COL] = 1

    reps = max(0, min_total_reps - tmp_df[REPS_COL].sum())

    tmp_df = tmp_df.assign(
        avg_district_pop = lambda df_: (df_[POP_COL]
            .div(
                (df_[REPS_COL] * (df_[REPS_COL] + 1)).pow(0.5)
            )
        )
    )

    while reps > 0 or tmp_df[REPS_COL].min() < min_state_reps:
        next_state_id = tmp_df.avg_district_pop.idxmax(axis=0)
        tmp_df.loc[next_state_id, REPS_COL] += 1
        p: int = tmp_df.loc[next_state_id, POP_COL]
        n: int = tmp_df.loc[next_state_id, REPS_COL]
        tmp_df.loc[next_state_id, "avg_district_pop"] = p/sqrt(n*(n+1))
        reps -= 1

    tmp_df["avg_district_pop"] = tmp_df[POP_COL].div(tmp_df[REPS_COL]).round()

    return tmp_df
