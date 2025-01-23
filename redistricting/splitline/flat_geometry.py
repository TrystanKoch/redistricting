"""Functions that operate only in flat projections of the spherical space."""

import numpy as np
import pandas as pd

def theta_from_steps(step, total_steps):
    """
    Gives the angle in radians swept out by "step" steps if a full revolution h
    as been split into "total_steps" steps.

    :param step: The number of angluar steps we have taken.
    :type step: int
    :param total_steps: The total number of angular steps we want to break a 
    full turn into.
    :type total_steps: int
    :returns: The angle, in radians.
    :rtype: float
    """
    return (2 * np.pi) * (step / total_steps)



def line_normal(theta):
    """
    A 2D unit vector that is normal to a line at an angle of theta radians
    with respect to the horizontal.

    :param theta: The angle of a line with respect to the horizontal.
    :type theta: float
    :returns: A 2D normal vector.
    :rtype: numpy.ndarray
    """
    return np.array([
        -np.sin(theta),
        np.cos(theta)
    ])


def line_tangent(theta):
    """
    A 2D unit vector that is tangent to a line at an angle of theta radians
    with respect to the horizontal.

    :param theta: The angle of a line with respect to the horizontal.
    :type theta: float
    :returns: A 2D tangent vector.
    :rtype: numpy.ndarray
    """
    return np.array([
        np.cos(theta),
        np.sin(theta)
    ])


def position_dot_products(df_, total_steps):
    """
    Finds the dot products of the position vector (x,y) with the line
    normals for each angle, given a number of steps around the circle we wish
    to calculate.  Larger results indicate that the point is further along in
    that direction compared to points with lower values.

    :param df_: A dataframe containing x and y position columns
    :type df_: pandas.core.frame.DataFrame
    :param total_steps: The number of angles we wish to compute during a full 
    revolution.
    :type total_steps: int
    :returns: Original dataframe with "total_steps" additional columns of dot 
    products.
    :rtype: pandas.core.frame.DataFrame
    """
    # Create a smaller dataframe just from the relevent columns.
    df_xy = df_[["x", "y"]]

    # Because dataframes create copies of themselves on every assignment or
    # append, it is much faster to create a list of dataframes and then
    # concatenate them once than to continuously append new columns to one
    # dataframe.
    directed_distances = []
    for step in range(total_steps):
        unit_normal = line_normal(theta_from_steps(step, total_steps))
        directed_distances.append(
            pd.DataFrame(
                # Take the dot product of the z and y columns with the unit 
                # normal to the line at an angle to the horizontal.
                df_xy.dot(unit_normal),

                # Name each column after the integer step that is taken.
                columns=[f"{step}"],
            )
        )
    df_ = pd.concat([df_, *directed_distances], axis=1)

    # Note: the final dataframe is quite large. However, this allows us to do
    # this calculation once instead of calculating the direction dot products
    # in every recursive step.
    return df_


def sort_by_angle_step(df_, n):
    """
    Sorts a dataframe by the column representing a particular angular step's 
    dot products.

    :param df_: Dataframe of block centroids with appended dot product columns
    :type df_: pandas.core.frame.DataFrame
    :param n: The column or integer for a column to sort the dataframe by.
    :type n: int or str
    :returns: Sorted DataFrame
    :rtype: pandas.core.frame.DataFrame
    """
    return df_.sort_values([str(n)])
