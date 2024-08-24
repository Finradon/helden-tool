from enum import Enum
from random import randint
# module to define custom dice methods

class roll(Enum):
    CRIT = 1
    CRIT_CONF = 2
    SUCCESS = 3
    FAIL = 4
    FAIL_CONF = 5

def d20 () -> int:
    """
    One d20
    """
    return randint(1, 20)

def d6 () -> int:
    """
    One d6
    """
    return randint(1, 6)

def xd6(count) -> int:
    """
    Roll X amount of d6
    @return: sum of all d6 rolls
    """
    res = 0
    for i in range(count):
        res += d6()
    
    return res

def xd20(count) -> int:
    """
    Roll X amount of d20s
    @return: sum of all d20 rolls
    """
    res = 0
    for i in range(count):
        res += d20()
    
    return res
