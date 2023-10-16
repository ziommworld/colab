import ipywidgets as widgets
from IPython.display import display

class ActionStorage:
    def __init__(self):
        self.actions = []

    def add_action(self, ap, movement, stamina_cost):
        self.actions.append({'AP': ap, 'Movement': movement, 'Stamina Cost': stamina_cost})

    def remove_last_action(self):
        if self.actions:
            return self.actions.pop()

    def clear_actions(self):
        self.actions = []

    def get_actions(self):
        return self.actions

storage = ActionStorage()

turn_counter = 1
current_AP = 4
last_turn_AP = 0
stamina = None
consecutive_passes = 0

turn_label = widgets.Label(value=f"Turn: {turn_counter}")

stamina_slider = widgets.IntSlider(
    value=10,
    min=1,
    max=20,
    step=1,
    description='Init STA:',
    disabled=False,
    continuous_update=False,
    orientation='horizontal',
    readout=True,
    readout_format='d'
)

start_game_btn = widgets.Button(description="Start Game", disabled=False, button_style='info')
tabs = widgets.Tab(children=[widgets.Output() for _ in range(20)])
for i in range(20):
    tabs.set_title(i, str(i+1))

end_round_btn = widgets.Button(description="End Round", disabled=True, button_style='danger')
reset_game_btn = widgets.Button(description="Reset Game", disabled=True)

ap_toggle = widgets.ToggleButtons(
    options=['1AP', '2AP', '3AP', '4AP'],
    description='AP:',
    value=None,
    disabled=True,
)

movement_toggle = widgets.ToggleButtons(
    options=['Walk', 'Run', 'Sprint'],
    description='Movement:',
    value=None,
    disabled=True
)

do_action_btn = widgets.Button(description="Do Action", disabled=True, button_style='success')
undo_action_btn = widgets.Button(description="Undo Action", disabled=True, button_style='warning')
action_dropdown = widgets.Dropdown(description="Actions:", disabled=True)

def compute_stamina_cost(ap, action):
    action = action.lower()
    ap_sta_map = {
        "run": {
            '1AP': 1,
            '2AP': 2,
            '3AP': 3,
            '4AP': 3
        },
        "sprint": {
            '1AP': 3,
            '2AP': 4,
            '3AP': 7,
            '4AP': 7
        }
    }
    return ap_sta_map.get(action, {}).get(ap, 0)

def compute_ap_stamina_penalty():
    if (4 - current_AP) + last_turn_AP == 7:
        return 1
    elif (4 - current_AP) + last_turn_AP == 8:
        return 2
    return 0

def update_ap_buttons():
    global current_AP
    valid_options = [f"{i}AP" for i in range(1, current_AP + 1)]
    ap_toggle.options = valid_options
    ap_toggle.value = None
    if current_AP == 0:
        ap_toggle.disabled = True
        movement_toggle.disabled = True
    else:
        ap_toggle.disabled = False
        movement_toggle.disabled = False

def do_action(change):
    global current_AP, last_turn_AP, stamina
    if ap_toggle.value and movement_toggle.value:
        stamina_cost_action = compute_stamina_cost(ap_toggle.value, movement_toggle.value)
        stamina_cost_ap = compute_ap_stamina_penalty()
        total_stamina_cost = stamina_cost_action + stamina_cost_ap

        if stamina - total_stamina_cost >= 0:
            stamina -= total_stamina_cost
            current_AP -= int(ap_toggle.value[0])
            storage.add_action(ap_toggle.value, movement_toggle.value, total_stamina_cost)
            actions = [f"{action['Movement']} - {action['AP']} / {action['Stamina Cost']} STA" for action in storage.get_actions()]
            action_dropdown.options = actions
            action_dropdown.value = actions[-1]
            update_ap_buttons()
            movement_toggle.value = None
        else:
            with tabs.children[turn_counter - 1]:
                print("Not enough stamina!")

do_action_btn.on_click(do_action)

def undo_action(change):
    global current_AP, stamina
    last_action = storage.remove_last_action()
    if last_action:
        current_AP += int(last_action['AP'][0])
        stamina += last_action['Stamina Cost']
        actions = [f"{action['Movement']} - {action['AP']} / {action['Stamina Cost']} STA" for action in storage.get_actions()]
        action_dropdown.options = actions
        update_ap_buttons()

undo_action_btn.on_click(undo_action)

progress_bar = widgets.IntProgress(
    value=1,
    min=1,
    max=20,
    step=1,
    description='Round: 1/20',
    bar_style='info',
    orientation='horizontal'
)

def end_round(change):
    global turn_counter, current_AP, last_turn_AP, stamina, consecutive_passes
    total_stamina_spent = sum([action['Stamina Cost'] for action in storage.get_actions()])
    total_ap_played = sum([int(action['AP'][0]) for action in storage.get_actions()])
    stamina_penalty = compute_ap_stamina_penalty()

    if total_ap_played == 0:
        consecutive_passes += 1
        if consecutive_passes == 1:
            stamina = min(stamina + 1, stamina_slider.value)
            rest_stamina = 1
        elif consecutive_passes > 1:
            stamina = min(stamina + 2, stamina_slider.value)
            rest_stamina = 2
        else:
            rest_stamina = 0
    else:
        consecutive_passes = 0
        rest_stamina = 0

    with tabs.children[turn_counter - 1]:
        print(f"Turn {turn_counter}:\n")
        for action in storage.get_actions():
            print(f"{action['Movement']} - {action['AP']} / {action['Stamina Cost']} STA")
        print(f"\nTotal AP Played: {total_ap_played}")
        print(f"Stamina Penalty: {stamina_penalty}")
        print(f"Stamina from Rest: {rest_stamina}")
        print(f"Total Stamina Spent: {total_stamina_spent + stamina_penalty}")
        print(f"Remaining Stamina: {stamina}\n")

    storage.clear_actions()
    action_dropdown.options = []
    last_turn_AP = 4 - current_AP
    current_AP = 4
    update_ap_buttons()
    progress_bar.value = turn_counter
    progress_bar.description = f'Round: {turn_counter+1}/20'
    turn_counter += 1
    turn_label.value = f"Turn: {turn_counter}"

end_round_btn.on_click(end_round)

def start_game(change):
    global stamina
    stamina = stamina_slider.value
    stamina_slider.disabled = True
    start_game_btn.disabled = True
    ap_toggle.disabled = False
    movement_toggle.disabled = False
    do_action_btn.disabled = False
    undo_action_btn.disabled = False
    action_dropdown.disabled = False
    end_round_btn.disabled = False
    reset_game_btn.disabled = False
    update_ap_buttons()

start_game_btn.on_click(start_game)

def reset_game(change):
    global turn_counter, current_AP, last_turn_AP, stamina, consecutive_passes
    turn_counter = 1
    current_AP = 4
    last_turn_AP = 0
    stamina = stamina_slider.value
    consecutive_passes = 0
    turn_label.value = f"Turn: {turn_counter}"
    storage.clear_actions()
    action_dropdown.options = []
    stamina_slider.disabled = False
    start_game_btn.disabled = False
    ap_toggle.disabled = True
    movement_toggle.disabled = True
    do_action_btn.disabled = True
    undo_action_btn.disabled = True
    action_dropdown.disabled = True
    end_round_btn.disabled = True
    reset_game_btn.disabled = True
    for i in range(20):
        tabs.children[i].clear_output()
    with tabs.children[0]:
        print("Game Reset!")

reset_game_btn.on_click(reset_game)

row_2 = widgets.HBox([stamina_slider, start_game_btn, progress_bar])
row_3 = widgets.HBox([ap_toggle])
row_4 = widgets.HBox([movement_toggle])
col_34 = widgets.VBox([row_3, row_4])
col_5 = widgets.VBox([do_action_btn, undo_action_btn, end_round_btn, action_dropdown])
row_345 = widgets.HBox([col_5, col_34])
row_7 = widgets.HBox([tabs])

display(row_2, row_345, row_7)
