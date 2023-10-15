import pandas as pd
from IPython.display import display, clear_output
import ipywidgets as widgets

def movement_matrix(ms, action):
    lgreen = '#A4D682'
    dgreen = '#6B7823'
    orange = '#FF8C00'
    red = '#FF5050'

    size = (ms if action == 'walk' else (2 * ms if action == 'run' else 4 * ms)) + 3
    print(size)
    def modified_distance(x1, y1, x2, y2):
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        diagonal = min(dx, dy)
        straight = (dx + dy) - 2 * diagonal
        return (diagonal * 4) + (straight * 3)

    # Adjust the function to calculate the distance from (0, 0) instead of from the center
    def modified_distance_from_origin(x, y):
        return modified_distance(x, y, 0, 0)

    center = size // 2  # Central point of the matrix

    # Create DataFrame with modified distances from the origin
    df = pd.DataFrame(index=range(-center, center + 1), columns=range(-center, center + 1))

    # Populate the DataFrame
    for i in df.index:
        for j in df.columns:
            df.at[i, j] = modified_distance_from_origin(i, j)

    ap_1_sta = 0
    ap_2_sta = 0
    ap_3_sta = 0
    ap_4_sta = 0

    for ap in range(1, 5):
        if action == "run":
            if ap == 1:
                ap_1_sta = 1
            elif ap == 2:
                ap_2_sta = 2
            elif ap == 3:
                ap_3_sta = 3
            elif ap == 4:
                ap_4_sta = 3
        elif action == "sprint":
            if ap == 1:
                ap_1_sta = 3
            elif ap == 2:
                ap_2_sta = 4
            elif ap == 3:
                ap_3_sta = 7
            elif ap == 4:
                ap_4_sta = 7

    q_len = len(df) // 4
    q_rem = len(df) % 4

    ap_level_values = ['1AP'] * q_len + ['2AP'] * q_len + ['3AP'] * q_len + ['4AP'] * (q_len + q_rem)
    new_level_values = [f'{ap_1_sta}STA'] * q_len + [f'{ap_2_sta}STA'] * q_len + [f'{ap_3_sta}STA'] * q_len + [f'{ap_4_sta}STA'] * (q_len + q_rem)

    name = str.upper(action)
    df[name] = ap_level_values
    df['COST'] = new_level_values

    # Setting the new multi-index
    df.set_index(name, append=True, inplace=True)
    df.set_index('COST', append=True, inplace=True)

    # Reordering the index levels to have the new index on top
    df = df.reorder_levels([name, 'COST', df.index.name])

    # Transposing the DataFrame to switch rows and columns
    df = df.T

    def highlight_cells(value):
      ap_1_ms = 0
      ap_2_ms = 0
      ap_3_ms = 0
      ap_4_ms = 0

      for ap in range(1, 5):
          if action == "walk":
              if ap == 1:
                  ap_1_ms = ms // 4
              elif ap == 2:
                  ap_2_ms = ms // 2
              elif ap == 3:
                  ap_3_ms = ms // 4 + ms // 2
              elif ap == 4:
                  ap_4_ms = ms
          if action == "run":
              if ap == 1:
                  ap_1_ms = ms // 2
              elif ap == 2:
                  ap_2_ms = ms
              elif ap == 3:
                  ap_3_ms = ms + ms // 2
              elif ap == 4:
                  ap_4_ms = 2 * ms
          elif action == "sprint":
              if ap == 1:
                  ap_1_ms = ms
              elif ap == 2:
                  ap_2_ms = 2 * ms
              elif ap == 3:
                  ap_3_ms = 3 * ms
              elif ap == 4:
                  ap_4_ms = 4 * ms

      if value <= ap_1_ms:
          return f'background-color: {lgreen}'
      elif value <= ap_2_ms:
          return f'background-color: {dgreen}'
      elif value <= ap_3_ms:
          return f'background-color: {orange}'
      elif value <= ap_4_ms:
          return f'background-color: {red}'  
    
    return df.style.applymap(highlight_cells)

# ++++++++

def display_movement_matrix(init_ms = 15):
    tab1_content = widgets.Output()
    tab2_content = widgets.Output()
    tab3_content = widgets.Output()

    def display_movement_matrix(change):
        with tab1_content:
            clear_output(wait=True)
            display(movement_matrix(ms_slider.value, 'walk'))
        with tab2_content:
            clear_output(wait=True)
            display(movement_matrix(ms_slider.value, 'run'))
        with tab3_content:
            clear_output(wait=True)
            display(movement_matrix(ms_slider.value, 'sprint'))

    # Create Tab widgets
    tabs = widgets.Tab()

    # Set the titles and content for each tab
    tabs.children = [tab1_content, tab2_content, tab3_content]

    # Set tab titles
    tabs.set_title(0, 'WALK')
    tabs.set_title(1, 'RUN')
    tabs.set_title(2, 'SPRINT')

    # Create a slider for ms
    ms_slider = widgets.IntSlider(value=init_ms, min=1, max=20, description='ms')

    # Attach the slider's value change event to the function
    ms_slider.observe(display_movement_matrix, names='value')

    # Create a VBox layout for the slider and tabs
    slider_and_tabs = widgets.VBox([ms_slider, tabs])

    # Display the combined widget
    display_movement_matrix(None)
    display(slider_and_tabs)