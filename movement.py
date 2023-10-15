import pandas as pd

def movement_matrix(size):
    def modified_distance(x1, y1, x2, y2):
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        diagonal = min(dx, dy)
        straight = (dx + dy) - 2 * diagonal
        return (diagonal * 4) + (straight * 3)

    # Adjust the function to calculate the distance from (0, 0) instead of from the center
    def modified_distance_from_origin(x, y):
        return modified_distance(x, y, 0, 0)

    center = size // 2  # Central point of the matrix

    # Create DataFrame with modified distances from the origin
    df_origin = pd.DataFrame(index=range(-center, center + 1), columns=range(-center, center + 1))

    # Populate the DataFrame
    for i in df_origin.index:
        for j in df_origin.columns:
            df_origin.at[i, j] = modified_distance_from_origin(i, j)

    return df_origin