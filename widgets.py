import ipywidgets as widgets
from IPython.display import display


def get_selector(dataframe, column):
    """Test"""

    dropdown = widgets.Dropdown(
        options=dataframe[column],
        value=None,
        description='Choose:',
    )

    slider = widgets.IntSlider(
        value=5,
        min=1,
        max=10,
        step=1,
        description='Number:',
        continuous_update=False  # update the value only when the user releases the slider handle
    )

    # slider.observe

    # Display the dropdown and output widgets
    box = widgets.HBox([dropdown, slider])

    display(box)

    return dropdown, slider

