"""Contains functions used in apportioning representatives."""

from math import sqrt

POP_COL = "POP20"
REPS_COL = "reps"

def huntington_hill(population_df, reps):
    """
    Apportion representatives according to the Huntington-Hill apportionment method.

    :param population_df: A dataframe of states (and/or territories) with populations
    :param reps: Number of representatives to apportion.

    Note that there will always be at least one representative per state.
    """
    tmp_df = population_df.copy()
    tmp_df[REPS_COL] = 1

    reps = max(0, reps - tmp_df[REPS_COL].sum())

    if reps > 0:
        tmp_df = tmp_df.assign(
            avg_district_pop = lambda df_: (df_[POP_COL]
                .div(
                    (df_[REPS_COL] * (df_[REPS_COL] + 1)).pow(0.5)
                )
            )
        )

    while reps > 0:
        next_state_id = tmp_df.avg_district_pop.idxmax(axis=0)
        tmp_df.loc[next_state_id, REPS_COL] += 1
        p = tmp_df.loc[next_state_id, POP_COL]
        n = tmp_df.loc[next_state_id, REPS_COL]
        tmp_df.loc[next_state_id, "avg_district_pop"] = p/sqrt(n*(n+1))
        reps -= 1

    tmp_df["avg_district_pop"] = tmp_df[POP_COL].div(tmp_df[REPS_COL]).round()

    return tmp_df
