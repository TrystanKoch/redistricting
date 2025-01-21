"""Contains functions used in apportioning representatives."""

from math import sqrt

POP_COL = "POP20"
REPS_COL = "reps"

def huntington_hill(population_df, min_total_reps, min_state_reps=1):
    """
    Apportion representatives according to the Huntington-Hill apportionment method.

    :param population_df: A dataframe of states (and/or territories) with populations
    :type population_df: pandas.core.frame.DataFrame
    :param min_total_reps: Least number of representatives to apportion.
    :type min_total_reps: int
    :param min_state_reps: Least allowable number of representatives in one state.
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
