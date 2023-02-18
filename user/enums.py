from enum import Enum


class GenderTypes(Enum):
    NONE = 1
    MALE = 2
    FEMALE = 3
    NOT_SET = 4


class UserStatus(Enum):
    ACTIVE = 1
    INACTIVE = 0
    DELETED = 3
