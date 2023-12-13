import pandas as pd
from src import RaceAlignment, BodyType
from src.shared.client import GoogleSheetsClient


class CharacterBuilder:
    def __init__(self, props, test_mode=False):
        self.test_mode = test_mode

        self.init_google_sheets()
        self.init_base_stats()

        self.reset_character(props)

    def reset_character(self, props):
        self.set_props(props)
        self.init_budgets()
        self.init_build()
        self.recalculate()

    def set_props(self, props):
        # Raises KeyError if not all required keys are present or invalid
        self.name = props["name"]
        self.level = props["level"]
        self.body_type = props["body_type"]
        self.race = props["race"]
        self.alignment = props["alignment"]

    def init_google_sheets(self):
        self.client = GoogleSheetsClient(test_mode=self.test_mode)

    def init_base_stats(self):
        self.base_stats = self.client.get_dict("model", "base")

    def init_budgets(self):
        budgets_df = self.client.get_df("model", "budget")
        df_multiindex = budgets_df.set_index(["race", "alignment"])
        self.budget_table = df_multiindex

        self.constitution = int(
            self.budget_table.loc[(self.race, self.alignment), "constitution"]
        )
        self.competence = int(
            self.budget_table.loc[(self.race, self.alignment), "competence"]
        )
        self.development = int(
            self.budget_table.loc[(self.race, self.alignment), "development"]
        )

        self.constitution_budget = (
            self.base_stats["base_constitution_budget"]
            + 3 * (self.constitution - 1) * self.level
        )
        self.competence_budget = (
            self.base_stats["base_competence_budget"]
            + 3 * (self.competence - 1) * self.level
        )
        self.development_budget = (
            self.base_stats["base_development_budget"]
            + 3 * (self.development - 1) * self.level
        )

        self.remaining_constitution_budget = self.constitution_budget
        self.remaining_competence_budget = self.competence_budget
        self.remaining_development_budget = self.development_budget

    def init_build(self):
        self.traits = {}
        self.attributes = {}
        self.items = {}

        self.invalid_traits = {}
        self.invalid_attributes = {}
        self.invalid_items = {}

    def set_trait(self, trait, stacks):
        if trait.id not in self.traits:
            validation_result = self.validate_entity(trait)

            # If the dictionary is not empty, requirements are not met
            if validation_result:
                return False, validation_result

        # At this point, either the trait is new and requirements are met, or it's an existing trait
        self.traits[trait.id] = stacks
        self.recalculate()
        # if self.revalidate_build():
        #     return False, (
        #         self.invalid_traits,
        #         self.invalid_attributes,
        #         self.invalid_items,
        #     )

        return True, (trait, stacks, self.traits)

    def set_attribute(self, attribute, stacks):
        if attribute.id not in self.attributes:
            validation_result = self.validate_entity(attribute)

            # If the dictionary is not empty, requirements are not met
            if validation_result:
                return False, validation_result

        # At this point, either the trait is new and requirements are met, or it's an existing trait
        self.attributes[attribute.id] = stacks
        if self.revalidate_build():
            return False, (
                self.invalid_traits,
                self.invalid_attributes,
                self.invalid_items,
            )
        return True, (attribute, stacks, self.attributes)

    def set_item(self, item, count):
        if item.id not in self.items:
            validation_result = self.validate_entity(item)

            # If the dictionary is not empty, requirements are not met
            if validation_result:
                return False, validation_result

        # At this point, either the trait is new and requirements are met, or it's an existing trait
        self.items[item.id] = count
        return True, (item, count, self.items)

    def unset_trait(self, trait):
        if trait.id in self.traits:
            del self.traits[trait.id]
            if self.revalidate_build():
                return False, (
                    self.invalid_traits,
                    self.invalid_attributes,
                    self.invalid_items,
                )

            return True, (trait, self.traits)
        else:
            raise KeyError(f"Trait {trait.id} not found in character")

    def unset_attribute(self, attribute):
        if attribute.id in self.attributes:
            del self.attributes[attribute.id]
            if self.revalidate_build():
                return False, (
                    self.invalid_traits,
                    self.invalid_attributes,
                    self.invalid_items,
                )

            return True, (attribute, self.attributes)
        else:
            raise KeyError(f"Attribute {attribute.id} not found in character")

    def unset_item(self, item):
        if item.id in self.items:
            del self.items[item.id]
            return True, (item, self.items)
        else:
            raise KeyError(f"Item {item.id} not found in character")

    def validate_entity(self, entity):
        requirements = {}

        def check_requirement(key, current_value, requirement, is_numeric=True):
            if not requirement:
                return True  # Requirement not applicable

            if is_numeric:
                if current_value < requirement:
                    requirements[key] = requirement - current_value
                return current_value >= requirement
            else:
                if current_value not in requirement:
                    requirements[
                        key
                    ] = False  # Requirement not met (for non-numeric types)
                return current_value in requirement

        # TODO ADD Cap checks - check for preliminary calculations

        # Checking all requirements
        all_requirements_met = all(
            [
                check_requirement("req_level", self.level, entity.get("req_level")),
                check_requirement(
                    "req_race", self.race, entity.get("req_race"), is_numeric=False
                ),
                check_requirement(
                    "req_alignment",
                    self.alignment,
                    entity.get("req_alignment"),
                    is_numeric=False,
                ),
                check_requirement(
                    "req_body_type",
                    self.body_type,
                    entity.get("req_body_type"),
                    is_numeric=False,
                ),
                check_requirement(
                    "req_constitution",
                    self.constitution,
                    entity.get("req_constitution"),
                ),
                check_requirement(
                    "req_competence", self.competence, entity.get("req_competence")
                ),
                check_requirement(
                    "req_development", self.development, entity.get("req_development")
                ),
                check_requirement("req_int_gp", self.int_gp, entity.get("req_int_gp")),
                check_requirement("req_str_gp", self.str_gp, entity.get("req_str_gp")),
                check_requirement("req_dex_gp", self.dex_gp, entity.get("req_dex_gp")),
                check_requirement("req_tgh_gp", self.tgh_gp, entity.get("req_tgh_gp")),
                check_requirement("req_wis_gp", self.wis_gp, entity.get("req_wis_gp")),
                check_requirement("req_med_gp", self.med_gp, entity.get("req_med_gp")),
                check_requirement("req_sth_gp", self.sth_gp, entity.get("req_sth_gp")),
                check_requirement("req_per_gp", self.per_gp, entity.get("req_per_gp")),
                check_requirement(
                    "req_dodge_cp", self.dodge_cp, entity.get("req_dodge_cp")
                ),
                check_requirement(
                    "req_block_cp", self.block_cp, entity.get("req_block_cp")
                ),
                check_requirement("req_mma_cp", self.mma_cp, entity.get("req_mma_cp")),
                check_requirement(
                    "req_finesse_cp", self.finesse_cp, entity.get("req_finesse_cp")
                ),
                check_requirement(
                    "req_crude_cp", self.crude_cp, entity.get("req_crude_cp")
                ),
                check_requirement(
                    "req_archery_cp", self.archery_cp, entity.get("req_archery_cp")
                ),
                check_requirement(
                    "req_firearms_cp", self.firearms_cp, entity.get("req_firearms_cp")
                ),
                check_requirement(
                    "req_thrown_cp", self.thrown_cp, entity.get("req_thrown_cp")
                ),
                check_requirement(
                    "req_bite_cp", self.bite_cp, entity.get("req_bite_cp")
                ),
                check_requirement(
                    "req_claw_cp", self.claw_cp, entity.get("req_claw_cp")
                ),
                check_requirement(
                    "req_swipe_cp", self.swipe_cp, entity.get("req_swipe_cp")
                ),
                check_requirement(
                    "req_sting_cp", self.sting_cp, entity.get("req_sting_cp")
                ),
            ]
        )

        return requirements if not all_requirements_met else {}

    def revalidate_build(self):
        self.recalculate()

        changes_made = True
        while changes_made:
            changes_made = False  # Reset flag for each iteration

            # Attempt to revalidate previously invalid traits, attributes, and items
            for entity_dict, invalid_dict in [
                (self.traits, self.invalid_traits),
                (self.attributes, self.invalid_attributes),
                (self.items, self.invalid_items),
            ]:
                for entity_id in list(invalid_dict.keys()):
                    if self.validate_entity(invalid_dict[entity_id]):
                        entity_dict[entity_id] = invalid_dict.pop(entity_id)
                        changes_made = True

            # Check current traits, attributes, and items for validity
            for entity_dict, invalid_dict in [
                (self.traits, self.invalid_traits),
                (self.attributes, self.invalid_attributes),
                (self.items, self.invalid_items),
            ]:
                for entity_id, entity in list(entity_dict.items()):
                    if not self.validate_entity(entity):
                        invalid_dict[entity_id] = entity_dict.pop(entity_id)
                        changes_made = True

            is_invalid = (
                self.invalid_traits or self.invalid_attributes or self.invalid_items
            )
            return is_invalid

    def recalculate(self):
        self.reload_build_pool()
        self.reload_unit_prices()
        self.recalculate_budgets()
        self.recalculate_modifiers()
        self.recalculate_stats()
        self.recalculate_caps()

    def reload_build_pool(self):
        self.traits_pool = self.client.get_df(
            "model",
            "traits",
            tuple_columns=["abilities"],
            list_columns=["req_race", "req_alignment", "req_body_type", "skills"],
        )
        self.attributes_pool = self.client.get_df(
            "model",
            "attributes",
            tuple_columns=["abilities"],
            list_columns=["req_race", "req_alignment", "req_body_type", "skills"],
        )
        self.items_pool = self.client.get_df(
            "model",
            "items",
            tuple_columns=["abilities"],
            list_columns=["req_race", "req_alignment", "req_body_type", "skills"],
        )
        self.skills = self.client.get_df("model", "skills")
        self.abilities = self.client.get_df("model", "abilities")

    def reload_unit_prices(self):
        # Retrieve the latest values
        self.requirement_values = self.client.get_dict("model", "requirements")
        self.modifier_values = self.client.get_dict("model", "modifiers")
        self.combat_values = self.client.get_dict("model", "combat")

        excluded_keys = [
            "req_level",
            "req_race",
            "req_alignment",
            "req_body_type",
            "req_body_part",
            "com_rel_cp",
        ]

        # Recalculate unit prices for each pool
        for pool in (self.traits_pool, self.attributes_pool, self.items_pool):
            # Initialize a list to store total values
            total_values = []

            for entity_id, entity in pool.iterrows():
                # Initialize the total value for this entity
                total_value = 0

                # Iterate through all keys and values in the entity
                for key, value in entity.items():
                    if key not in excluded_keys and (
                        key.startswith("req_")
                        or key.startswith("mod_")
                        or key.startswith("com_")
                    ):
                        value = float(value or 0)
                        total_value += value * self.requirement_values.get(key, 0)
                        total_value += value * self.modifier_values.get(key, 0)
                        total_value += value * self.combat_values.get(key, 0)

                # Append the total value to the list
                total_values.append(total_value)

            # Add the total values as a new column to the DataFrame
            pool["value"] = total_values

    def recalculate_budgets(self):
        try:
            # Calculate the constitution budget cost for traits
            constitution_budget_cost = sum(
                self.traits_pool[self.traits_pool["id"] == trait_id]["value"] * count
                for trait_id, count in self.traits.items()
            )
            # Subtract the cost from the constitution budget
            self.remaining_constitution_budget = (
                self.constitution_budget - constitution_budget_cost
            )

            # Calculate the competence budget cost for attributes
            competence_budget_cost = sum(
                self.attributes_pool[attribute_id]["value"] * count
                for attribute_id, count in self.attributes.items()
            )
            # Subtract the cost from the competence budget
            self.remaining_competence_budget = (
                self.competence_budget - competence_budget_cost
            )

            # Calculate the development budget cost for items
            development_budget_cost = sum(
                self.items_pool[item_id]["value"] * count
                for item_id, count in self.items.items()
            )
            # Subtract the cost from the development budget
            self.remaining_development_budget = (
                self.development_budget - development_budget_cost
            )

        except KeyError as e:
            raise ValueError(f"Key {e} not found in the corresponding pool.")

    def recalculate_caps(self):
        self.hp_cap = self.base_stats["base_hp_cap"] + self.level
        self.sta_cap = self.base_stats["base_stamina_cap"] + self.level

        self.ms_cap = (
            self.base_stats["base_ms_cap"]
            + self.level // 2
            + self.modifiers.get("mod_ms_cap", 0)
        )
        self.cp_cap = (
            self.base_stats["base_cp_cap"]
            + self.level // 2
            + self.modifiers.get("mod_gp_cap", 0)
        )
        self.gp_cap = (
            self.base_stats["base_gp_cap"]
            + self.level // 2
            + self.modifiers.get("mod_cp_cap", 0)
        )

    def recalculate_modifiers(self):
        self.modifiers = {}

        # Helper function to process each entity
        def process_entity(entity_id, stacks, pool):
            # Find the row where id matches
            entity_data = pool[pool["id"] == entity_id].iloc[0]
            for key, value in entity_data.items():
                if key.startswith("mod_") and value:
                    if key in self.modifiers:
                        self.modifiers[key] += stacks
                    else:
                        self.modifiers[key] = stacks

        # Process traits
        for trait_id, stacks in self.traits.items():
            process_entity(trait_id, stacks, self.traits_pool)

        # Process attributes
        for attribute_id, stacks in self.attributes.items():
            process_entity(attribute_id, stacks, self.attributes_pool)

    def recalculate_stats(self):
        # gps - general proficiencies

        self.int_gp = self.modifiers.get("mod_int_gp", 0)
        self.str_gp = self.modifiers.get("mod_str_gp", 0)
        self.dex_gp = self.modifiers.get("mod_dex_gp", 0)
        self.tgh_gp = self.modifiers.get("mod_tgh_gp", 0)
        self.wis_gp = self.modifiers.get("mod_wis_gp", 0)
        self.med_gp = self.modifiers.get("mod_med_gp", 0)
        self.sth_gp = self.modifiers.get("mod_sth_gp", 0)
        self.per_gp = self.modifiers.get("mod_per_gp", 0)

        # cps - combat proficiencies

        self.dodge_cp = self.modifiers.get("mod_dodge_cp", 0)
        self.block_cp = self.modifiers.get("mod_block_cp", 0)
        self.mma_cp = self.modifiers.get("mod_mma_cp", 0)
        self.crude_cp = self.modifiers.get("mod_crude_cp", 0)
        self.finesse_cp = self.modifiers.get("mod_finesse_cp", 0)
        self.archery_cp = self.modifiers.get("mod_archery_cp", 0)
        self.firearms_cp = self.modifiers.get("mod_firearms_cp", 0)
        self.thrown_cp = self.modifiers.get("mod_thrown_cp", 0)
        self.bite_cp = self.modifiers.get("mod_bite_cp", 0)
        self.claw_cp = self.modifiers.get("mod_claw_cp", 0)
        self.swipe_cp = self.modifiers.get("mod_swipe_cp", 0)
        self.sting_cp = self.modifiers.get("mod_sting_cp", 0)

        # general stats

        self.ms = self.base_stats["base_ms"] + self.modifiers.get("mod_ms", 0)
        self.stamina = self.base_stats["base_stamina"] + self.modifiers.get(
            "mod_stamina", 0
        )
        self.composure = (
            self.base_stats["base_composure"]
            + self.level
            + self.modifiers.get("mod_composure", 0)
        )

        self.evasion = self.dodge_cp // 2 + self.modifiers.get("mod_evasion", 0)
        self.protection = self.block_cp // 2 + self.modifiers.get("mod_protection", 0)
        self.wrestling = self.mma_cp // 2 + self.modifiers.get("mod_wrestling", 0)

        # body stats

        self.total_hp = (
            self.base_stats["base_hp"]
            + 6 * self.level
            + 3 * self.modifiers.get("mod_total_hp_incr", 0)
        )
        self.body_phys_res = self.modifiers.get("mod_body_phys_res", 0)
        self.body_elem_res = self.modifiers.get("mod_body_elem_res", 0)

    def recalculate_caps(self):
        self.hp_cap = self.base_stats["base_hp_cap"] + self.level
        self.sta_cap = self.base_stats["base_sta_cap"] + self.level

        self.ms_cap = (
            self.base_stats["base_ms_cap"]
            + self.level // 2
            + self.modifiers.get("mod_ms_cap", 0)
        )
        self.cp_cap = (
            self.base_stats["base_cp_cap"]
            + self.level // 2
            + self.modifiers.get("mod_gp_cap", 0)
        )
        self.gp_cap = (
            self.base_stats["base_gp_cap"]
            + self.level // 2
            + self.modifiers.get("mod_cp_cap", 0)
        )

    def recalculate_combat_stats(self):
        pass

    def upload_character(self, sheet_name, worksheet_name):
        if not self.revalidate_build():
            # TODO: Upload character to Google Sheets

            pass

            character_config = {}

            character_config_df = pd.DataFrame(character_config)

            self.client.update_worksheet(
                sheet_name, worksheet_name, character_config_df
            )
