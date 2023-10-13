from enum import Enum

class RaceAlignment(Enum):
    PURIST = 'P'
    SAVAGE = 'S'
    ANIMUS = 'A'
    ZBORG = 'Z'

class BodyPart(Enum):
    TORSO = "torso"
    HEAD = "head"
    L_ARM = "l_arm"
    R_ARM = "r_arm"
    L_LEG = "l_leg"
    R_LEG = "r_leg"