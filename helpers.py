import pandas as pd

def sum_mods(modifiers, prop):
    """Sum up the specified property of a list of dictionaries."""
    return sum(modifier[prop] for modifier in modifiers if prop in modifier)

def get_val(dataframe, name):
    """Uses dataframe as dictionary and get value that corresponds to name."""
    return dataframe.set_index('Name').loc[name, 'Value']

def get_res(equipment, body_part):
     """Return the physical and elemental resistances for a given body part."""
     for item in equipment:
        if item["body_part"] == body_part:
            return (item["phys_res"], item["elem_res"])

     return (None, None)  # Return (None, None) if the body part is not found

def get_df(client, sheet, worksheet):
    """Gets a worksheet from currently loaded sheet and transforms it into a dataframe"""
    sheet = client.open(sheet)
    worksheet = sheet.worksheet(worksheet)
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df