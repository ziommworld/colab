import re
import ast

import pandas as pd


# Function to calculate a simple hash of the properties
def calculate_hash(dict):
    # Convert the dictionary into a sorted tuple of tuples
    dict_tuple = tuple(sorted(dict.items()))
    # Convert the tuple into a string
    dict_str = str(dict_tuple)
    # Return the hash of the string
    return hash(dict_str)


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
    # If the cell is empty or not a string, return an empty list
    if cell is None or not isinstance(cell, str):
        return []

    # This regular expression matches tuples in the form (string, number)
    # and adds quotes around the first element of the tuple
    cell = re.sub(r"\((\w+),\s*(\d+)\)", r"('\1', \2)", cell)

    try:
        # Convert the string to a list of tuples using ast.literal_eval
        evaluated = ast.literal_eval(f"[{cell}]")

        # Validate the format of each tuple
        for element in evaluated:
            if not (isinstance(element, tuple) and len(element) == 2):
                raise ValueError(
                    f"Each element must be a tuple of two items, got: {element}"
                )
            if not (
                isinstance(element[0], str) and isinstance(element[1], (int, float))
            ):
                raise ValueError(
                    f"The first item must be a string and the second item must be a number, got: {element}"
                )

        return evaluated

    except (ValueError, SyntaxError) as e:
        # Raise an error with a message indicating which cell caused the problem
        raise ValueError(f"Error processing cell '{cell}': {e}")


# ABC -> [ABC]
# ABC, XYZ -> [ABC, XYZ]
def list_converter(cell):
    # If the cell is not a string, return an empty list
    if not isinstance(cell, str):
        return []

    # First, strip whitespace to ensure that empty lists are correctly identified.
    cell = cell.strip()

    # If the cell is an empty string or just contains empty brackets, return an empty list.
    if cell == "" or cell == "[]":
        return []

    # Now, attempt to convert the cell content to a list.
    try:
        # ast.literal_eval safely evaluates a string as a Python literal (list, dict, etc.).
        # The replace method ensures there are no spaces after commas,
        # which is required for ast.literal_eval to correctly interpret the string as a list.
        cell = cell.replace(", ", ",")
        return ast.literal_eval(cell)
    except (ValueError, SyntaxError):
        # If the conversion fails, it's likely due to the cell not being a valid list string.
        # Depending on the desired behavior, you can return an empty list,
        # the original cell, or raise an error.
        return [cell]
