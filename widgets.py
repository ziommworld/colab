import ipywidgets as widgets
from IPython.display import display


def get_selector(dataframe, column, selection):
    """Test"""

    dropdown = widgets.Dropdown(
        options=dataframe[column],
        value=None,
        description='Choose:',
    )

    slider = widgets.IntSlider(
        value=1,
        min=1,
        max=10,
        step=1,
        description='Number:',
        continuous_update=False  # update the value only when the user releases the slider handle
    )

    def update_dropdown(change):
        dropdown.value = change['new']
        slider.value = 1

        selection[dropdown.value] = slider.value

    def update_slider(change):
        slider.value = change['new']

        selection[dropdown.value] = slider.value

    dropdown.observe(update_dropdown)
    slider.observe(update_slider)

    # Display the dropdown and output widgets
    box = widgets.HBox([dropdown, slider])

    display(box)

    return dropdown, slider
