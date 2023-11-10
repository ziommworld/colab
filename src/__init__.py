from enum import Enum


class RaceAlignment(Enum):
    PURIST = "P"
    SAVAGE = "S"
    ANIMUS = "A"
    ZBORG = "Z"


class BodyType(Enum):
    HUMANOID = "humanoid"
    BEASTUMANOID = "beastumanoid"
    SENTRY = "sentry"
    MECHARACHNID = "mecharachnid"
    AVIAN = "avian"
    QUADRUPED = "quadruped"


class BodyPartType(Enum):
    TORSO = "torso"
    HEAD = "head"
    TAIL = "tail"
    L_ARM_1 = "l_arm_1"
    R_ARM_1 = "r_arm_1"
    L_LEG_1 = "l_leg_1"
    R_LEG_1 = "r_leg_1"
    L_ARM_2 = "l_arm_2"
    R_ARM_2 = "r_arm_2"
    L_LEG_2 = "l_leg_2"
    R_LEG_2 = "r_leg_2"


class InjuryType(Enum):
    BLEED = "bleed"  # humanoid injury
    SHOCK = "shock"  # elemental injury
    CONCUSSION = "concussion"  # head injury
    MALFUNCTION = "malfunction"  # mechanical injury
    IMMOBILIZE = "immobilize"  # leg injury
    DISABLE = "disable"  # arm injury


class CombatProficiency(Enum):
    DODGE = "dodge"
    BLOCK = "block"

    MMA = "mma"
    FINESSE = "finesse"
    CRUDE = "crude"

    ARCHERY = "archery"
    FIREARM = "firearm"
    THROWN = "thrown"

    BITE = "bite"
    CLAW = "claw"
    STING = "sting"


class DamageType(Enum):
    PHYSICAL = "physical"
    ELEMENTAL = "elemental"
    PURE = "pure"


class Ability(Enum):
    CONCUSSIVE = "concussive"


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
        BodyPartType.L_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.R_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.L_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
    },
    BodyType.BEASTUMANOID: {
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
        BodyPartType.L_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.R_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.L_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
    },
    BodyType.SENTRY: {
        BodyPartType.TORSO: {
            "max_injuries": {
                InjuryType.MALFUNCTION: 4,
                InjuryType.SHOCK: 3,
            }
        },
        BodyPartType.L_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.R_ARM_1: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        BodyPartType.L_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
    },
    BodyType.MECHARACHNID: {
        BodyPartType.HEAD: {
            "max_injuries": {
                InjuryType.MALFUNCTION: 2,
                InjuryType.SHOCK: 3,
            }
        },
        BodyPartType.TORSO: {
            "max_injuries": {
                InjuryType.MALFUNCTION: 2,
                InjuryType.SHOCK: 3,
            }
        },
        BodyPartType.TAIL: {
            "max_injuries": {
                InjuryType.DISABLE: 2,
            }
        },
        # limb (leg) pairs
        BodyPartType.L_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 1,
            }
        },
        BodyPartType.R_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 1,
            }
        },
        BodyPartType.L_LEG_2: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 1,
            }
        },
        BodyPartType.R_LEG_2: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 1,
            }
        },
    },
    BodyType.AVIAN: {
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
        BodyPartType.L_ARM_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_ARM_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.L_ARM_2: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 3,
            }
        },
    },
    BodyType.QUADRUPED: {
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
        BodyPartType.L_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_LEG_1: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.L_LEG_2: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
        BodyPartType.R_LEG_2: {
            "max_injuries": {
                InjuryType.IMMOBILIZE: 2,
            }
        },
    },
}


COMBAT_PROFICIENCIES = {
    BodyType.HUMANOID: [
        CombatProficiency.DODGE,
        CombatProficiency.BLOCK,
        CombatProficiency.MMA,
        CombatProficiency.FINESSE,
        CombatProficiency.CRUDE,
        CombatProficiency.ARCHERY,
        CombatProficiency.FIREARM,
        CombatProficiency.THROWN,
    ],
    BodyType.BEASTUMANOID: [
        CombatProficiency.DODGE,
        CombatProficiency.BLOCK,
        CombatProficiency.BITE,
        CombatProficiency.CLAW,
        CombatProficiency.FINESSE,
        CombatProficiency.CRUDE,
        CombatProficiency.ARCHERY,
        CombatProficiency.THROWN,
    ],
    BodyType.SENTRY: [
        CombatProficiency.DODGE,
        CombatProficiency.BLOCK,
        CombatProficiency.FIREARM,
        CombatProficiency.FINESSE,
        CombatProficiency.CRUDE,
        CombatProficiency.THROWN,
    ],
    BodyType.MECHARACHNID: [
        CombatProficiency.DODGE,
        CombatProficiency.BITE,
        CombatProficiency.STING,
        CombatProficiency.FIREARM,
        CombatProficiency.THROWN,
        CombatProficiency.FINESSE,
    ],
    BodyType.AVIAN: [
        CombatProficiency.DODGE,
        CombatProficiency.MMA,
        CombatProficiency.THROWN,
        CombatProficiency.BITE,
        CombatProficiency.CLAW,
    ],
    BodyType.QUADRUPED: [
        CombatProficiency.DODGE,
        CombatProficiency.MMA,
        CombatProficiency.BITE,
        CombatProficiency.CLAW,
    ],
}
