import re
import ast

import pandas as pd


def to_snake_case(name):
    """
    Convert a name to snake_case.
    """
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
    name = re.sub(r"\W", "", name)
    return name


def try_convert_to_numeric(value):
    try:
        return pd.to_numeric(value)
    except ValueError:
        return value


def tuple_converter(cell):
    try:
        # Evaluate it as if it's a tuple directly
        evaluated = ast.literal_eval(cell)
        if isinstance(evaluated, tuple):
            # Ensure all non-numeric elements are treated as strings
            return tuple(
                str(item) if not isinstance(item, (int, float)) else item
                for item in evaluated
            )
        return evaluated
    except (ValueError, SyntaxError):
        # If it fails to evaluate, return as is (it's probably a string)
        return cell


# ABC -> [ABC]
# ABC, XYZ -> [ABC, XYZ]
def list_converter(self, cell):
    try:
        # Remove spaces after commas for proper list conversion
        cell = cell.replace(", ", ",")
        return ast.literal_eval(cell)
    except (ValueError, SyntaxError):
        # If conversion fails, return the cell as a list with a single string element
        return [cell]
