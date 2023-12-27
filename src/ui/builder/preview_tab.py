import ipywidgets as widgets
from IPython.display import display


def render_preview():
    # Accordion sections titles
    sections = [
        "Stats",
        "Caps",
        "Budgets",
        "GPs",
        "CPs",
        "Skills",
        "Abilities",
    ]

    output_widgets = {section: widgets.Output() for section in sections}

    def sync_stats(config):
        output_widget = output_widgets["Stats"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("Stats:"))
            print(f"Syncing... {config}")

    def sync_caps(config):
        output_widget = output_widgets["Caps"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("Caps:"))
            print(f"Syncing... {config}")

    def sync_budgets(config):
        output_widget = output_widgets["Budgets"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("Budgets:"))
            print(f"Syncing... {config}")

    def sync_gps(config):
        output_widget = output_widgets["GPs"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("GPs:"))
            print(f"Syncing... {config}")

    def sync_cps(config):
        output_widget = output_widgets["CPs"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("CPs:"))
            print(f"Syncing... {config}")

    def sync_skills(config):
        output_widget = output_widgets["Skills"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("Skills:"))
            print(f"Syncing... {config}")

    def sync_abilities(config):
        output_widget = output_widgets["Abilities"]
        with output_widget:
            output_widget.clear_output()
            display(widgets.Label("Abilities:"))
            print(f"Syncing... {config}")

    sync_outputs = {
        "Stats": sync_stats,
        "Caps": sync_caps,
        "Budgets": sync_budgets,
        "GPs": sync_gps,
        "CPs": sync_cps,
        "Skills": sync_skills,
        "Abilities": sync_abilities,
    }

    # Create the accordion widget
    accordion = widgets.Accordion(
        children=[output_widgets[section] for section in sections],
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

    return preview_hbox, sync_outputs
