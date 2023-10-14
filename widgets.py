import ipywidgets as widgets

def get_selector(dataframe, column):

    dropdown = widgets.Dropdown(
        options=dataframe[column],
        value=None,
        description='Choose:',
    )

    output = widgets.Output()

    def on_dropdown_change(change):
        if change['type'] == 'change' and change['name'] == 'value':
            # Clear the previous output
            output.clear_output()

            # Get the selected value from the dropdown
            selected_value = change['new']

            # Find the row in the original DataFrame (df) that matches the selected value
            selected_row = dataframe[dataframe[column] == selected_value]

            # Display the selected row
            with output:
                display(selected_row)

    # Set up the event handler for the dropdown
    dropdown.observe(on_dropdown_change)

    # Create a slider
    slider = widgets.IntSlider(
        value=5,  # initial value
        min=1,  # minimum value
        max=10,  # maximum value
        step=1,  # step size
        description='Number:',
        continuous_update=False  # update the value only when the user releases the slider handle
    )

    # slider.observe

    # Display the dropdown and output widgets
    box = widgets.HBox([dropdown, slider])
    
    display(box)

    return output
