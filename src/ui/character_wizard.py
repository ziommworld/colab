import ipywidgets as widgets
from IPython.display import display

from src import BodyType, RaceAlignment
from src.forge.character_builder import CharacterBuilder
from src.shared.client import GoogleSheetsClient
from src.ui.builder.build_selection_tab import render_build_selection
from src.ui.builder.preview_tab import render_preview
from src.ui.builder.properties_tab import render_properties


class CharacterWizard:
    def __init__(self, client: GoogleSheetsClient):
        # builder = CharacterBuilder({}, test_mode=True)
        self.client = GoogleSheetsClient(test_mode=True)
        self.render_wizard()

    def render_wizard(self):
        initial_props = {
            "body_type": BodyType.BEASTUMANOID.name,
            "level": 1,
            "race": RaceAlignment.SAVAGE.name,
            "alignment": RaceAlignment.SAVAGE.name,
            "name": "Test",
        }
        initial_props = None

        properties_tab = render_properties(initial_props)

        traits_df = self.client.get_df("model", "traits")
        traits_tab = render_build_selection(traits_df)

        attributes_df = self.client.get_df("model", "attributes")
        attributes_tab = render_build_selection(attributes_df)

        items_df = self.client.get_df("model", "items")
        items_tab = render_build_selection(items_df)

        preview_tab, sync_outputs = render_preview()

        sync_outputs["Stats"]("Stats")
        sync_outputs["Caps"]("Caps")
        sync_outputs["Budgets"]("Budgets")
        sync_outputs["GPs"]("GPs")
        sync_outputs["CPs"]("CPs")
        sync_outputs["Skills"]("Skills")
        sync_outputs["Abilities"]("Abilities")

        tab = widgets.Tab(
            children=[
                properties_tab,
                traits_tab,
                attributes_tab,
                items_tab,
                preview_tab,
            ]
        )
        tab.set_title(0, "Properties")
        tab.set_title(1, "Traits")
        tab.set_title(2, "Attributes")
        tab.set_title(3, "Items")
        tab.set_title(4, "Preview")

        display(tab)
