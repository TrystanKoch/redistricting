"""Contains functions used in apportioning representatives."""

from enum import StrEnum
from math import sqrt

from . import data_loading
from . import data_cleaning

POP_COL = "POP20"
REPS_COL = "reps"

class ApportionmentMethod(StrEnum):
    """Possible Apportionment methods"""
    HHILL = "huntington_hill"


def apportion_representatives(
        min_total_reps=435,
        min_state_reps=1,
        include_dc=False,
        include_pr=False,
        method=ApportionmentMethod.HHILL
    ):
    """
    Apportion US Representatives to the states.

    :param min_total_reps: The number of state representatives to apportion.
    :type min_total_reps: int
    :param min_state_reps: Optional minimum number of representatives allowed 
    per state.
    :type min_state_reps: int
    :param include_dc: Whether to apportion representatives to the District of 
    Columbia.
    :type include_dc: bool
    :param include_pr: Whether to apportion representatives to Puerto Rico.
    :type include_pr: bool
    :param method: Representative apportionment method.
    :type method: ApportionmentMethod
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



def huntington_hill(population_df, min_total_reps, min_state_reps=1):
    """
    Apportion representatives according to the Huntington-Hill apportionment 
    method.

    :param population_df: A dataframe of states (and/or territories) with 
    populations
    :type population_df: pandas.core.frame.DataFrame
    :param min_total_reps: Least number of representatives to apportion.
    :type min_total_reps: int
    :param min_state_reps: Least allowable number of representatives in one 
    state.
    :type min_state_reps: int
    
    Note that there will always be at least one representative per state.
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
        p = tmp_df.loc[next_state_id, POP_COL]
        n = tmp_df.loc[next_state_id, REPS_COL]
        tmp_df.loc[next_state_id, "avg_district_pop"] = p/sqrt(n*(n+1))
        reps -= 1

    tmp_df["avg_district_pop"] = tmp_df[POP_COL].div(tmp_df[REPS_COL]).round()

    return tmp_df
