import ipywidgets as widgets


def render_preview():
    # Accordion sections titles
    sections = [
        "Stats",
        "Caps",
        "Budgets",
        "General Proficiencies",
        "Combat Proficiencies",
        "Skills",
        "Abilities",
    ]

    # Create the accordion widget
    accordion = widgets.Accordion(
        children=[
            widgets.VBox([widgets.Label("Content for " + section)])
            for section in sections
        ],
        layout=widgets.Layout(
            padding="10px",
            width="70%",  # Adjust the percentage as needed for the left column
        ),
    )
    for i, section in enumerate(sections):
        accordion.set_title(i, section)

    # Create buttons with similar layout as previous example
    button_layout = widgets.Layout(
        margin="10px 0px 10px 0px", width="120px"
    )  # Top, Right, Bottom, Left

    sync_button = widgets.Button(
        description="Sync model",
        icon="refresh",
        button_style="primary",
        layout=button_layout,
    )

    save_button = widgets.Button(
        description="Save char",
        icon="cloud",
        button_style="success",
        layout=button_layout,
    )

    # Create VBox for buttons
    buttons_vbox = widgets.VBox(
        [sync_button, save_button],
        layout=widgets.Layout(
            padding="10px",
            display="flex",
            flex_flow="column",
            align_items="center",
            width="30%",  # Adjust the percentage as needed for the right column
        ),
    )

    # Create HBox for the overall layout
    preview_hbox = widgets.HBox(
        [accordion, buttons_vbox],
        layout=widgets.Layout(
            display="flex",
            align_items="stretch",
            width="100%",
        ),
    )

    return preview_hbox
