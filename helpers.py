def sum_mods(modifiers, prop):
    """Sum up the specified property of a list of dictionaries."""
    return sum(modifier[prop] for modifier in modifiers if prop in modifier)

def get_res(equipment, body_part):
     """Return the physical and elemental resistances for a given body part."""
     for item in equipment:
        if item["body_part"] == body_part:
            return (item["phys_res"], item["elem_res"])

     return (None, None)  # Return (None, None) if the body part is not found

