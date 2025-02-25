"""Module for Representative aportionment."""

from .apportionment import ApportionmentMethod
from .apportionment import apportion_representatives
from .apportionment import huntington_hill

__all__ = [
    "ApportionmentMethod",
    "apportion_representatives",
    "huntington_hill"
]
