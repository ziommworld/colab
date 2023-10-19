import pandas as pd
from IPython.display import display, clear_output
import ipywidgets as widgets


def range_matrix(size, half, full):
    lgreen = "#A4D682"
    dgreen = "#6B7823"
    blue = "#4078A4"
    orange = "#FF8C00"
    red = "#FF5050"

    melee = 3
    reaching = 6
    short = 10
    mid = 30
    long = 50

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
    df = pd.DataFrame(
        index=range(-center, center + 1), columns=range(-center, center + 1)
    )

    # Populate the DataFrame
    for i in df.index:
        for j in df.columns:
            df.at[i, j] = modified_distance_from_origin(i, j)

    def highlight_cells(value):
        if half is None and full is None:
            if value <= melee:
                return f"background-color: {lgreen}"
            elif value <= reaching:
                return f"background-color: {dgreen}"
            elif value <= short:
                return f"background-color: {blue}"
            elif value <= mid:
                return f"background-color: {orange}"
            elif value <= long:
                return f"background-color: {red}"
        else:  # explosions
            if value <= half:
                return f"background-color: {red}"
            elif value <= full:
                return f"background-color: {orange}"

    return df.style.applymap(highlight_cells)


# ++++++++


def display_range_matrix(init_ms=15):
    tab1_content = widgets.Output()
    tab2_content = widgets.Output()
    tab3_content = widgets.Output()
    tab4_content = widgets.Output()

    def display_range_matrix(change):
        with tab1_content:
            clear_output(wait=True)
            display(range_matrix(30, None, None))
        with tab2_content:
            clear_output(wait=True)
            display(range_matrix(10, 3, 6))
        with tab3_content:
            clear_output(wait=True)
            display(range_matrix(10, 6, 9))
        with tab4_content:
            clear_output(wait=True)
            display(range_matrix(10, 9, 12))

    # Create Tab widgets
    tabs = widgets.Tab()

    # Set the titles and content for each tab
    tabs.children = [tab1_content, tab2_content, tab3_content, tab4_content]

    # Set tab titles
    tabs.set_title(0, "Ranges")
    tabs.set_title(1, "Explosive")
    tabs.set_title(2, "Hexplosive")
    tabs.set_title(3, "Sexplsove")

    # Display the combined widget
    display_range_matrix(None)
    display(tabs)
