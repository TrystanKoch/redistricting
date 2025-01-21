"""Functions that operate on shapes in curvilinear CRS spaces."""

import warnings

import pyproj

def centered_gnomonic_crs(shape):
    """
    Creates a gnomonic CRS centered at a geographic shape's approximate centroid.

    A "gnomonic" projection is one where all lines represent great circles.

    :param shape: A geographic shape defined through latitude and longitude in NAD83.
    :type shape: geopandas.geodataframe.GeoDataFrame
    :return: A gnomonic CRS centered on the geographic shape.
    :rtype: pyproj.crs.crs.CRS
    """

    with warnings.catch_warnings():
        # The exact point we choose for our crs will not affect the great
        # circle we find, so the centroid does not need to be exact. Assume
        # flat earth for simplicity :-)
        warnings.simplefilter("ignore")
        center = shape.centroid

    # Friendly note: this resulting CRS definitely does NOT assume a flat earth.
    return pyproj.CRS.from_proj4(
        f"+proj=gnom "
        f"+lon_0={center.x.iloc[0]} "
        f"+lat_0={center.y.iloc[0]} "
    )
