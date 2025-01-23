"""Functions that operate only in flat projections of the spherical space."""

import numpy as np
import pandas as pd

def theta_from_steps(step, total_steps):
    """Converts angular steps to radians.
    
    Gives the angle in radians swept out by "step" steps if a full revolution
    has been split into "total_steps" steps.

    Parameters
    ----------
    step : int
        The number of angluar steps we have taken
    total_steps : int
        The total number of angular steps we want to break a full turn into

    Returns
    -------
    float
        An angle, in radians.
    """
    return (2 * np.pi) * (step / total_steps)



def line_normal(theta):
    """Returns a line's unit normal vector.

    A 2D unit vector that is normal to a line at an angle of theta radians
    with respect to the horizontal.

    Parameters
    ----------
    theta : float
        The angle in radians of a line with respect to the horizontal
    
    Returns
    -------
    numpy.ndarray
        A 2D unit vector at an angle theta + pi
    """
    return np.array([
        -np.sin(theta),
        np.cos(theta)
    ])


def line_tangent(theta):
    """Returns a line's unit tangent vector

    A 2D unit vector that is tangent to a line at an angle of theta radians
    with respect to the horizontal.

    Parameters
    ----------
    theta : float
        The angle of a line with respect to the horizontal
    
    Returns
    -------
    numpy.ndarray
        A 2D unit vector at an angle theta
    """
    return np.array([
        np.cos(theta),
        np.sin(theta)
    ])


def position_dot_products(df_, total_steps):
    """Finds many directed positions for all points in a dataframe.

    Finds the dot products of the position vector (x,y) with the line
    normals for each angle, given a number of steps around the circle we wish
    to calculate.  Larger results indicate that the point is further along in
    that direction compared to points with lower values.

    Parameters
    ----------
    df_: pandas.core.frame.DataFrame
        A dataframe containing x and y position columns
    :type df_: pandas.core.frame.DataFrame
    total_steps: int
        The number of angles we wish to compute during a full revolution.

    
    Returns
    -------
    pandas.core.frame.DataFrame
        Original dataframe with additional columns of dot products
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
    """Sort a dataframe by a column of directed distances.

    Sorts a dataframe by the column representing a particular angular step's 
    dot products.

    Parameters
    ----------
    df_ : pandas.core.frame.DataFrame
        Dataframe of block centroids with appended dot product columns
    n : int or str
        The column or integer for a column to sort the dataframe by

    Returns
    -------
    pandas.core.frame.DataFrame
        Sorted dataframe
    """
    return df_.sort_values([str(n)])
