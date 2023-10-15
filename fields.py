import ipywidgets as widgets
from helpers import get_df 

def get_selector(id, dataframe, column, selection):
    """Test"""
    has_max_stack = 'Stack' in dataframe.columns 
    options = dataframe[column]

    dropdown = widgets.Dropdown(
        options=options,
        value=None,
        description=id,
    )

    if has_max_stack:
      slider = widgets.IntSlider(
          value=1,
          min=1,
          max=10,
          step=1,
          description='Number:',
          disabled=True,
          continuous_update=False  # update the value only when the user releases the slider handle
      )
    else:
      slider = None
    
    label = widgets.Label(value="")

    button = widgets.Button(
        description='Reset'
    )

    def update_dropdown(change):
      if change['name'] == 'label':

        new_value = change['new']
        if new_value is not None:
          if not has_max_stack:
            selection[new_value] = True
          else:
            slider.value = 1
            slider.disabled = False
            slider.max = dataframe.loc[dataframe[column] == new_value, 'Stack'].values[0]
            label.value = f"max stack: {slider.max}"
            selection[new_value] = slider.value
        else:
          if has_max_stack:
            slider.disabled = True
        
        old_value = change['old']
        if old_value is not None:
          del selection[old_value]

        # %clear
        print(selection)
        
    def reset_dropdown(button):
      dropdown.value = None
      label.value = ''

    dropdown.observe(update_dropdown)
    button.on_click(reset_dropdown)

    if has_max_stack:
      def update_slider(change):
        if change['name'] == 'value':
          slider.value = change['new']

        if (dropdown.value):
            selection[dropdown.value] = slider.value
        
        # %clear
        print(selection)

      slider.observe(update_slider)
      box = widgets.HBox([dropdown, slider, button, label])
    else:
      box = widgets.HBox([dropdown, button, label])

    display(box)

    return dropdown, slider

# ==========================================

def modifiers_selection(traits_selection, attributes_selection, items_selection):
  global client

  traits = widgets.Output()
  with traits:
    traits_df = get_df(client, 'test', 'traits').sort_values(by='Name')

    trait_name_1, trait_stack_1 = get_selector('trait_1', traits_df, 'Name', traits_selection)
    trait_name_2, trait_stack_2 = get_selector('trait_2', traits_df, 'Name', traits_selection)
    trait_name_3, trait_stack_2 = get_selector('trait_3', traits_df, 'Name', traits_selection)
    trait_name_4, trait_stack_2 = get_selector('trait_4', traits_df, 'Name', traits_selection)
    trait_name_5, trait_stack_2 = get_selector('trait_5', traits_df, 'Name', traits_selection)
    trait_name_6, trait_stack_2 = get_selector('trait_6', traits_df, 'Name', traits_selection)

  attributes = widgets.Output()
  with attributes:
    attributes_df = get_df(client, 'test', 'attributes').sort_values(by='Name')

    attribute_name_1, attribute_stack_1 = get_selector('attribute_1', attributes_df, 'Name', attributes_selection)
    attribute_name_2, attribute_stack_2 = get_selector('attribute_2', attributes_df, 'Name', attributes_selection)
    attribute_name_3, attribute_stack_2 = get_selector('attribute_3', attributes_df, 'Name', attributes_selection)
    attribute_name_4, attribute_stack_2 = get_selector('attribute_4', attributes_df, 'Name', attributes_selection)
    attribute_name_5, attribute_stack_2 = get_selector('attribute_5', attributes_df, 'Name', attributes_selection)
    attribute_name_6, attribute_stack_2 = get_selector('attribute_6', attributes_df, 'Name', attributes_selection)

  items = widgets.Output()
  with items:
    items_df = get_df(client, 'test', 'items').sort_values(by='Name')

    equipment_head, equipment_stack_1 = get_selector('head_eq', items_df, 'Name', items_selection)
    equipment_torso, equipment_stack_2 = get_selector('torso_eq', items_df, 'Name', items_selection)
    equipment_arms, equipment_stack_2 = get_selector('arms_eq', items_df, 'Name', items_selection)
    equipment_legs, equipment_stack_2 = get_selector('legs_eq', items_df, 'Name', items_selection)
    equipment_weapon_1, equipment_stack_2 = get_selector('wpn_eq_1', items_df, 'Name', items_selection)
    equipment_weapon_2, equipment_stack_2 = get_selector('wpn_eq_2', items_df, 'Name', items_selection)

  tabs = widgets.Tab()
  tabs.children = [traits, attributes, items]

  # Set tab titles
  tabs.set_title(0, 'Traits')
  tabs.set_title(1, 'Attributes')
  tabs.set_title(2, 'Items')

  display(tabs)