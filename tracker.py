import ipywidgets as widgets
from IPython.display import display


def display_tracker():
    class ActionStorage:
        def __init__(self):
            self.actions = []

        def add_action(self, action, ap, ms, sta, att, dmg):
            self.actions.append(
                {
                    "ACTION": action,
                    "AP": ap,
                    "MS": ms,
                    "STA": sta,
                    "ATT": att,
                    "DMG": dmg,
                }
            )

        def remove_action_by_index(self, index):
            if 0 <= index < len(self.actions):
                return self.actions.pop(index)
            else:
                raise IndexError("Invalid index")

        def clear_actions(self):
            self.actions = []

        def get_actions(self):
            return self.actions[::-1]

    actions = ActionStorage()

    turn_counter = 1
    current_AP = 4
    last_turn_AP = 0
    init_sta = 10
    sta = None
    ms = None
    consecutive_passes = 0

    turn_label = widgets.Label(value=f"Turn: {turn_counter}")

    sta_slider = widgets.IntSlider(
        value=init_sta,
        min=1,
        max=20,
        step=1,
        description="STA:",
        continuous_update=False,
        orientation="horizontal",
    )

    ms_slider = widgets.IntSlider(
        value=10,
        min=1,
        max=20,
        step=1,
        description="MS:",
        continuous_update=False,
        orientation="horizontal",
    )

    def update_sta_from_slider(change):
        global sta
        sta = change.new

    sta_slider.observe(update_sta_from_slider, names="value")

    start_game_btn = widgets.Button(
        description="Start Game", disabled=False, button_style="info"
    )
    tabs = widgets.Tab(children=[widgets.Output() for _ in range(20)])
    for i in range(20):
        tabs.set_title(i, str(i + 1))

    end_round_btn = widgets.Button(
        description="End Round", disabled=True, button_style="danger"
    )
    reset_game_btn = widgets.Button(description="Reset Game", disabled=True)

    ap_toggle = widgets.ToggleButtons(
        options=["1AP", "2AP", "3AP", "4AP"],
        description="AP:",
        value=None,
        disabled=True,
    )

    actions_toggle = widgets.ToggleButtons(
        options=[
            "M_Walk",
            "M_Run",
            "M_Sprint",
            "A_Quick",
            "A_Normal",
            "A_Steady",
            "A_Charged",
            "A_Dual",
        ],
        description="Action:",
        value=None,
        disabled=True,
    )

    def update_ap_options(change):
        selected_action = change.new
        if selected_action:
            all_valid_ap_options = (
                list(ap_sta_map[selected_action].keys())
                if selected_action in ap_sta_map
                else ["1AP", "2AP", "3AP", "4AP"]
            )

            # Filtering based on current_AP
            valid_ap_options = [
                ap for ap in all_valid_ap_options if int(ap[0]) <= current_AP
            ]

            # If there are no valid options, disable the AP toggle
            if not valid_ap_options:
                ap_toggle.options = []
                ap_toggle.value = None
                ap_toggle.disabled = True
            else:
                ap_toggle.options = valid_ap_options
                ap_toggle.value = None  # Reset the value
                ap_toggle.disabled = False
        else:
            ap_toggle.options = []
            ap_toggle.value = None
            ap_toggle.disabled = True

    actions_toggle.observe(update_ap_options, names="value")

    do_action_btn = widgets.Button(
        description="Do Action", disabled=True, button_style="success"
    )
    undo_action_btn = widgets.Button(
        description="Undo Action", disabled=True, button_style="warning"
    )
    action_dropdown = widgets.Dropdown(description="Actions:", disabled=True)
    action_dropdown.layout.width = "750px"

    ap_sta_map = {
        "M_Walk": {"1AP": 0, "2AP": 0, "3AP": 0, "4AP": 0},
        "M_Run": {"1AP": 1, "2AP": 2, "3AP": 3, "4AP": 3},
        "M_Sprint": {"1AP": 3, "2AP": 4, "3AP": 7, "4AP": 7},
        "A_Quick": {"2AP": 1},
        "A_Normal": {"3AP": 1},
        "A_Steady": {"4AP": 1},
        "A_Charged": {"3AP": 1},
        "A_Dual": {"3AP": 2},
    }

    def compute_stamina_cost(ap, action):
        return ap_sta_map.get(action, {}).get(ap, 0)

    def compute_ms(ap, action):
        sta_penalty = compute_stamina_penalty()
        sta_ms_penalty = sta_penalty.get("MS", 0) if sta_penalty else 0
        ms_x = ms - sta_ms_penalty

        for ap in range(1, 5):
            if action == "M_Walk":
                if ap == 1:
                    return ms_x // 4
                elif ap == 2:
                    return ms_x // 2
                elif ap == 3:
                    return ms_x // 4 + ms_x // 2
                elif ap == 4:
                    return ms_x
            if action == "M_Run":
                if ap == 1:
                    return ms_x // 2
                elif ap == 2:
                    return ms_x
                elif ap == 3:
                    return ms_x + ms_x // 2
                elif ap == 4:
                    return 2 * ms_x
            elif action == "M_Sprint":
                if ap == 1:
                    return ms_x
                elif ap == 2:
                    return 2 * ms_x
                elif ap == 3:
                    return 3 * ms_x
                elif ap == 4:
                    return 4 * ms_x

    def compute_damage_modifier(action):
        dmg_map = {
            "A_Quick": -6,
            "A_Charged": 6,
        }
        return dmg_map.get(action, 0)

    def compute_attack_rating(action):
        att_map = {"A_Quick": -1, "A_Steady": 2, "A_Charged": -1, "A_Dual": -2}

        sta_penalty = compute_stamina_penalty()
        att_penalty = sta_penalty.get(action, 0) if sta_penalty else 0
        att_x = att_map.get(action, 0) - att_penalty
        return att_x

    def compute_ap_penalty():
        this_turn_AP = 4 - current_AP
        if this_turn_AP + last_turn_AP == 7:
            return {"STA": 1}
        elif this_turn_AP + last_turn_AP == 8:
            return {"STA": 2}
        return None

    def compute_stamina_penalty():
        if sta == 5:
            return {"MS": 1, "ATT": 1}
        elif sta == 3:
            return {"MS": 2, "ATT": 2}
        elif sta == 1:
            return {"MS": 3, "ATT": 3}

    def update_ap_buttons():
        nonlocal current_AP

        # Determine which buttons to show based on current_AP
        valid_options = (
            [f"{i}AP" for i in range(1, current_AP + 1)] if current_AP > 0 else []
        )

        # If there are no valid options, disable the toggle and clear its options
        if not valid_options:
            ap_toggle.disabled = True
            actions_toggle.disabled = True
            ap_toggle.options = []
            ap_toggle.value = None  # Reset the value
        else:
            ap_toggle.options = valid_options
            ap_toggle.disabled = False
            actions_toggle.disabled = False
            ap_toggle.value = valid_options[
                0
            ]  # Reset the value to the first valid option

    def do_action(change):
        nonlocal current_AP, last_turn_AP, sta, actions
        if ap_toggle.value and actions_toggle.value:
            stamina_cost_action = compute_stamina_cost(
                ap_toggle.value, actions_toggle.value
            )
            stamina_cost_ap = (
                compute_ap_penalty().get("STA", 0) if compute_ap_penalty() else 0
            )
            total_stamina_cost = stamina_cost_action + stamina_cost_ap

            if sta - total_stamina_cost >= 0:
                ms = compute_ms(ap_toggle.value, actions_toggle.value)
                ms_slider.value = ms

                sta -= total_stamina_cost
                sta_slider.value = sta
                current_AP -= int(ap_toggle.value[0])
                att = compute_attack_rating(actions_toggle.value)
                dmg = compute_damage_modifier(actions_toggle.value)

                actions.add_action(
                    actions_toggle.value,
                    ap_toggle.value,
                    ms,
                    total_stamina_cost,
                    att,
                    dmg,
                )
                options = [
                    f"[{action['ACTION']}] {action['AP']} | STA: {action['STA']} | MS: {action['MS']} | ATT: {action['ATT']} | DMG: {action['DMG']}"
                    for action in actions.get_actions()
                ]
                action_dropdown.options = options
                action_dropdown.value = options[0]
                update_ap_buttons()
                actions_toggle.value = None
                ap_toggle.value = None
            else:
                # with tabs.children[turn_counter - 1]:
                print("Not enough stamina!")

    do_action_btn.on_click(do_action)

    def undo_action(change):
        nonlocal current_AP, sta

        # 1. Get the currently selected value from the dropdown
        selected_value = action_dropdown.value

        # 2. Find its index in the dropdown options
        try:
            action_index = list(action_dropdown.options).index(selected_value)
        except ValueError:
            # Selected value not in the dropdown options
            return

        # 3. Pass that index to remove_action_by_index
        removed_action = actions.remove_action_by_index(action_index)

        if removed_action:
            current_AP += int(removed_action["AP"][0])
            sta += removed_action["STA"]
            sta_slider.value = sta

            action_options = [
                f"[{action['ACTION']}] {action['AP']} | STA:{action['STA']} | MS:{action['MS']} | ATT:{action['ATT']} | DMG:{action['DMG']}"
                for action in actions.get_actions()
            ]
            action_dropdown.options = action_options
            update_ap_buttons()

    undo_action_btn.on_click(undo_action)

    progress_bar = widgets.IntProgress(
        value=1,
        min=1,
        max=20,
        step=1,
        description="Round: 1/20",
        bar_style="info",
        orientation="horizontal",
    )

    def end_round(change):
        nonlocal turn_counter, current_AP, last_turn_AP, sta, consecutive_passes
        total_stamina_spent = sum([action["STA"] for action in actions.get_actions()])
        total_ap_played = sum(
            [int(action["AP"][0]) for action in actions.get_actions()]
        )

        ap_penalty = compute_ap_penalty()
        ap_sta_penalty = ap_penalty.get("STA", 0) if ap_penalty else 0

        sta_penalty = compute_stamina_penalty()
        sta_att_penalty = sta_penalty.get("ATT", 0) if sta_penalty else 0
        sta_ms_penalty = sta_penalty.get("MS", 0) if sta_penalty else 0

        if total_ap_played == 0:
            consecutive_passes += 1
            if consecutive_passes == 1:
                sta = min(sta + 1, init_sta)
                sta_slider.value = sta
                rest_stamina = 1
            elif consecutive_passes > 1:
                sta = min(sta + 2, init_sta)
                sta_slider.value = sta
                rest_stamina = 2
            else:
                rest_stamina = 0
        else:
            consecutive_passes = 0
            rest_stamina = 0

        with tabs.children[turn_counter - 1]:
            print(f"Turn {turn_counter}:\n")
            print(f"Start stamina: {sta_slider.value}")
            for action in actions.get_actions():
                print(
                    f"[{action['ACTION']}] AP:{action['AP']} | STA:{action['STA']} | MS:{action['MS']} | ATT:{action['ATT']} | DMG:{action['DMG']}"
                )
            print(f"\nTotal AP Played: {total_ap_played}")
            print(f"Stamina Penalty: {ap_sta_penalty}")
            print(f"MS Penalty next round: {sta_ms_penalty}")
            print(f"ATT Penalty next round: {sta_att_penalty}")
            print(f"Stamina from Rest: {rest_stamina}")
            print(f"Total Stamina Spent: {total_stamina_spent + ap_sta_penalty}")
            print(f"Remaining Stamina: {sta}\n")

        sta_slider.value = sta
        actions.clear_actions()
        action_dropdown.options = []
        last_turn_AP = 4 - current_AP
        current_AP = 4
        update_ap_buttons()
        progress_bar.value = turn_counter
        progress_bar.description = f"Round: {turn_counter+1}/20"
        turn_counter += 1
        tabs.selected_index = turn_counter - 2

    end_round_btn.on_click(end_round)

    def start_game(change):
        nonlocal sta, ms
        sta = sta_slider.value
        ms = ms_slider.value
        start_game_btn.disabled = True
        ap_toggle.disabled = False
        actions_toggle.disabled = False
        do_action_btn.disabled = False
        undo_action_btn.disabled = False
        action_dropdown.disabled = False
        end_round_btn.disabled = False
        reset_game_btn.disabled = False
        update_ap_buttons()

    start_game_btn.on_click(start_game)

    def reset_game(change):
        nonlocal turn_counter, current_AP, last_turn_AP, sta, consecutive_passes
        turn_counter = 1
        current_AP = 4
        last_turn_AP = 0
        sta = sta_slider.value

        consecutive_passes = 0
        actions.clear_actions()
        action_dropdown.options = []
        sta_slider.disabled = False
        start_game_btn.disabled = False
        ap_toggle.disabled = True
        actions_toggle.disabled = True
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

    col_0 = widgets.VBox([sta_slider, ms_slider])
    col_1 = widgets.VBox([start_game_btn, progress_bar])
    row_2 = widgets.HBox([col_0, col_1])
    row_3 = widgets.HBox([ap_toggle])
    row_4 = widgets.HBox([actions_toggle])
    col_34 = widgets.VBox([row_4, row_3])
    col_5 = widgets.VBox(
        [do_action_btn, undo_action_btn, end_round_btn, action_dropdown]
    )
    row_345 = widgets.HBox([col_5, col_34])
    row_7 = widgets.HBox([tabs])

    display(row_2, row_345, row_7)


