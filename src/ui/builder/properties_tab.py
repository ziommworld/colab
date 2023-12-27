import ipywidgets as widgets

from src.shared.common import calculate_hash


# Function to create properties tab content
def render_properties(initial_props=None):
    current_hash = None
    new_hash = None

    input_layout = widgets.Layout(
        margin="10px 0px 10px 0px", width="100%"
    )  # Top, Right, Bottom, Left

    name_widget = widgets.Text(
        value=initial_props["name"] if initial_props else "Kano",
        description="Name:",
        layout=input_layout,
    )
    level_widget = widgets.IntSlider(
        value=initial_props["level"] if initial_props else 4,
        min=1,
        max=8,
        step=1,
        description="Level:",
        layout=input_layout,
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
        value=initial_props["body_type"] if initial_props else "HUMANOID",
        description="Body Type:",
        layout=input_layout,
    )
    race_widget = widgets.Dropdown(
        options=["PURIST", "SAVAGE", "ANIMUS", "ZBORG"],
        value=initial_props["race"] if initial_props else "SAVAGE",
        description="Race:",
        layout=input_layout,
    )
    alignment_widget = widgets.Dropdown(
        options=["PURIST", "SAVAGE", "ANIMUS", "ZBORG"],
        value=initial_props["alignment"] if initial_props else "SAVAGE",
        description="Alignment:",
        layout=input_layout,
    )

    def update_props(btn):
        nonlocal current_hash
        props = {
            "name": name_widget.value,
            "level": level_widget.value,
            "body_type": body_type_widget.value,
            "race": race_widget.value,
            "alignment": alignment_widget.value,
        }
        current_hash = calculate_hash(props)
        update_button.disabled = True
        print(props)  # Just for demonstration

    button_layout = widgets.Layout(
        margin="10px 0px 10px 0px", width="120px"
    )  # Top, Right, Bottom, Left

    update_button = widgets.Button(
        description="Update props",
        icon="check",
        button_style="info",
        layout=button_layout,
    )
    update_button.on_click(update_props)

    # Function to check for changes in properties
    def check_for_changes(change):
        nonlocal new_hash
        props = {
            "name": name_widget.value,
            "level": level_widget.value,
            "body_type": body_type_widget.value,
            "race": race_widget.value,
            "alignment": alignment_widget.value,
        }
        new_hash = calculate_hash(props)
        update_button.disabled = new_hash == current_hash

    name_widget.observe(check_for_changes, names="value")
    level_widget.observe(check_for_changes, names="value")
    body_type_widget.observe(check_for_changes, names="value")
    race_widget.observe(check_for_changes, names="value")
    alignment_widget.observe(check_for_changes, names="value")

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

    properties_hbox = widgets.HBox([left_vbox, right_vbox], layout=flex_layout)

    return properties_hbox
