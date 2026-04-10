from enum import Enum


class LabelType(Enum):
    MAT = 1
    GTL = 2


class OpConTestComparator(Enum):
    EQ = 1
    NEQ = 2
    Contains = 3
    Absent = 4
    Exists = 5
