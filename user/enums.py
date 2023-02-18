from enum import Enum


class GenderTypes(Enum):
    MALE = 1
    FEMALE = 2
    NOT_SET = 0


class UserStatus(Enum):
    ACTIVE = 1
    INACTIVE = 0
    DELETED = 3
