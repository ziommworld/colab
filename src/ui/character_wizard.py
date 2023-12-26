import ipywidgets as widgets
from IPython.display import display

from src.forge.character_builder import CharacterBuilder
from src.shared.client import GoogleSheetsClient
from src.ui.builder.build_selection_tab import render_build_selection
from src.ui.builder.properties_tab import render_properties


class CharacterWizard:
    def __init__(self, client: GoogleSheetsClient):
        # builder = CharacterBuilder({}, test_mode=True)
        self.client = GoogleSheetsClient(test_mode=True)
        self.render_wizard()

    def render_wizard(self):
        properties_content = render_properties()
        traits_content = render_build_selection(self.client)
        attributes_content = widgets.VBox([widgets.Label("Attributes content here")])
        items_content = widgets.VBox([widgets.Label("Items content here")])
        preview_content = widgets.VBox([widgets.Label("Preview content here")])

        tab = widgets.Tab(
            children=[
                properties_content,
                traits_content,
                attributes_content,
                items_content,
                preview_content,
            ]
        )
        tab.set_title(0, "Properties")
        tab.set_title(1, "Traits")
        tab.set_title(2, "Attributes")
        tab.set_title(3, "Items")
        tab.set_title(4, "Preview")

        display(tab)
