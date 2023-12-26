from IPython.display import display
import ipywidgets as widgets


def render_build_selection(client):
    # Dictionaries to keep track of selectors
    selectors_dict = {"traits": {}, "attributes": {}, "items": {}}

    # Layouts for each category
    traits_layout = widgets.VBox()

    # Add and Remove buttons for each category
    add_trait_button = widgets.Button(description="Add Trait")
    add_trait_button.on_click(
        lambda btn: add_selector(
            "traits", client, selectors_dict, traits_layout, "traits", "name"
        )
    )

    remove_trait_button = widgets.Button(description="Remove Trait")
    remove_trait_button.on_click(
        lambda btn: remove_selector("traits", selectors_dict, traits_layout)
    )

    return widgets.VBox(
        [widgets.HBox([add_trait_button, remove_trait_button]), traits_layout]
    )


def generate_selector(id, dataframe, column, selection):
    has_max_stack = "Stack" in dataframe.columns
    options = dataframe[column].dropna().unique()

    dropdown = widgets.Dropdown(
        options=options,
        value=None,
        description=id,
    )

    slider = widgets.IntSlider(
        value=0,
        min=0,
        max=10,
        step=1,
        description="Stacks:",
        disabled=not has_max_stack,
        continuous_update=False,
    )

    label = widgets.Label(value="")
    button = widgets.Button(description="Reset")

    def update_dropdown(change):
        if change["type"] == "change" and change["name"] == "value":
            new_value = change["new"]
            old_value = change["old"]
            if new_value is not None:
                selection[id] = new_value
                if has_max_stack:
                    slider.max = dataframe.loc[
                        dataframe[column] == new_value, "Stack"
                    ].values[0]
                    label.value = f"max stack: {slider.max}"
            if old_value is not None:
                selection.pop(id, None)

    def reset_dropdown(b):
        dropdown.value = None
        label.value = ""
        slider.value = 0
        selection.pop(id, None)

    dropdown.observe(update_dropdown, names="value")
    button.on_click(reset_dropdown)

    if has_max_stack:

        def update_slider(change):
            if change["type"] == "change" and change["name"] == "value":
                if dropdown.value:
                    selection[id] = (dropdown.value, change["new"])

        slider.observe(update_slider, names="value")

    box = widgets.HBox([dropdown, slider, button, label])
    return box


def add_selector(category, client, selection_dict, layout, dataframe_name, column_name):
    selector_id = f"{category}_{len(selection_dict[category]) + 1}"
    dataframe = client.get_df("model", dataframe_name)

    # get_selector now returns a single HBox object, not a tuple
    selector_widget = generate_selector(
        selector_id, dataframe, column_name, selection_dict
    )

    # Update the selector dictionary
    selection_dict[category][selector_id] = selector_widget

    # Add the HBox to the VBox children
    layout.children += (selector_widget,)


def remove_selector(category, selection_dict, layout):
    if selection_dict[category]:
        selector_id = list(selection_dict[category].keys())[-1]
        del selection_dict[category][selector_id]
        layout.children = list(layout.children)[:-1]
