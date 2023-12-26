import ipywidgets as widgets


def render_build_selection(df):
    selectors = []
    traits_layout = widgets.VBox()

    def add_selector(df, selectors, layout, column_name):
        selector_widget = generate_selector(df, column_name, selectors, layout)
        selectors.append(selector_widget)
        layout.children += (selector_widget,)

    def generate_selector(dataframe, column_name, selectors, layout):
        has_max_stack = "Stack" in dataframe.columns
        options = dataframe[column_name].dropna().unique()

        dropdown = widgets.Dropdown(
            options=options,
            value=None,
            layout=widgets.Layout(flex="2 2 auto", width="200px"),
        )

        slider = widgets.IntSlider(
            min=0,
            max=10,
            step=1,
            disabled=not has_max_stack,
            layout=widgets.Layout(
                flex="1 1 auto", width="auto", margin="0px 40px 0px 40px"
            ),
        )

        def reset_dropdown(btn):
            dropdown.value = None
            slider.value = 0

        reset_button = widgets.Button(
            icon="rotate-left",
            button_style="warning",
            layout=widgets.Layout(flex="0 1 auto", width="auto"),
        )
        reset_button.on_click(reset_dropdown)

        remove_button = widgets.Button(
            icon="ban",
            button_style="danger",
            layout=widgets.Layout(flex="0 1 auto", width="auto"),
        )
        remove_button.on_click(
            lambda btn: remove_selector(selectors, selector_box, layout)
        )

        def on_selection_change(change):
            # Update logic here
            print(f"Selection changed: {change['new']}")

        dropdown.observe(on_selection_change, names="value")
        slider.observe(on_selection_change, names="value")

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

    def remove_selector(selectors, selector_widget, layout):
        if selector_widget in selectors:
            selectors.remove(selector_widget)
            layout.children = [
                child for child in layout.children if child != selector_widget
            ]

    add_button = widgets.Button(
        button_style="success",
        icon="plus",
        layout=widgets.Layout(width="240px"),
    )
    add_button.on_click(lambda btn: add_selector(df, selectors, traits_layout, "name"))

    add_button_hbox = widgets.HBox(
        [add_button],
        layout=widgets.Layout(
            display="flex",
            flex_flow="column",
            align_items="center",
            width="100%",
            margin="10px 0px 0px 0px",
        ),
    )

    selectors_box = widgets.VBox(
        [traits_layout, add_button_hbox],
        layout=widgets.Layout(padding="10px"),
    )

    return selectors_box


# Example usage:
# Assuming you have a dataframe `df` with appropriate columns
# selectors_box = render_build_selection(df)
