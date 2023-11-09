from enum import Enum

class SpecificCalibMode(Enum):
    _MEDIAN = 1
    _MEAN = 2
    _MIN = 3
    _MAX = 4
    NA = 0

class ModelNameEnum(Enum):
    STATIC = 1
    EMPIRICAL_DIST = 2
    UNIFORM_Q1_Q3 = 3
    UNIFORM_AVG_STDEV = 4
