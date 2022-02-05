"""
Calculates the next sat pass, using specified predictor and times. Several
algorthims are envisaged.
"""

from datetime import datetime, timedelta
from enum import Enum
from math import sin, cos, acos, pi
from orbit_predictor.predictors.base import CartesianPredictor
from orbit_predictor.locations import Location

class PassAlgo(Enum):
    """List of available algorithms for calculating the sat pass."""
    TIME_TICKS = 1
    DISTANCE = 2
    MAX_STEPS = 3

# It's ok to have more than 5 arguments.
# pylint: disable=R0913
def get_pass(pred: CartesianPredictor, loc: Location, aos: datetime, los: datetime,
             algo: PassAlgo, delta: float):
    """Returns position list for specified satellite (identified by predictor) for
       specified location, between AOS (start time) and LOS (end time). algo
       specifies the algorithm for picking the intermediate steps. delta is
       a parameter that is algorithm dependent. smooth parameter determines if
       the locations should be averaged. If set to False, the antenna will point
       exactly at the current sat location. Effectively, the antenna will
       always be lagging behind. When set to True, it will take the current
       and next point and will average them. As a result, the antenna will be
       roughly 50% of the time ahead of the sat and 50% lagging behind.

       TIME_TICKS - antenna is moved every delta seconds
       DISTANCE - antenna is moved if its pointing deviates from the sat position
                  by more than delta degrees (not implemented yet)
       MAX_STEPS - conducts the whole fly over with exactly delta number of steps

       TIME_TICKS is the most basic algorithm and easiest to implement and understand.
       However, its flaw comes from varying radial velocity of a passing sat. When
       it's low over the horizon, the angular movement is very slow, so frequent
       rotator movements are not necessary. However, when the sat get closer to
       the zenith, its angular velocity increases greatly, so frequent rotator
       adjustments would be useful. The delta parameter is interpreted as seconds.

       DISTANCE - this algorithm attempts to address the problem described above
       by deciding to conduct the next move depending on how far the antenna and
       sat position differ. Tuning this parameter requires a knowledge of the
       antenna characteristics. If its very narrow, then you'd want to make many
       small adjustments. For wider beam antennas, fewer larger adjustments may
       be better. The delta parameter is interpreted as angular degrees.

       MAX_STEPS - this is another possible approach that splits the total pass
       into specified number of equal steps. It's somewhat similar to TIME_TICKS,
       but may possibly be a bit better in treating very long and very brief
       passes more uniformly. The delta parameter is interpreted as number of steps.
       Highly experimental."""

    pos_list = []

    if algo == PassAlgo.TIME_TICKS:
        d = timedelta(seconds = delta)
    elif algo == PassAlgo.MAX_STEPS:
        d = (los - aos) / delta
    elif algo == PassAlgo.DISTANCE:
        d = timedelta(seconds = 1)

    t = aos
    while t < los:
        t += d
        # Make sure we don't do anything stupid, like tracking below horizon. If the next
        # step would put as past LOS (i.e. below horizon), trim down the last interval
        # and end it early.
        t = min(t, los)
        pos = pred.get_position(t)
        az, el = loc.get_azimuth_elev_deg(pos)

        if algo in [PassAlgo.TIME_TICKS, PassAlgo.MAX_STEPS]:
            # Time ticks and maximum steps algorithms add the position all the time.
            pos_list.append([t, az, el])
        if algo == PassAlgo.DISTANCE:
            # The distance algorithm adds the next position only if its distance is
            # greater than specified value.
            if not pos_list:
                pos_list.append([t, az, el])
                continue
            [old_az, old_el] = pos_list[-1]
            if distance(az, el, old_az, old_el) > delta:
                pos_list.append([t, az, el])

    return pos_list

def deg2rad(x: float) -> float:
    """Converts value specified in degress into radians."""
    return x/180.0*pi

def rad2deg(x: float) -> float:
    """Converts value specified in radians into degrees."""
    return x*180.0/pi

def distance(az1: float, el1:float, az2:float, el2: float) -> float:
    """ Calculates spherical distance between two points (az1, el1) and (az2, el2).
        The azimuth/elevation parameters are expressed in degrees. The value is
        returned in degrees.

        az = lon = lambda, el = lat = phi """
    az1 = deg2rad(az1)
    el1 = deg2rad(el1)
    az2 = deg2rad(az2)
    el2 = deg2rad(el2)

    # This is based on the classical great circle distance. See here for details:
    # https://en.wikipedia.org/wiki/Great-circle_distance#Formulae
    d = acos(sin(el1)*sin(el2) + cos(el1)*cos(el2)*cos(az2-az1))
    return rad2deg(d)
