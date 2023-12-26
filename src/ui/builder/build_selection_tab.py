import ipywidgets as widgets


def render_build_selection(client):
    selectors = []
    traits_layout = widgets.VBox()

    # ===================== ADD =====================

    add_button = widgets.Button(
        button_style="success",
        icon="plus",
        layout=widgets.Layout(
            width="240px",
        ),
    )

    add_button.on_click(
        lambda btn: add_selector(client, selectors, traits_layout, "traits", "name")
    )

    add_button_hbox = widgets.HBox(
        [add_button],
        layout=widgets.Layout(
            display="flex",
            flex_flow="column",
            align_items="center",
            width="100%",  # Adjust the percentage as needed for the right column
            margin="10px 0px 0px 0px",
        ),
    )

    # ===================== ADD =====================

    selectors_box = widgets.VBox(
        [traits_layout, add_button_hbox],
        layout=widgets.Layout(
            padding="10px",
        ),
    )

    return selectors_box


def generate_selector(dataframe, column_name):
    has_max_stack = "Stack" in dataframe.columns
    options = dataframe[column_name].dropna().unique()

    # ===================== DROPDOWN =====================

    dropdown = widgets.Dropdown(
        options=options,
        value=None,
        layout=widgets.Layout(flex="2 2 auto", width="200px"),
    )

    # ===================== SLIDER =====================

    slider = widgets.IntSlider(
        min=0,
        max=10,
        step=1,
        disabled=not has_max_stack,
        layout=widgets.Layout(
            flex="1 1 auto", width="auto", margin="0px 40px 0px 40px"
        ),
    )

    # ===================== RESET =====================

    def reset_dropdown(btn):
        dropdown.value = None
        slider.value = 0

    reset_button = widgets.Button(
        icon="rotate-left",
        button_style="warning",
        layout=widgets.Layout(flex="0 1 auto", width="auto"),
    )
    reset_button.on_click(reset_dropdown)

    # ===================== REMOVE =====================

    remove_button = widgets.Button(
        icon="ban",
        button_style="danger",
        layout=widgets.Layout(flex="0 1 auto", width="auto"),
    )
    
    
    # TODO UPDATE REMOVE CALLBACK TO REMOVE THE SELECTOR FROM THE LAYOUT AND SELECTION
    
    remove_button.on_click(
        lambda btn: remove_selector()
    )

    # ===================== SELECTOR =====================

    selector_box = widgets.HBox(
        [dropdown, slider, reset_button, remove_button],
        layout=widgets.Layout(
            display="flex",
            flex_flow="row",
            align_items="stretch",
            width="100%",
            margin="10px 0px 10px 0px",
        ),
    )

    return selector_box


def add_selector(client, selectors, layout, dataframe_name, column_name):
    dataframe = client.get_df("model", dataframe_name)

    # get_selector now returns a single HBox object, not a tuple
    selector_widget = generate_selector(dataframe, column_name)

    # Update the selector dictionary
    selectors.append(selector_widget)

    # Add the HBox to the VBox children
    layout.children += (selector_widget,)


def remove_selector(selectors, idx, layout):
    if len(selectors):
        selectors.pop(idx)
        layout.children.pop(idx)


# TODO ADD UPDATE CALLBACK TO UPDATE THE SELECTION 

    # def update_dropdown(change):
    #     if change["type"] == "change" and change["name"] == "value":
    #         new_value = change["new"]
    #         old_value = change["old"]
    #         if new_value is not None:
    #             selection[id] = new_value
    #             if has_max_stack:
    #                 slider.max = dataframe.loc[
    #                     dataframe[column] == new_value, "Stack"
    #                 ].values[0]
    #                 label.value = f"max stack: {slider.max}"
    #         if old_value is not None:
    #             selection.pop(id, None)

    # dropdown.observe(update_dropdown, names="value")

    # if has_max_stack:

    #     def update_slider(change):
    #         if change["type"] == "change" and change["name"] == "value":
    #             if dropdown.value:
    #                 selection[id] = (dropdown.value, change["new"])

    #     slider.observe(update_slider, names="value")

    # box = widgets.HBox([dropdown, slider, button, label])
    # return box
