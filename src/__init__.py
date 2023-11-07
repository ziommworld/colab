from enum import Enum


class BodyType(Enum):
    HUMANOID = "humanoid"


class BodyPartType(Enum):
    TORSO = "torso"
    HEAD = "head"
    L_ARM = "l_arm"
    R_ARM = "r_arm"
    L_LEG = "l_leg"
    R_LEG = "r_leg"


class InjuryType(Enum):
    BLEED = "bleed"
    SHOCK = "shock"
    CONCUSSION = "concussion"
    INJURY = "injury"


BODY_CONFIGS = {
    BodyType.HUMANOID: {
        BodyPartType.HEAD: {
            "max_injuries": {
                InjuryType.BLEED: 3,
                InjuryType.SHOCK: 3,
                InjuryType.CONCUSSION: 4,
            }
        },
        BodyPartType.TORSO: {
            "max_injuries": {
                InjuryType.BLEED: 3,
                InjuryType.SHOCK: 3,
            }
        },
        BodyPartType.L_ARM: {
            "max_injuries": {
                InjuryType.INJURY: 2,
            }
        },
        BodyPartType.R_ARM: {
            "max_injuries": {
                InjuryType.INJURY: 2,
            }
        },
        BodyPartType.L_LEG: {
            "max_injuries": {
                InjuryType.INJURY: 2,
            }
        },
        BodyPartType.R_LEG: {
            "max_injuries": {
                InjuryType.INJURY: 2,
            }
        },
    },
}
