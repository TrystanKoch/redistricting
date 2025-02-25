"""Functions that operate only in flat projections of the spherical space."""

import math

import numpy as np
import pandas as pd
import shapely


def theta_from_steps(step: int, total_steps: int) -> float:
    """Convert angular steps to radians.

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



def line_normal(theta: float) -> np.ndarray:
    """Return a 2D line's unit normal vector.

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


def line_tangent(theta: float) -> np.ndarray:
    """Return a 2D line's unit tangent vector.

    A 2D unit vector that is tangent to a line at an angle of theta radians
    with respect to the horizontal.

    Parameters
    ----------
    theta : float
        The angle in radians of a line with respect to the horizontal

    Returns
    -------
    numpy.ndarray
        A 2D unit vector at an angle theta

    """
    return np.array([
        np.cos(theta),
        np.sin(theta)
    ])


def position_dot_products(
        df_: pd.DataFrame,
        total_steps: int
    ) -> pd.DataFrame:
    """Find many directed positions for all points in a dataframe.

    Finds the dot products of the position vector (x,y) with the line
    normals for each angle, given a number of steps around the circle we wish
    to calculate.  Larger results indicate that the point is further along in
    that direction compared to points with lower values.

    Parameters
    ----------
    df_: pandas.core.frame.DataFrame
        A dataframe containing x and y position columns
    total_steps: int
        The number of angles we wish to compute during a full revolution

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


def sort_by_angle_step(df_: pd.DataFrame, n: int) -> pd.DataFrame:
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


def point_angle_line(
        p: shapely.Point,
        theta: float,
        length: float = 2_000_000
    ) -> shapely.LineString:
    """Create a long line from a point and an azimuthal angle.

    Parameters
    ----------
    p : shapely.geometry.Point
        A midpoint on the line
    theta : float
        The angle at which the line intercepts the point
    length : float
        The length of the line, larger than any shape considered

    Returns
    -------
    shapely.geometry.LineString
        A long line that intercepts the point p at an angle theta

    """
    p0 = np.array([p.x, p.y])
    t = line_tangent(theta)
    d = length
    start_p = p0 - t*d/2
    end_p = p0 + t*d/2
    return shapely.LineString([
        start_p,
        end_p
    ])


def directed_distance(
        p: shapely.Point,
        t: np.ndarray[float]
    ) -> float:
    """Dot product of the point's position vector with a vector.

    Parameters
    ----------
    p : shapely.geometry.Point
        A location
    t : numpy.ndarray
        A 2D vector

    Returns
    -------
    float
        The distance of a point from the origin in the direction t.

    Notes
    -----
    For this to be interpretable, t should be a unit vector. Strictly
    speaking, this is not necessary.

    """
    return p.x*t[0] + p.y*t[1]




def boundary_intersection_points(
        shape: shapely.Geometry,
        p: shapely.Point,
        theta: float
    ) -> tuple[shapely.Point, shapely.Point]:
    """Find the intersection of a shape's boundary and a line.

    Parameters
    ----------
    shape : shapely.Geometry
        A shape representing a region
    p : shapely.geometry.Point
        A point the line goes through
    theta : float
        The angle in radians at which the line intercepts the point

    Returns
    -------
    tuple[shapely.geometry.Point, shapely.geometry.Point]
        Two points where the line intersects the shape's boundary

    Notes
    -----
    For this to be interperetable, the point p should be inside the shape
    under consideration.

    Additionally, if there are more than two intersections, this function
    will return the two that are most distant from one another.

    The points are returned in order of the directed distance along the line.
    A line at angle theta and a line at angle theta + pi, will therefore
    return the same points but in reverse order.

    """
    boundary = shape.boundary
    line = point_angle_line(p, theta)
    intersections = shapely.intersection(boundary, line)

    t = line_tangent(theta)

    min_d = math.inf
    max_idx = 0
    max_d = -math.inf
    min_idx = 0
    idx = 0

    for point in intersections.geoms:
        d = directed_distance(point, t)
        if d < min_d:
            min_d = d
            min_idx = idx
        if d > max_d:
            max_d = d
            max_idx = idx
        idx += 1

    start_point = intersections.geoms[min_idx]
    end_point = intersections.geoms[max_idx]

    return start_point, end_point


def midpoint(p1: shapely.Point, p2: shapely.Point) -> shapely.Point:
    """Find a point halfway beteen two points.

    Parameters
    ----------
    p1 : shapely.geometry.Point
        A point
    p2 : shapely.geometry.Point
        A second point

    Returns
    -------
    shapely.geometry.Point
        A point halfway between the inputs

    """
    return shapely.geometry.Point(
        (p1.x + p2.x) / 2,
        (p1.y + p2.y) / 2
    )
