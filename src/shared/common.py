import re


def to_snake_case(name):
    """
    Convert a name to snake_case.
    """
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    name = re.sub(r"\W", "", name)
    return name
