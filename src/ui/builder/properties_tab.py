import ipywidgets as widgets


# Function to create properties tab content
def render_properties():
    input_layout = widgets.Layout(
        margin="10px 0px 10px 0px", width="100%"
    )  # Top, Right, Bottom, Left

    name_widget = widgets.Text(value="Kano", description="Name:", layout=input_layout)
    level_widget = widgets.IntSlider(
        value=4, min=1, max=8, step=1, description="Level:", layout=input_layout
    )
    body_type_widget = widgets.Dropdown(
        options=[
            "HUMANOID",
            "BEASTUMANOID",
            "SENTRY",
            "MECHARACHNID",
            "AVIAN",
            "QUADRUPED",
        ],
        value="HUMANOID",
        description="Body Type:",
        layout=input_layout,
    )
    race_widget = widgets.Dropdown(
        options=["PURIST", "SAVAGE", "ANIMUS", "ZBORG"],
        value="SAVAGE",
        description="Race:",
        layout=input_layout,
    )
    alignment_widget = widgets.Dropdown(
        options=["PURIST", "SAVAGE", "ANIMUS", "ZBORG"],
        value="SAVAGE",
        description="Alignment:",
        layout=input_layout,
    )

    def update_props(b):
        props = {
            "name": name_widget.value,
            "level": level_widget.value,
            "body_type": body_type_widget.value,
            "race": race_widget.value,
            "alignment": alignment_widget.value,
        }
        print(props)  # Just for demonstration

    button_layout = widgets.Layout(
        margin="10px 0px 10px 0px", width="100px"
    )  # Top, Right, Bottom, Left

    update_button = widgets.Button(
        description="Update",
        button_style="primary",
        layout=button_layout,
    )
    update_button.on_click(update_props)

    flex_layout = widgets.Layout(
        display="flex",
        flex_flow="row",
        align_items="stretch",
        width="100%",
    )

    left_vbox = widgets.VBox(
        [name_widget, level_widget, body_type_widget, race_widget, alignment_widget],
        layout=widgets.Layout(
            padding="10px",
            width="60%",  # Adjust the percentage as needed for the left column
        ),
    )

    right_vbox = widgets.VBox(
        [update_button],
        layout=widgets.Layout(
            padding="10px",
            display="flex",
            flex_flow="column",
            align_items="center",
            width="40%",  # Adjust the percentage as needed for the right column
        ),
    )

    content_hbox = widgets.HBox([left_vbox, right_vbox], layout=flex_layout)

    return content_hbox
