import ipywidgets as widgets

def get_selector(id, dataframe, column, selection):
    """Test"""
    options = dataframe[column]

    dropdown = widgets.Dropdown(
        options=options,
        value=None,
        description=id,
    )

    slider = widgets.IntSlider(
        value=1,
        min=1,
        max=10,
        step=1,
        description='Number:',
        disabled=True,
        continuous_update=False  # update the value only when the user releases the slider handle
    )
    
    label = widgets.Label(value="")

    button = widgets.Button(
        description='Reset'
    )

    def update_dropdown(change):
      if change['name'] == 'label':
        slider.value = 1

        new_value = change['new']
        if new_value is not None:
          slider.disabled = False
          slider.max = dataframe.loc[dataframe[column] == new_value, 'Stack'].values[0]
          label.value = f"max stack: {slider.max}"
          selection[new_value] = slider.value
        else:
          slider.disabled = True
        
        old_value = change['old']
        if old_value is not None:
          del selection[old_value]

        # %clear
        print(selection)
        
    def update_slider(change):
      if change['name'] == 'value':
        slider.value = change['new']

        if (dropdown.value):
            selection[dropdown.value] = slider.value
        
        # %clear
        print(selection)

    def reset_dropdown(button):
      dropdown.value = None
      label.value = ''

    dropdown.observe(update_dropdown)
    slider.observe(update_slider)
    button.on_click(reset_dropdown)

    # Display the dropdown and output widgets
    box = widgets.HBox([dropdown, slider, button, label])

    display(box)

    return dropdown, slider
