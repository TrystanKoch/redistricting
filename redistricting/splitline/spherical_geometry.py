"""Functions that operate on shapes in curvilinear CRS spaces."""

import warnings
import math

import geopandas as gpd
import pyproj

def centered_gnomonic_crs(shape):
    """Create gnomonic coordinate reference system around a point.

    Creates a gnomonic CRS centered at a geographic shape's approximate 
    centroid.

    A "gnomonic" projection is one where all lines represent great circles.

    Parameters
    ----------
    shape : geopandas.geodataframe.GeoDataFrame
        A geographic shape defined through latitude and longitude in NAD83
    
    Returns
    -------
    pyproj.crs.crs.CRS
        A gnomonic CRS centered on the geographic shape
    
    """
    with warnings.catch_warnings():
        # The exact point we choose for our crs will not affect the great
        # circle we find, so the centroid does not need to be exact. Assume
        # flat earth for simplicity :-)
        warnings.simplefilter("ignore")
        center = shape.centroid

    # Friendly note: this resulting CRS definitely does NOT assume a flat
    # earth.
    return pyproj.CRS.from_proj4(
        f"+proj=gnom "
        f"+lon_0={center.x.iloc[0]} "
        f"+lat_0={center.y.iloc[0]} "
    )


def aeqd_from_point(p):
    """Create an Azimuthal Equidistand CRS centered at a point.
    
    Parameters
    ----------
    p : shapely.geometry.Point
        A point intended as the center of an Azimuthal equidistant projection
    
    Returns
    -------
    pyproj.CRS
        An azimutal equidistant coordinate reference frame centered at p.

    Notes
    -----
    The coordinates of p must be latitude and longitude for this function to
    either work or have any meaning.

    """
    return pyproj.CRS.from_proj4(
        f"+proj=aeqd "
        f"+lon_0={p.x} "
        f"+lat_0={p.y} "
    )


def distance_to_aeqd_point(p):
    """Compute a distance between a point and the origin.

    Parameters
    ----------
    p : shapely.geometry.Point
        A point in an azimuthal equidistant coordinate reference system

    Returns
    -------
    float
        The distance between this point and the origin
    
    Notes
    -----
    Intended to be used along with a point in an azimuthal equidistant
    coordinate reference system that is centered on an origin point. In any
    other case, this is just a flat 2d distance.

    """
    return math.sqrt(p.x*p.x + p.y*p.y)


def geom_with_crs(geometry, crs):
    """Convert a shapely geometry back to a geodataframe.

    Parameters
    ----------
    geometry : shapely.Geometry
        A geometry representing some set of points in a CRS
    crs : pyproj.CRS
        A coordinate reference system

    Returns
    -------
    geopandas.DataFrame
        A geodataframe wrapping the geometry with the crs
    
    """
    return gpd.GeoDataFrame(
        {'geometry' : [geometry]},
        crs=crs
    )


def find_great_circle_distance(start, end, crs, lat_lon_crs_name="EPSG:4326"):
    """Find the great circle distance between two points.

    Parameters
    ----------
    start : shapely.geometry.Point
        An origin point
    end : shapely.geometry.Point
        A second point
    crs : pyproj.CRS
        A coordinate reference system.
    lat_lon_crs_name : str
        An identifier for a CRS that gives latitude and longitude.

    Returns
    -------
    float
        The great circle distance between the two points.
    
    """
    start_lat_lon = (
        geom_with_crs(start, crs)
        .to_crs(lat_lon_crs_name)
        .geometry.iloc[0]
    )
    aeqd_crs = aeqd_from_point(start_lat_lon)
    end_aeqd = (
        geom_with_crs(end, crs)
        .to_crs(aeqd_crs)
        .geometry.iloc[0]
    )
    return distance_to_aeqd_point(end_aeqd)
