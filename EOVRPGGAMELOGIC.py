class Item:
    def __init__(self, name, item_type, effect_value):
        self.name = name
        self.abbreviation = name[:2].upper()
        self.item_type = item_type  # "heal", "stamina", "both", "boost", "damage"
        self.effect_value = effect_value  # Value of the effect
    @classmethod
    def get_items(cls):
        return [
            cls("Asparagus Pea Medley ", "heal", 15),
            cls("Tiny Meat ", "damage", 3),
            cls("Medium Meat ", "damage", 5),
            cls("Large Meat ", "damage", 7),
            cls("Frostbitten ", "heal", 22),
            cls("Carrot Delight", "heal", 10),
            cls("Pea Salad", "heal", 8),
            cls("Asparagus Medley", "heal", 12),
            cls("Fusion", "heal", 9),
            cls("Radish Medley", "heal", 6),
            cls("Kale Bowl", "heal", 8),
            cls("Carrot", "heal", 8),
            cls("Peas", "heal", 8),
            cls("Asparagus", "heal", 8),
            cls("Broccoli", "heal", 8),
            cls("Radish", "heal", 8),
            cls("Kale", "heal", 8),

            cls("Meat Skewers", "heal", 18),
            cls("Mmedium Meat & Frosted Kale Salad", "heal", 30),
            cls("Tiny Meat Stir", "heal", 16),
            cls("R Tiny Meat", "heal", 5),
            cls("R Medium Meat", "heal", 10),
            cls("R Large Meat", "heal", 15),

            cls("Carrot", "heal", 8),
            cls("Pea", "heal", 5),
            cls("Asparagus", "heal", 10),
            cls("Broccoli", "heal", 6),
            cls("Radish", "heal", 8),
            cls("Kale", "heal", 9),

            cls("Healing Wraps", "remove_status", 35),  # Heals 20 HP
            cls("Spore Balm", "remove_status", 30),
            cls("Stamina Potion", "stamina", 15),  # Restores 15 stamina
            cls("Rage-Fused Binding", "boost", 15),
            cls("Adrenaline Bar", "boost", 10),  # Boosts damage by 5
            cls("Inferno Shard", "boost", 25),
            cls("Poison Gas", "damage", 10),  # Deals 10 damage to a target
            cls("Purification Crystal", "cure_status", 0),  # Removes all status effects
            
            cls("Lifespark Glyph", "heal", 999),
            cls("Etheric Infusion", "full_restore", 999),  # Fully restores HP and stamina
            cls("Embercool Salve", "remove_status", 25)
            ]

    def use(self, target):
        if self.item_type == "remove_status":
                # Define which effects each item can remove
                effect_removers = {
                    "Healing Wraps": "bleeding",
                    "Spore Balm": "poison",
                    "Embercool Salve": "burn"
                }
                
                effect_to_remove = effect_removers.get(self.name)
                if effect_to_remove:  # Only proceed if we have a valid effect to remove
                    if effect_to_remove in target.status_effects:
                        target.status_effects.remove(effect_to_remove)
                        print(f"{target.name} uses {self.name} and removes the {effect_to_remove} status effect!")
                    else:
                        print(f"{target.name} doesn't have {effect_to_remove} status effect!")
                else:
                    print(f"{self.name} cannot remove any status effects!")
                    return

        if self.item_type == "protection":
            target.protection += self.effect_value
            print(f"{target.name} uses {self.name} and gains {self.effect_value} protection!")
        
        elif self.item_type == "full_restore":
            target.health = target.max_health
            target.stamina = target.max_stamina
            print(f"{target.name} uses {self.name} and fully restores all stats!")
            
        elif self.item_type == "cure_status":
            target.status_effects.clear()
            print(f"{target.name} uses {self.name} and removes all status effects!")
            
        elif self.item_type == "full_heal":
            target.health = target.max_health
            print(f"{target.name} uses {self.name} and fully restores HP!")
            
        elif self.item_type == "full_stamina":
            target.stamina = target.max_stamina
            print(f"{target.name} uses {self.name} and fully restores stamina!")
            
        elif self.item_type == "heal":
            target.health = min(target.max_health, target.health + self.effect_value)
            print(f"{target.name} uses {self.name} and heals {self.effect_value} HP!")
            
        elif self.item_type == "stamina":
            target.stamina = min(target.stamina + self.effect_value, target.max_stamina)  # Updated
            print(f"{target.name} uses {self.name} and recovers {self.effect_value} stamina!")

        elif self.item_type == "both":
            target.health = min(target.max_health, target.health + self.effect_value[0])
            target.stamina = min(target.stamina + self.effect_value[1], target.max_stamina)  # Updated
            print(f"{target.name} uses {self.name} and heals {self.effect_value[0]} HP and recovers {self.effect_value[1]} stamina!")

        elif self.item_type == "boost":
            target.temp_damage += self.effect_value
            print(f"{target.name} uses {self.name} and temporarily increases their damage by {self.effect_value}!")

        elif self.item_type == "damage":
            target.health -= self.effect_value
            print(f"{target.name} uses {self.name} and takes {self.effect_value} damage!")


        status_effects = ','.join(target.status_effects) if target.status_effects else "None"
        print(f"{target.name},{target.max_health},{target.health},{target.stamina},{target.max_stamina},{target.luck},{target.protection},{target.light},{target.damage},{status_effects}")

class Battle:
    def __init__(self, players):
        self.players = players
        self.creatures = []
        self.current_creature_index = 0  # Track which creature is currently active
        self.total_drops = {}  # To store total drops from this battle
        self.total_exp = 0  # To store total experience gained in this battle
        self.items_used = {}
        self.temp_boosts = {
            player.name: {
                'damage': 0,
                'protection': 0,
                'turns_remaining': 0
            } for player in players
        }

        # Create items
        self.items = [
            Item("AP Medley ", "heal", 15),
            
            Item("Tiny Meat ", "damage", 3),
            Item("Medium Meat ", "damage", 5),
            Item("Large Meat ", "damage", 7),
            
            Item("FV Stir-Fry", "heal", 22),
            Item("CD", "heal", 10),
            Item("Pp Salad", "heal", 8),
            
            Item("Aasparagus Medley", "heal", 12),
            Item("TB Fusion", "heal", 9),
            Item("Rm Medley", "heal", 6),
            Item("Kb Bowl", "heal", 8),
            Item("Carrot", "heal", 8),
            Item("Pea", "heal", 5),
            Item("Asparagus", "heal", 10),
            Item("Broccoli", "heal", 6),
            Item("Radish", "heal", 8),
            Item("Kale", "heal", 9),

            Item("Wraith-Warmed Root Stew", "heal", 30),
            Item("Twilight Broccoli Bliss Bake", "heal", 25),
            Item("Gloomy Carrot Delight", "heal", 10),

            Item("MS Skewers", "heal", 18),
            Item("Mmedium Meat & Frosted Kale Salad", "heal", 30),
            
            Item("TM Stir", "heal", 16),
            Item("RTiny Meat", "heal", 5),
            Item("RMedium Meat", "heal", 10),
            Item("RLarge Meat", "heal", 15),

            Item("Healing Wraps", "remove_status", 35),  # Heals 20 HP
            Item("Spore Balm", "remove_status", 30),
            Item("Stamina Potion", "stamina", 15),  # Restores 15 stamina
            Item("Rrage-Fused Binding", "boost", 15),
            Item("Adrenaline Bar", "boost", 10),  # Boosts damage by 5
            Item("Inferno Shard", "boost", 25), # Boosts damage by 5
            Item("Poison Gas", "damage", 10),  # Deals 10 damage to a target
            Item("Purification Crystal", "cure_status", 0),  # Removes all status effects

            Item("Lifespark Glyph", "heal", 999),
            Item("Etheric Infusion", "full_restore", 999),  # Fully restores HP and stamina
            Item("Embercool Salve", "remove_status", 25)  # New item for single status removal
        ]

        # Define creatures with possible status effects and EXP ranges
        self.creature_templates = [
            Creature("Shadow Stalker", "SS", "Veilmarsh", 5, 135, 
                    {"tiny meat": 0.5, "fiber": 0.3, "leaves": 0.2, "fur": 0.2}, 
                    (10, 20), True, ['bleeding'], 
                    special_ability="double_strike", luck=10),
            Creature("Murk Wraith", "MW", "Veilmarsh", 10, 75, 
                    {"essence": 0.5,"feather": 0.2}, 
                    (10, 20), True, ["bleeding"], 
                    special_ability="", luck=14),
            Creature("Gloom Thicket", "GT", "Veilmarsh", 3, 125, 
                    {"tiny meat": 0.5,"leaves": 0.2}, 
                    (10, 20), False, [], 
                    special_ability="", luck=15),
            Creature("Sporefang", "SP", "Veilmarsh", 11, 40, 
                    {"pelt": 0.5,"claw": 0.2}, 
                    (10, 20), True, ["poison"],
                     special_ability="", luck=18),
            
            Creature("Crystal Rabbit", "CR", "Shattered Plains", 7, 400, 
                    {"tiny meat": 0.7,"resin": 0.2,"fur":0.8}, 
                    (10, 20), False, [], 
                    special_ability="", luck=25),
            Creature("Fissure Frolicker", "FF", "Shattered Plains", 8, 310, 
                    {"medium meat": 0.7,"pulp": 0.2,"pelt":0.8}, 
                    (10, 20), True, ["poison"], 
                    special_ability="", luck=28),
            Creature("Crimson Cracker", "CC", "Shattered Plains", 11, 300, 
                    {"scale": 0.7,"claw": 0.2}, 
                    (10, 20), False, [], 
                    special_ability="quake_stomp", luck=30),
            Creature("Dune Dancer", "DD", "Shattered Plains", 8, 360, 
                    {"scale": 0.7,"pelt":0.8}, 
                    (10, 20), False, [], 
                    special_ability="", luck=35),
            
            Creature("Ashen Hopper", "AH", "Cinderglade", 10, 800, 
                    {"tiny meat": 0.7,"fiber": 0.8}, 
                    (10, 20), False, [], 
                    special_ability="", luck=44),
            Creature("Charseed Buncher", "CB", "Cinderglade", 10, 840, 
                    {"tiny meat": 0.7,"emberbark": 0.4}, 
                    (10, 20), False, [], 
                    special_ability="life_drain", luck=47),
            Creature("Ember Revenant", "ER", "Cinderglade", 14, 702, 
                    {"hide": 0.7,"scale": 0.8}, 
                    (10, 20), True, ["burn"], 
                    special_ability="scorching_grasp", luck=50),
            Creature("Flamewretch", "FW", "Cinderglade", 13, 690, 
                    {"hide": 0.7,"claw": 0.4}, 
                    (10, 20), True, ["burn"], 
                    special_ability="inferno_charge", luck=54),

            Creature("Silhouette Slinker", "SSL", "Obsidian Dunes", 3, 920, 
                    {"tiny meat": 0.7,"shards": 0.8}, 
                    (10, 20), False, [], 
                    special_ability="", luck=58),
            Creature("Cinder Wisp", "CW", "Obsidian Dunes", 5, 1200, 
                    {"medium meat": 0.6,"fur": 0.4,"essence":0.5}, 
                    (40, 120), False, [''], 
                    special_ability="inferno_charge", luck=64),
            Creature("Mirage Stalker", "MS", "Obsidian Dunes", 15, 750, 
                    {"pelt": 0.7,"claw": 0.8,"Obsidian Fragment":0.4}, 
                    (10, 20), False, [], 
                    special_ability="", luck=68),
            Creature("Reflex Vulture", "RV", "Obsidian Dunes", 13, 690, 
                    {"eye": 0.6,"feather": 0.4}, 
                    (40, 120), False, [''], 
                    special_ability="reflective_dive", luck=73),

            Creature("Cloudwalker", "CWA", "Gloom Peaks", 14, 840, 
                    {"tiny meat": 0.6,"frostshard wood": 0.4,"feather":0.5}, 
                    (40, 120), False, [''], 
                    special_ability="", luck=75),        
            Creature("Peak Nibbler", "PN", "Gloom Peaks", 25, 960, 
                    {"medium meat": 0.6, "wool": 0.4,"crystal":0.4}, 
                    (40, 120), False, [''], 
                    special_ability="", luck=80),
            Creature("Shadowdrake", "SD", "Gloom Peaks", 19, 900, 
                    {"scale": 0.6,"claw": 0.4,"feather":0.5}, 
                    (40, 120), False, [''], 
                    special_ability="", luck=90),        
            Creature("Sable Maw", "SM", "Gloom Peaks", 15, 1080, 
                    {"pelt": 0.6, "bone": 0.4,"obsidian Fang":0.4}, 
                    (40, 120), True, [''], 
                    special_ability="tremor_stomp", luck=99)
            ]

        self.plants = [
                Plant("Fiber", "Veilmarsh", 0.7),
                Plant("Carrots", "Veilmarsh", 0.4),
                Plant("Leaves", "Veilmarsh", 0.6),
                
                Plant("Resin", "Shattered Plains", 0.2),
                Plant("Peas", "Shattered Plains", 0.5),
                Plant("Pulp", "Shattered Plains", 0.6),
                
                Plant("Shards", "Obsidian Dunes", 0.4),
                Plant("Fiber", "Obsidian Dunes", 0.8),
                Plant("Essence", "Obsidian Dunes", 0.5),
                
                Plant("Frostshard Wood", "Gloom Peaks", 0.4),
                Plant("Kale", "Gloom Peaks", 0.6),
                Plant("Broccoli", "Gloom Peaks", 0.5),
                Plant("Crystal", "Gloom Peaks", 0.4),

                Plant("Emberbark", "Cinderglade", 0.6),
                Plant("Asparagus", "Cinderglade", 0.8),
                Plant("Radishes", "Cinderglade", 0.7),
                Plant("Fiber", "Cinderglade", 0.8)
            ]

        # Define creature encounter chances while gathering in each biome
        self.gathering_encounter_chances = {
            "Veilmarsh": 0.2,    # 30% chance to encounter creatures
            "Shattered Plains": 0.4, # 40% chance to encounter creatures
            "Obsidian Dunes": 0.5, # 20% chance to encounter creatures
            "Gloom Peaks": 0.7, # 20% chance to encounter creatures
            "Cinderglade": 0.5 # 20% chance to encounter creatures
        }

        self.biomes = {
            "Veilmarsh": self.creature_templates[:4],  # Veilmarsh creatures
            "Shattered Plains": self.creature_templates[4:8],  # Shattered Plains creatures
            "Obsidian Dunes": self.creature_templates[8:12],  # Obsidian Dunes creatures
            "Gloom Peaks": self.creature_templates[12:16],  # Gloom Peaks creatures
            "Cinderglade": self.creature_templates[16:20]  # Cinderglade creatures
        }

        # Define stamina costs for traveling between biomes
        self.travel_costs = {
            ("Veilmarsh", "Obsidian Dunes"): 15,
            ("Veilmarsh", "Gloom Peaks"): 30,
            ("Veilmarsh", "Cinderglade"): 15,
            ("Veilmarsh", "Shattered Plains"): 10,
            
            ("Obsidian Dunes", "Veilmarsh"): 15,
            ("Obsidian Dunes", "Gloom Peaks"): 10,
            ("Obsidian Dunes", "Cinderglade"): 10,
            ("Obsidian Dunes", "Shattered Plains"): 10,
            
            ("Shattered Plains", "Veilmarsh"): 10,
            ("Shattered Plains", "Gloom Peaks"): 20,
            ("Shattered Plains", "Cinderglade"): 10,
            ("Shattered Plains", "Obsidian Dunes"): 10,
            
            ("Gloom Peaks", "Veilmarsh"): 30,
            ("Gloom Peaks", "Shattered Plains"): 20,
            ("Gloom Peaks", "Cinderglade"): 10,
            ("Gloom Peaks", "Obsidian Dunes"): 10,

            ("Cinderglade", "Veilmarsh"): 20,
            ("Cinderglade", "Shattered Plains"): 10,
            ("Cinderglade", "Gloom Peaks"): 10,
            ("Cinderglade", "Obsidian Dunes"): 10,
        }
    def apply_temp_boost(self, player, stat_type, amount, duration):
        """Apply a temporary stat boost to a player"""
        self.temp_boosts[player.name][stat_type] += amount
        self.temp_boosts[player.name]['turns_remaining'] = duration
        
        # Apply the boost
        if stat_type == 'damage':
            player.damage += amount
        elif stat_type == 'protection':
            player.protection += amount

    def update_temp_boosts(self):
        """Update temporary stat boosts at the end of each turn"""
        for player_name, boosts in self.temp_boosts.items():
            if boosts['turns_remaining'] > 0:
                boosts['turns_remaining'] -= 1
                
                # Remove expired boosts
                if boosts['turns_remaining'] == 0:
                    player = next(p for p in self.players if p.name == player_name)
                    player.damage -= boosts['damage']
                    player.protection -= boosts['protection']
                    boosts['damage'] = 0
                    boosts['protection'] = 0
                    
    def choose_target(self, for_heal=False):
        """
        Let the player choose a target (creature or player)
        for_heal: if True, only show creatures that are alive
        """
        if for_heal:
            # For healing abilities, show only alive players
            valid_targets = [p for p in self.players if p.health > 0]
        else:
            # For attacks/other abilities, show the current creature
            valid_targets = [self.creatures[self.current_creature_index]] if self.current_creature_index < len(self.creatures) else []

        if not valid_targets:
            print("No valid targets available!")
            return None

        print("\nChoose a target:")
        for i, target in enumerate(valid_targets, 1):
            if isinstance(target, PlayerCharacter):
                print(f"{i}. {target.name} (HP: {target.health}/{target.max_health})")
            else:
                print(f"{i}. {target.name} (HP: {target.health}/{target.max_health})")

        try:
            choice = int(input("Enter target number: ")) - 1
            if 0 <= choice < len(valid_targets):
                return valid_targets[choice]
            else:
                print("Invalid target selection.")
                return None
        except ValueError:
            print("Please enter a valid number.")
            retubreak
            

    def shadow_lottery(self):
        lottery = ShadowLottery()
        print("\n" * 21)
        print("\n=== SHADOW LOTTERY ===")
        print("How many draws would you like?")
        
        try:
            num_draws = int(input("Enter number of draws: "))
            if num_draws < 1:
                print("Must draw at least once!")
                return
                
            results = lottery.draw_lottery(num_draws)

            print("\n" * 21)
            print("\n=== LOTTERY RESULTS ===")
            for i, result in enumerate(results, 1):
                print(f"\nDraw #{i}:")
                print(f"Category: {result['category']}")
                print(f"Item won: {result['item']}")
                if result['glowstone'] > 0:
                    print(f"Bonus: {result['glowstone']} glowstone!")
                print("\n===          ===")
                
        except ValueError:
            print("Please enter a valid number")

        # Add new method to Battle class
    def gather_plants(self, player):
        # Check stamina first
        stamina_cost = 5
        if player.stamina < stamina_cost:
            print(f"Not enough stamina to gather plants. Required: {stamina_cost}")
            return

        # Keep asking for biome until valid
        while True:
            current_biome = input("Which biome are you gathering in?: ").strip().capitalize()
            full_biome = None
            for biome, abbrev in BIOME_ABBREVIATIONS.items():
                if current_biome.upper() == abbrev or current_biome.lower() == biome.lower():
                    full_biome = biome
                    break
            
            if full_biome and full_biome in self.biomes:
                break
            print("Invalid biome selected. Please try again.")

        # Define plants available in each biome
        biome_plants = {
            "Veilmarsh": {
                "Fiber": 0.7,
                "Carrots": 0.7,
                "Leaves": 0.3
            },
            "Shattered Plains": {
                "Resin ": 0.5,
                "Peas": 0.7,
                "Pulp": 0.6
            },
            "Obsidian Dunes": {
                "Shards ": 0.5,
                "Fiber": 0.7,
                "Essence": 0.6
            },
            "Gloom Peaks": {
                "Frostshard Wood ": 0.5,
                "Kale": 0.7,
                "Broccoli": 0.7,
                "Crystal": 0.6
            },
            "Cinderglade": {
                "Emberbark": 0.8,
                "Asparagus": 0.7,
                "Radishes": 0.7,
                "Fiber": 0.4
            }
        }

        # Let player choose a plant
        while True:
            plant_choice = input("\nEnter the name or abbreviation of the plant you want to gather: ").strip()
            selected_plant = None
            
            for plant in biome_plants[full_biome].keys():
                if (plant_choice.lower() == plant.lower() or 
                    plant_choice.upper() == PLANT_ABBREVIATIONS.get(plant, "").upper()):
                    selected_plant = plant
                    break
            
            if selected_plant:
                break
            print("Invalid plant selection. Please try again.")
        chance = biome_plants[full_biome][selected_plant]
        player.stamina -= stamina_cost

        if random.random() < chance:
            amount = random.randint(1, 3)
            print(f"\nSuccess! You gathered {amount} {selected_plant}(s)")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        else:
            print(f"\nFailed to gather {selected_plant}")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        # Inside gather_plants method, replace the creature encounter section with:
        if random.random() < self.gathering_encounter_chances[full_biome]:
            creatures = self.biomes[full_biome]
            num_creatures = random.randint(1, 2)
            
            # Create the creature instances
            self.creatures = []
            for creature in random.choices(creatures, k=num_creatures):
                new_creature = Creature(
                    creature.name,
                    creature.abbreviation,
                    creature.biome,
                    creature.damage,
                    creature.health,  # This sets both health and max_health
                    creature.drops,
                    creature.exp_range,
                    creature.is_predator,
                    creature.status_effects.copy()  # Make a copy of status effects
                )
                new_creature.reset_health()  # Explicitly reset health
                self.creatures.append(new_creature)
            
            # Display encounter message with specific details
            creature_counts = {}
            for creature in self.creatures:
                creature_counts[creature.name] = creature_counts.get(creature.name, 0) + 1
            
            # Clear screen and display formatted encounter message
            print("\n" * 3)  # Print 21 empty lines to clear screen
            print("\n=== ENCOUNTER ===")
            print("")
            encounter_message = "While gathering, you've encountered: "
            encounter_details = [f"{count} {name}" for name, count in creature_counts.items()]
            print(encounter_message + ", ".join(encounter_details) + "!")
            print("")
            print("\n=== ENCOUNTER ===")
            
            self.start_battle()

    def prompt_for_players(self):
        num_players = int(input("Enter the number of players (0 for none at the beginning): "))
        if num_players > 0:
            for _ in range(num_players):
                player_stats = PlayerCharacter.from_input()
                self.players.append(player_stats)
        else:
            print("No players will be created. Starting with an empty game.")
            return False  # Indicate no players were created
        return True  # Indicate players were created

    def choose_action(self):
        while True:
            print("\n" * 21)
            action = input("What are you doing?").strip().lower()

            if action == 'b':
                if not self.players:  # If no players exist
                    self.prompt_for_players()
                
                if self.players:  # Proceed with battle if players exist
                    self.initiate_battle()
                    continue  # Continue the loop for the next action

    # Add to existing choose_action method
            elif action == 'f':
                farming = FarmingSystem()
                while True:
                    print("\n" * 10)
                    print("\n=== FARMING MENU ===")
                    print("1. Plant and harvest crop")
                    print("2. Exit farming")
                    
                    choice = input("Choose an option: ")
                    
                    if choice == "1":
                        farming.plant_and_harvest()
                    elif choice == "2":
                        break
                    else:
                        print("Invalid choice!")
                        
            elif action == 's':
                if not self.players:
                    self.prompt_for_players()
                if self.players:
                    self.sell_items(self.players[0])
                continue
                
            elif action == 'r':
                if not self.players:
                    self.prompt_for_players()
                
                if self.players:
                    self.recover_menu(self.players[0])
                    continue

            elif action == 'l':
                self.shadow_lottery()
                continue

            elif action == 't':
                if not self.players:  # If no players exist
                    self.prompt_for_players()
                
                if self.players:  # Proceed with travel if players exist
                    self.travel(self.players[0])  # Assuming you want to travel with the first player
                    continue  # Continue the loop for the next action
                
            elif action == 're':
                print("Refreshing the game...")
                self.players.clear()  # Clear all players
                self.creatures.clear()  # Clear all creatures
                self.current_creature_index = 0  # Reset creature index
                self.total_drops.clear()  # Clear drops
                self.total_exp = 0  # Reset experience
                self.prompt_for_players()  # Start fresh with new players
                continue
            
            elif action == 'g':
                if not self.players:
                    self.prompt_for_players()
                if self.players:  # Only proceed if there are players
                    self.gather_plants(self.players[0])  # Use the first player for gathering
                continue
            elif action == "h":
                if not self.players:
                    self.prompt_for_players()
                if self.players:
                    self.hunt_prey()  # Using self.hunt_prey() instead of hunt_prey()
                continue
            
            elif action == 'c':
                if not self.players:
                    self.prompt_for_players()
                
                if self.players:
                    self.craft_menu(self.players[0])
                continue
            
            elif action == 'bo':
                self.show_bounties()
                continue
            else:
                print("Invalid action. Try again.")

    def recover_menu(self, player):
        """Handle recovery options for the player."""
        while True:
            print("")
            print("")
            print("\nRecovery Options:")
            print("1. Nap (Recover 10 stamina)")
            print("2. Sleep (Recover 25 stamina)")
            print("3. Use Item")
            print("4. Back")
            print("")
            print("")
            
            choice = input("Choose an option: ").strip()
            
            if choice == '1':
                player.stamina = min(player.stamina + 10, player.max_stamina)
                print(f"{player.name} takes a nap and recovers 10 stamina. Current stamina: {player.stamina}/{player.max_stamina}")
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
            elif choice == '2':
                player.stamina = min(player.stamina + 25, player.max_stamina)
                print(f"{player.name} gets some sleep and recovers 25 stamina. Current stamina: {player.stamina}/{player.max_stamina}")
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
            elif choice == '3':
                # Use the Battle class's items list instead of player inventory
                if self.items:
                    self.use_item(player)
                else:
                    print("No items available!")
                    
            elif choice == '4':
                break
                
            else:
                print("Invalid option. Please try again.")

    def travel(self, player):
        """Handle multiple players traveling from one biome to another using full names or abbreviations."""
        # Get starting biome
        start_input = input("Where are you starting from? (name or abbreviation): ").strip()
        starting_biome = None
        
        # Check for both full name and abbreviation
        for biome, abbrev in BIOME_ABBREVIATIONS.items():
            if start_input.upper() == abbrev or start_input.lower() == biome.lower():
                starting_biome = biome
                break
        
        if not starting_biome or starting_biome not in self.biomes:
            print("Invalid starting biome. Please choose a valid biome.")
            return

        # Get destination biome
        dest_input = input("Which biome would you like to travel to? (name or abbreviation): ").strip()
        destination_biome = None
        
        # Check for both full name and abbreviation
        for biome, abbrev in BIOME_ABBREVIATIONS.items():
            if dest_input.upper() == abbrev or dest_input.lower() == biome.lower():
                destination_biome = biome
                break
        
        if not destination_biome or destination_biome not in self.biomes:
            print("Invalid destination biome. Please choose a valid biome.")
            return

        stamina_cost = self.travel_costs.get((starting_biome, destination_biome))
        if stamina_cost is None:
            print(f"You cannot travel from {starting_biome} to {destination_biome}.")
            return

        # Check if all players have enough stamina
        for player in players:
            if player.stamina < stamina_cost:
                print("\n" * 21)
                print(f"{player.name} does not have enough stamina to travel to {destination_biome}.")
                return

        # If we get here, all players have enough stamina, so deduct it
        for player in players:
            player.stamina -= stamina_cost
            print("\n" * 21)
            print(f"{player.name} travels from {starting_biome} to {destination_biome} and it takes {stamina_cost} stamina.")

            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        encounter_chance = random.randint(1, 100)

        if encounter_chance <= 20:
        
            print("During travel, the group encountered bad weather, losing 10 stamina each.")
            for player in players:
                player.stamina -= 10
                if player.stamina < 0:
                    print("\n" * 21)
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name} cannot continue and the travel failed due to low stamina!")
                    return

        elif encounter_chance <= 50:
            event_type = random.choice(["cache", "healer"])
            if event_type == "cache":
                print("\n" * 21)
                
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
                print("During your travel, the group found a hidden cache and each received a free prize!")
            elif event_type == "healer":
                for player in players:
                    player.health = player.max_health
                    player.stamina = player.max_stamina
                    print("\n" * 21)
                    print(f"{player.name}'s stats are now: HP={player.health}/{player.max_health}, Stamina={player.stamina}/{player.max_stamina}")
                print("During your travel, you encountered a healer who restored everyone's stats to full!")

        else:
            self.creatures.clear()
            self.current_creature_index = 0  # Reset the creature index
            creatures = self.biomes[destination_biome]
            num_creatures = random.randint(1, 3)

            self.creatures = []
            for creature in random.choices(creatures, k=num_creatures):
                new_creature = Creature(
                    creature.name,
                    creature.abbreviation,
                    creature.biome,
                    creature.damage,
                    creature.health,
                    creature.drops,
                    creature.exp_range,
                    creature.is_predator,
                    creature.status_effects.copy()
                )
                new_creature.reset_health()
                self.creatures.append(new_creature)

            print(f"During travel, the group encountered {len(self.creatures)} creatures!")
            self.start_battle()

    def use_item(self, player):
        print("\n" * 21)
        print("Choose an item to use by typing its abbreviation:")

        abbrev = input("Enter item abbreviation: ").upper()
        item = next((i for i in self.items if i.abbreviation == abbrev), None)
        
        if item:
            # For healing/support items, allow targeting other players
            if item.item_type in ['heal', 'remove_status', 'stamina', 'boost']:
                print("\nChoose target player:")
                for idx, player in enumerate(self.players, 1):
                    print(f"{idx}. {player.name} - HP: {player.health}/{player.max_health}")
                
                try:
                    target_idx = int(input("Enter player number: ")) - 1
                    if 0 <= target_idx < len(self.players):
                        target = self.players[target_idx]
                        
                        # Apply item effect based on type
                        if item.item_type == 'heal':
                            target.health = min(target.health + item.effect_value, target.max_health)
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"{target.name} healed for {item.effect_value} HP!")
                        elif item.item_type == 'remove_status':
                            if target.status_effects:
                                target.status_effects.clear()
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print(f"Removed all status effects from {target.name}!")
                        elif item.item_type == 'stamina':
                            target.stamina = min(target.stamina + item.effect_value, target.max_stamina)
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"{target.name} recovered {item.effect_value} stamina!")
                        elif item.item_type == 'boost':
                            target.damage += item.effect_value
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"\n=== STAT INCREASE ===")
                            print(f"{target.name}'s damage increased by {item.effect_value}!")
                            print(f"\n=== STAT INCREASE ===")
                            print("")
                            
                        self.items_used[item.name] = self.items_used.get(item.name, 0) + 1
                    else:
                        print("Invalid target selection.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                # For offensive items, show all possible targets
                print("\nChoose target:")
                all_targets = []
                
                # Add creatures to targets
                for creature in self.creatures:
                    if creature.health > 0:
                        all_targets.append(('creature', creature))
                
                # Add players to targets
                for player in self.players:
                    all_targets.append(('player', player))
                
                # Display all targets
                for idx, (target_type, target) in enumerate(all_targets, 1):
                    print(f"{idx}. {target.name} ({target_type}) - HP: {target.health}/{target.max_health}")
                
                try:
                    target_idx = int(input("Enter target number: ")) - 1
                    if 0 <= target_idx < len(all_targets):
                        target_type, target = all_targets[target_idx]
                        if item.item_type == 'damage':
                            target.health -= item.effect_value
                            print(f"{target.name} felt sick and took {item.effect_value} damage!")

                            print(f"\n=== PLAYER LINE ===")
                            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                            print(f"\n=== PLAYER LINE ===")
                        self.items_used[item.name] = self.items_used.get(item.name, 0) + 1
                    else:
                        print("Invalid target selection.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("Item not found.")

    def join_new_player(self):
        """Handle the joining of a new player during the battle."""
        print("")
        print("")
        print("")
        print("\n--- A new player wants to join the battle! ---")
        new_player = PlayerCharacter.from_input()  # Create a new player character
        self.players.append(new_player)  # Add to the existing list of players
        print(f"{new_player.name} has joined the battle!")
        print("\n---                                        ---")

    def roar_of_need(self):
        # Get the current player (assuming it's the first player's turn)
        current_player = self.players[0]

        # Check if player has enough stamina
        if current_player.stamina >= 10:  # Cost of ability
            current_player.stamina -= 10
            new_player = PlayerCharacter.from_input()  # Create a new player character
            self.players.append(new_player)  # Add to the existing list of players
            print(f"{new_player.name} has joined the battle!")
            print("\n---                                        ---")
        else:
            print(f"Not enough stamina! Required: 10, Current: {current_player.stamina}")

    def sell_items(self, player):
        has_trader = input("Do you have the Budgeteer title? (y/n): ").lower() == 'y'
        price_multiplier = 1.2 if has_trader else 1.0
        
        # Define base item prices with abbreviations
        item_prices = {
            # Armor prices
            "Ethereal Crown": {"price": 250, "abbrev": "EC"},
            "Ethereal Robes": {"price": 300, "abbrev": "ER"},
            "Ethereal Greaves": {"price": 300, "abbrev": "EG"},
            
            "Shadow Hood": {"price": 200, "abbrev": "SH"},
            "Shadow Cloak": {"price": 300, "abbrev": "SC"},
            "Shadow Boots": {"price": 250, "abbrev": "SHB"},
            
            "Ashen Helm": {"price": 200, "abbrev": "AH"},
            "Ashen Breastplate": {"price": 250, "abbrev": "ABP"},
            "Ashen Treads": {"price": 300, "abbrev": "AT"},

            "Crimson Scale Helm": {"price": 200, "abbrev": "CH"},
            "Crimson Scale Breastplate": {"price": 300, "abbrev": "CB"},
            "Crimson Scale Legguards": {"price": 250, "abbrev": "CS"},

            "Spectral Helm": {"price": 200, "abbrev": "SPH"},
            "Spectral Chestplate": {"price": 300, "abbrev": "SPC"},
            "Spectral Greaves": {"price": 250, "abbrev": "SG"},

            "Obsidian Helm": {"price": 250, "abbrev": "OH"},
            "Obsidian Breastplate": {"price": 350, "abbrev": "OB"},
            "Obsidian Legguards": {"price": 300, "abbrev": "OL"},

            "Crimson Longbow": {"price": 150, "abbrev": "CL"},
            "Wraith Dagger": {"price": 150, "abbrev": "WD"},
            "Flamebrand Sword": {"price": 150, "abbrev": "FS"},
            
            # Materials prices
            "Wraith Silk": {"price": 50, "abbrev": "WS"},
            "Spectral Essence": {"price": 60, "abbrev": "SE"},
            "Phantom Threads": {"price": 55, "abbrev": "PT"},
            "Infernal Core": {"price": 60, "abbrev": "IC"},
            
            # Food prices
            "Wraith-Warmed Root Stew": {"price": 50, "abbrev": "WR"},
            "Asparagus Medley": {"price": 50, "abbrev": "AS"},
            "Twilight Broccoli Bliss": {"price": 50, "abbrev": "TB"},
            "Frostbitten Vegetable Stir-Fry": {"price": 50, "abbrev": "FV"},

            "Gloomy Carrot Delight": {"price": 60, "abbrev": "GC"},
            "Shadow Pea Salad": {"price": 55, "abbrev": "SS"},
            "Asparagus Pea Medley": {"price": 55, "abbrev": "AA"},
            "Twilight Broccoli Fusion": {"price": 55, "abbrev": "TF"},

            "Cursed Radish Medley": {"price": 55, "abbrev": "CR"},
            "Shadow Pea & Tiny Meat Skewers": {"price": 55, "abbrev": "SM"},
            "Grilled Medium Meat & Frosted Kale Salad": {"price": 55, "abbrev": "GM"},
            "Gloomy Carrot": {"price": 4, "abbrev": "CA"},
            "Shadow Peas": {"price": 4, "abbrev": "PE"},
            "Ebon Asparagus": {"price": 4, "abbrev": "AS"},
            "Twilight Broccoli": {"price": 4, "abbrev": "BR"},
            "Cursed Radishes": {"price": 4, "abbrev": "RA"},
            "Frosted Kale": {"price": 4, "abbrev": "KA"},
            "Tiny Meat": {"price": 4, "abbrev": "TI"},
            "Medium Meat": {"price": 12, "abbrev": "ME"},
            "Large Meat": {"price": 15, "abbrev": "LA"},
            
            # Drops prices
            "Fiber": {"price": 3, "abbrev": "FBR"},
            "Leaves": {"price": 2, "abbrev": "LVS"},
            "Essence": {"price": 5, "abbrev": "ES"},
            "Scale": {"price": 4, "abbrev": "SC"},
            "Claw": {"price": 6, "abbrev": "CL"},
            "Feather": {"price": 3, "abbrev": "FT"},
            "Hide": {"price": 5, "abbrev": "HD"},
            "Bone": {"price": 4, "abbrev": "BN"}
        }
        
        print("\n=== SELLING MENU ===")
        if has_trader:
            print("Trader title active: +20% selling prices!")
        
        # Create reverse lookup dictionary for abbreviations
        abbrev_to_item = {info["abbrev"]: item_name for item_name, info in item_prices.items()}
        
        item_input = input("\nWhat would you like to sell? (full name or abbreviation, or 'exit'): ").upper()
        if item_input.lower() == 'exit':
            return
            
        # Check if input matches either full name or abbreviation
        item_to_sell = None
        if item_input in abbrev_to_item:
            item_to_sell = abbrev_to_item[item_input]
        elif item_input in item_prices:
            item_to_sell = item_input
            
        if item_to_sell:
            quantity = int(input(f"How many {item_to_sell} would you like to sell?: "))
            base_price = item_prices[item_to_sell]["price"]
            adjusted_price = int(base_price * price_multiplier)
            total_price = adjusted_price * quantity
            print(f"\nSold {quantity}x {item_to_sell} for {total_price} Glowstone!")
        else:
            print("That item cannot be sold!")
    
    def initiate_battle(self):
        #print("Choose a creature to fight:")
    
        #for creature in self.creature_templates:
            #print(f"{creature.abbreviation}: {creature.name}")

        creature_abbrev = input("Enter the abbreviation of the creature to battle: ").strip().upper()

        # Find the selected creature
        selected_creature = next((c for c in self.creature_templates if c.abbreviation == creature_abbrev), None)
        if not selected_creature:
            print("Invalid creature abbreviation.")
            return

        num_creatures = random.randint(1, 4)  # Roll for 1 to 4 of the selected creature
        self.creatures = [Creature(
            selected_creature.name,
            selected_creature.abbreviation,
            selected_creature.biome,
            selected_creature.damage,
            selected_creature.max_health,
            selected_creature.drops,
            selected_creature.exp_range,
            selected_creature.is_predator,
            selected_creature.status_effects
        ) for _ in range(num_creatures)]
        print("\n" * 21)
        print("\n--- Creatures Encountered ---")
        print(f"You will face {num_creatures} {selected_creature.name}(s)!")

        # Display the creatures being fought
        for creature in self.creatures:
            print(f"- {creature}")
        

        self.current_creature_index = 0  # Reset index for the new battle
        self.start_battle()

    def start_battle(self):
        current_creature = self.creatures[self.current_creature_index]
    
        # Display battle status
        print(f"\nBattle with {current_creature.name}")
        print(f"{current_creature.name}'s Health: {current_creature.health}")
        
        # Display each player's health
        for player in self.players:
            print(f"{player.name}'s Health: {player.health}")
        # Reset total drops and experience for the new battle
        self.total_drops = {}
        self.total_exp = 0

        # Ensure every creature starts with full health
        for creature in self.creatures:
            creature.reset_health()

        battle_ended = False
        while not battle_ended:
            self.update_temp_boosts()
            if self.current_creature_index >= len(self.creatures):
                print("All creatures have been defeated!")
                battle_ended = True
                break

            # Get the currently active creature
            active_creature = self.creatures[self.current_creature_index]

            # Check if the active creature is still alive
            while active_creature.health <= 0:
                print(f"{active_creature.name} has fallen!")
                self.current_creature_index += 1
                if self.current_creature_index >= len(self.creatures):
                    print("All creatures have been defeated!")
                    return  # End battle
                active_creature = self.creatures[self.current_creature_index]
            print("")
            print("\n--- Current Creature ---")
            print(f"\nYou are facing a {active_creature.name} with {active_creature.health} HP.")
            print("\n---                  ---")
            print("")
            # Player's turn to act
            for player in self.players:
                if player.health <= 0:  # Skip if the player is already defeated
                    continue
                
                # Apply status effects before the player's turn
                if not player.apply_status_effects():  # This must happen before the player acts

                    if player.health > 0:  # Allow only alive players to act
                        print(f"\n{player.name}'s turn!")
                        action = input("Enter an action: ").strip().lower()

                        if action == 'a':
                            # Directly target the active creature
                            target_creature = active_creature
                            # Calculate hit chance based on luck comparison
                            miss_chance = 0.15  # Base 5% miss chance for players
                            if player.luck < target_creature.luck:
                                luck_diff = target_creature.luck - player.luck
                                miss_chance += luck_diff * 0.08  # Each point of luck difference adds 8% miss chance
                                miss_chance = min(miss_chance, 0.75)  # Cap total miss chance at 40%
                            
                            # Check if attack misses
                            if random.random() < miss_chance:
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print("")
                                print(f"\n{player.name}'s attack misses {target_creature.name}!")
                                print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")

                                print("")
                                # Add the creature's attack message here
                                if active_creature.health > 0:
                                    damage_dealt = max(active_creature.damage - player.protection, 0)
                                    player.health -= damage_dealt
                                    print(f"{active_creature.name} attacks {player.name} for {damage_dealt} damage after protection!")
                                    print(f"{player.name}'s Health: {player.health}/{player.max_health}")
                                print("")
                                continue
                            
                            # Calculate damage considering player's damage stat
                            damage = player.damage

                            # 20% chance for critical hit
                            if random.random() <= 0.20:
                                damage *= 2  # Double the damage
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                            
                            # Apply damage to creature
                            target_creature.health -= damage
                            
                            # Print attack message
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print("")
                            print(f"{player.name} hits for {damage} damage!")
                            print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                            print("")
                            # Check if creature is defeated
                            if target_creature.health <= 0:
                                print(f"{target_creature.name} is defeated!")
                                
                                # Generate and display drops
                                drops, exp_gained = target_creature.generate_drops()
                                
                                # Update total drops
                                for item, quantity in drops.items():
                                    self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                
                                self.total_exp += exp_gained
                                
                                print(f"Drops gained: {drops}")
                                print(f"Experience gained: {exp_gained}")
                                
                                # Move to next creature
                                self.current_creature_index += 1
                                break



                        elif action == 's':
                            # Show current stats
                            print("\n" * 21)
                            print(f"\n=== {player.name}'s Current Stats ===")
                            print(f"Health: {player.health}/{player.max_health}")
                            print(f"Stamina: {player.stamina}/{player.max_stamina}")
                            print(f"Damage: {player.damage}")
                            print(f"Protection: {player.protection}")
                            print(f"Status Effects: {', '.join(player.status_effects) if player.status_effects else 'None'}")
                            print(f"\n===                               ===")
                            # Show active creature stats
                            print(f"\n=== {active_creature.name}'s Stats ===")
                            print(f"Health: {active_creature.health}/{active_creature.max_health}")
                            print(f"Damage: {active_creature.damage}")
                            print(f"\n===                               ===")
                            
                            # Allow another action after viewing stats
                            print(f"\n{player.name}'s turn!")
                            follow_up_action = input("Choose your action: ").strip().lower()
    
                            # Process the follow-up action by recursively calling the same action handling logic
                            if follow_up_action == 'a':
                                # Directly target the active creature
                                target_creature = active_creature
                                # Calculate hit chance based on luck comparison
                                miss_chance = 0.15  # Base 5% miss chance for players
                                if player.luck < target_creature.luck:
                                    luck_diff = target_creature.luck - player.luck
                                    miss_chance += luck_diff * 0.08  # Each point of luck difference adds 8% miss chance
                                    miss_chance = min(miss_chance, 0.75)  # Cap total miss chance at 40%
                                
                                # Check if attack misses
                                if random.random() < miss_chance:
                                    print("\n" * 21)
                                    print(f"\n--- Actions during {player.name}'s turn ---")
                                    print("")
                                    print(f"\n{player.name}'s attack misses {target_creature.name}!")
                                    print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                                    print("")

                                    # Add the creature's attack message here
                                    if active_creature.health > 0:
                                        damage_dealt = max(active_creature.damage - player.protection, 0)
                                        player.health -= damage_dealt
                                        print(f"{active_creature.name} attacks {player.name} for {damage_dealt} damage after protection!")
                                        print(f"Health: {target.health}")
                                    print("")
                                    continue
                                
                                # Calculate damage considering player's damage stat
                                damage = player.damage

                                # 20% chance for critical hit
                                if random.random() <= 0.20:
                                    damage *= 2  # Double the damage
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                
                                # Apply damage to creature
                                target_creature.health -= damage
                                
                                # Print attack message
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print("")
                                print(f"{player.name} hits for {damage} damage!")
                                print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                                print("")
                                # Check if creature is defeated
                                if target_creature.health <= 0:
                                    print(f"{target_creature.name} is defeated!")
                                    
                                    # Generate and display drops
                                    drops, exp_gained = target_creature.generate_drops()
                                    
                                    # Update total drops
                                    for item, quantity in drops.items():
                                        self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                    
                                    self.total_exp += exp_gained
                                    
                                    print(f"Drops gained: {drops}")
                                    print(f"Experience gained: {exp_gained}")
                                    
                                    # Move to next creature
                                    self.current_creature_index += 1
                                    break
                                
                                if target_creature.health <= 0:
                                    print(f"{target_creature.name} is defeated!")
                                    drops, exp_gained = target_creature.generate_drops()
                                    for item, quantity in drops.items():
                                        self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                    self.total_exp += exp_gained
                                    print(f"Drops gained: {drops}")
                                    print(f"Experience gained: {exp_gained}")
                                    self.current_creature_index += 1
                                    break
                            elif follow_up_action == 't':
                                target_player = self.choose_target(for_heal=True)
                                if target_player:
                                    player.triage(target_player)
                                
                            elif follow_up_action == 'as':
                                target_player = self.choose_target(for_heal=True)
                                if target_player:
                                    player.aid_surge(target_player)

                            elif follow_up_action == 'i':
                                player.iron_bastion()

                            elif follow_up_action == 'f':
                                player.fortify()

                            elif follow_up_action == 'eh':
                                target_player = self.choose_target()
                                if target_player:
                                    player.emergency_heal(target_player)

                            elif follow_up_action == 'bb':
                                target_player = self.choose_target()
                                if target_player:
                                    player.body_bash(target_player)

                            elif follow_up_action == 'p':
                                target_player = self.choose_target()
                                if target_player:
                                    player.power_attack(target_player)

                            elif follow_up_action == 'cp':
                                target_player = self.choose_target()
                                if target_player:
                                    player.critical_precision(target_player)
                                    
                            elif follow_up_action == 'pg':
                                target_player = self.choose_target()
                                if target_player:
                                    player.poison_gas(target_player)

                            elif follow_up_action == 'cb':
                                target_player = self.choose_target()
                                if target_player:
                                    player.crushing_blow(target_player)

                            elif follow_up_action == 'gs':
                                target_player = self.choose_target()
                                if target_player:
                                    player.guardian_slam(target_player)

                            elif follow_up_action == 'r':
                                target_player = self.choose_target()
                                if target_player:
                                    player.ravage(target_player)

                            elif follow_up_action == 'd':
                                target_player = self.choose_target()
                                if target_player:
                                    player.double_strike(target_player)

                            elif follow_up_action == 'ra':
                                player.rally()

                            elif follow_up_action == 'e':
                                if self.attempt_escape(player, active_creature):
                                    return  # End the battle if escape was successful
                                
                            elif follow_up_action == 'rn':
                                self.roar_of_need()
                                
                            elif follow_up_action == 'j':
                                self.join_new_player()
                                print(f"{player.name} can now take another action.")
                                break  # Break to allow the player to take an additional action

                            elif follow_up_action == 'ui':
                                self.use_item(player)  # Correctly pass the player to use_item
                            
                            else:
                                print("Invalid action.")
                                # Add other action handlers similarly
                            
                        elif action == 't':
                            target_player = self.choose_target(for_heal=True)
                            if target_player:
                                player.triage(target_player)
                                
                        elif action == 'as':
                            target_player = self.choose_target(for_heal=True)
                            if target_player:
                                player.aid_surge(target_player)

                        elif action == 'i':
                            player.iron_bastion()

                        elif action == 'f':
                            player.fortify()

                        elif action == 'eh':
                            target_player = self.choose_target()
                            if target_player:
                                player.emergency_heal(target_player)

                        elif action == 'bb':
                            target_player = self.choose_target()
                            if target_player:
                                player.body_bash(target_player)
                            
                        elif action == 'pg':
                            target_player = self.choose_target()
                            if target_player:
                                player.poison_gas(target_player)

                        elif action == 'p':
                            target_player = self.choose_target()
                            if target_player:
                                player.power_attack(target_player)

                        elif action == 'cp':
                            target_player = self.choose_target()
                            if target_player:
                                player.critical_precision(target_player)

                        elif action == 'cb':
                            target_player = self.choose_target()
                            if target_player:
                                player.crushing_blow(target_player)

                        elif action == 'gs':
                            target_player = self.choose_target()
                            if target_player:
                                player.guardian_slam(target_player)

                        elif action == 'r':
                            target_player = self.choose_target()
                            if target_player:
                                player.ravage(target_player)

                        elif action == 'd':
                            target_player = self.choose_target()
                            if target_player:
                                player.double_strike(target_player)

                        elif action == 'ra':
                            player.rally()

                        elif action == 'e':
                            if self.attempt_escape(player, active_creature):
                                return  # End the battle if escape was successful
                            
                        elif action == 'rn':
                            self.roar_of_need()
                            
                        elif action == 'j':
                            self.join_new_player()
                            print(f"{player.name} can now take another action.")
                            break  # Break to allow the player to take an additional action

                        elif action == 'ui':
                            self.use_item(player)  # Correctly pass the player to use_item
                        
                        else:
                            print("Invalid action.")

                # Creature's turn after all players have acted
                if active_creature.health > 0:
                    alive_players = [p for p in self.players if p.health > 0]
                    if not alive_players:  # If there are no alive players left
                        break

                    target_player = random.choice(alive_players)  # Choose a random alive player
                    active_creature.attack(player)  # Creatures attack players
                    
             # At the end of the battle loop, check if all creatures are defeated
            if all(creature.health <= 0 for creature in self.creatures):
                battle_ended = True
                break
            
            # Check if all players are defeated
            if all(player.health <= 0 for player in self.players):
                print("All players have been defeated!")
                battle_ended = True
                break

        # Call end_battle when the battle is over
        if battle_ended:
            self.end_battle()

                    

    def end_battle(self):
        for player in self.players:
            player.clear_temp_stats()
        for player_name, boosts in self.temp_boosts.items():
            if boosts['damage'] > 0 or boosts['protection'] > 0:
                player = next(p for p in self.players if p.name == player_name)
                player.damage -= boosts['damage']
                player.protection -= boosts['protection']
                boosts['damage'] = 0
                boosts['protection'] = 0
                boosts['turns_remaining'] = 0
        print("")
        print("")
        print("")
        print("\n--- End of Battle Stats ---")
        for player in self.players:
            # Show current player stats
            status_effects = ','.join(player.status_effects) if player.status_effects else "None"
            print("")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
            print("")
            print(f"Health: {player.health}/{player.max_health}")
            print(f"Stamina: {player.stamina}/{player.max_stamina}")
            print(f"Damage: {player.damage}")
            print(f"Protection: {player.protection}")
            print(f"Status Effects: {', '.join(player.status_effects) if player.status_effects else 'None'}")
            print("")
            print("")
            # Only remove 'daze' status effect after battle
            if 'daze' in player.status_effects:
                player.status_effects.remove('daze')
                print(f"Daze effect removed from {player.name}")

        # Show total drops and EXP from the battle
        print("\n--- Total Drops Gained ---")
        if self.total_drops:
            for item, amount in self.total_drops.items():
                print(f"{item}: {amount}")
        else:
            print("No drops were gained.")

        print(f"Total Experience Gained: {self.total_exp}")

        print("\n--- Items Used During Battle ---")
        if self.items_used:
            for item_name, count in self.items_used.items():
                print(f"{item_name}: {count}")
        else:
            print("No items were used.")


    def attempt_escape(self, player, active_creature):
        if random.random() < 0.4:  # 40% chance to escape
            print(f"{player.name} successfully escaped from {active_creature.name}!")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
            return True  # Return True to indicate the battle should end
        else:
            # Calculate damage when escape fails
            damage_dealt = max(active_creature.damage - player.protection, 0)
            player.health -= damage_dealt
            
            print(f"{player.name} failed to escape and takes {damage_dealt} damage from {active_creature.name}!")
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
            return False  # Return False to indicate the battle continuesrn None

    def show_bounties(self):
        bounty_system = BountySystem()
        available_bounties = bounty_system.get_available_bounties()
        print("\n" * 21)
        print("\n=== Available Bounties ===")
        for i, bounty in enumerate(available_bounties, 1):
            print(f"\n{i}. {bounty['type']} Bounty:")
            print(f"Task: {bounty['task']}")
            print(f"Reward: {bounty['reward']} glowstone")
        
        choice = input("\nSelect a bounty (1-3) or press Enter to skip: ")
        if choice.isdigit() and 1 <= int(choice) <= len(available_bounties):
            selected_bounty = available_bounties[int(choice)-1]
            print(f"\nYou've accepted the bounty: {selected_bounty['task']}")
            print(f"Complete this task to earn {selected_bounty['reward']} glowstone!")
            print("\n===               ===")
            return selected_bounty
        return None

    def reset_all_creatures(self):
        """Reset health for all creatures in the battle."""
        for creature in self.creatures:
            creature.reset_health()

    def hunt_prey(self):
        # Initial prey hunting chance (30%)
        if random.random() <= 0.55:
            # Existing pet hunting logic
            pet_types = {
                "Pup": {"abbrev": "PU", "rewards": (1, 5), "biome": "Cinderglade"},
                "Pangolin": {"abbrev": "PA", "rewards": (5, 10), "biome": "Veilmarsh"},
                "Wispfly": {"abbrev": "WF", "rewards": (10, 20), "biome": "Gloom Peaks"},
                "Shardlizard": {"abbrev": "SL", "rewards": (15, 25), "biome": "Shattered Plains"}
            }
            
            # Display available pets with abbreviations
            print("\nAvailable pets:")
            for pet, info in pet_types.items():
                print(f"{pet} ({info['abbrev']})")
            
            # Get pet choice from user
            pet_input = input("Which pet would you like to catch? (name or abbreviation): ").upper()
            stamina_cost = 5

            player = self.players[0]
            
            if player.stamina < stamina_cost:
                print(f"Not enough stamina to capture a pet! Required: {stamina_cost}")
                return

            # Find the pet by name or abbreviation
            selected_pet = None
            for pet, info in pet_types.items():
                if pet_input == info['abbrev'] or pet_input == pet.upper():
                    selected_pet = pet
                    break
            
            if not selected_pet:
                print("That pet is not available to catch!")
                return
            
            try:
                num_pets = int(input("How many would you like to catch? "))
                player.stamina -= stamina_cost
                if num_pets < 1:
                    print("You must try to catch at least 1!")
                    return
            except ValueError:
                print("Please enter a valid number!")
                return
                
            successful_catches = 0
            total_glowstone = 0
            
            for i in range(num_pets):
                pet_direction = random.choice(["left", "right", "forward", "backward"])
                guess = input(f"\nPet #{i+1} is running! Guess left, right, forward, backward!: ").lower()
                
                if guess == pet_direction:
                    print("Success! You caught the pet!")
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                    print(f"\n=== PLAYER LINE ===")
                    successful_catches += 1
                    glowstone = random.randint(*pet_types[selected_pet]['rewards'])
                    total_glowstone += glowstone
                    print(f"You earned {glowstone} glowstone!")
                else:
                    print(f"The pet got away! It ran {pet_direction}!")
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                    print(f"\n=== PLAYER LINE ===")
                    
            print(f"\nCatching Results:")
            print(f"Pets Caught: {successful_catches}/{num_pets}")
            print(f"Total Glowstone Earned: {total_glowstone}")

            # After prey hunting sequence completes (whether successful or not)
            if random.random() <= 0.5:  # 50% chance for creature encounter
                print("\n" * 3)  # Print 21 empty lines to clear screen
                print("\n=== ENCOUNTER ===")
                
                # Get the current biome based on the selected pet
                current_biome = None
                for pet, info in pet_types.items():
                    if pet_input == info['abbrev'] or pet_input == pet.upper():
                        current_biome = info['biome']
                        break
                
                if current_biome and current_biome in self.biomes:
                    # Clear any existing creatures
                    self.creatures.clear()
                    
                    # Get available creatures for this biome
                    biome_creatures = self.biomes[current_biome]
                    
                    # Spawn 1-2 random creatures from this biome
                    num_creatures = random.randint(1, 2)
                    selected_creatures = random.choices(biome_creatures, k=num_creatures)
                    
                    # Create the creature instances
                    for creature_template in selected_creatures:
                        new_creature = Creature(
                            creature_template.name,
                            creature_template.abbreviation,
                            creature_template.biome,
                            creature_template.damage,
                            creature_template.max_health,
                            creature_template.drops,
                            creature_template.exp_range,
                            creature_template.is_predator,
                            creature_template.status_effects
                        )
                        self.creatures.append(new_creature)
                    
                    print(f"You've encountered {num_creatures} creatures in {current_biome}!")
                    print("\n=== ENCOUNTER ===")
                    self.start_battle()
        else:
            print("\n FAILURE: No pets found.")

    def craft_menu(self, player):
        crafting = CraftingSystem()
        
        while True:
            recipe_name = input("Enter the name of the item to craft or 'exit' to leave: ")
            crafting.craft_item(player, recipe_name, player.inventory)
            if recipe_name == 'exit':
                break
            

    def shadow_lottery(self):
        lottery = ShadowLottery()
        print("\n" * 21)
        print("\n=== SHADOW LOTTERY ===")
        print("How many draws would you like?")
        
        try:
            num_draws = int(input("Enter number of draws: "))
            if num_draws < 1:
                print("Must draw at least once!")
                return
                
            results = lottery.draw_lottery(num_draws)

            print("\n" * 21)
            print("\n=== LOTTERY RESULTS ===")
            for i, result in enumerate(results, 1):
                print(f"\nDraw #{i}:")
                print(f"Category: {result['category']}")
                print(f"Item won: {result['item']}")
                if result['glowstone'] > 0:
                    print(f"Bonus: {result['glowstone']} glowstone!")
                print("\n===          ===")
                
        except ValueError:
            print("Please enter a valid number")

        # Add new method to Battle class
    def gather_plants(self, player):
        # Check stamina first
        stamina_cost = 5
        if player.stamina < stamina_cost:
            print(f"Not enough stamina to gather plants. Required: {stamina_cost}")
            return

        # Keep asking for biome until valid
        while True:
            current_biome = input("Which biome are you gathering in?: ").strip().capitalize()
            full_biome = None
            for biome, abbrev in BIOME_ABBREVIATIONS.items():
                if current_biome.upper() == abbrev or current_biome.lower() == biome.lower():
                    full_biome = biome
                    break
            
            if full_biome and full_biome in self.biomes:
                break
            print("Invalid biome selected. Please try again.")

        # Define plants available in each biome
        biome_plants = {
            "Veilmarsh": {
                "Fiber": 0.7,
                "Carrots": 0.7,
                "Leaves": 0.3
            },
            "Shattered Plains": {
                "Resin ": 0.5,
                "Peas": 0.7,
                "Pulp": 0.6
            },
            "Obsidian Dunes": {
                "Shards ": 0.5,
                "Fiber": 0.7,
                "Essence": 0.6
            },
            "Gloom Peaks": {
                "Frostshard Wood ": 0.5,
                "Kale": 0.7,
                "Broccoli": 0.7,
                "Crystal": 0.6
            },
            "Cinderglade": {
                "Emberbark": 0.8,
                "Asparagus": 0.7,
                "Radishes": 0.7,
                "Fiber": 0.4
            }
        }

        # Let player choose a plant
        while True:
            plant_choice = input("\nEnter the name or abbreviation of the plant you want to gather: ").strip()
            selected_plant = None
            
            for plant in biome_plants[full_biome].keys():
                if (plant_choice.lower() == plant.lower() or 
                    plant_choice.upper() == PLANT_ABBREVIATIONS.get(plant, "").upper()):
                    selected_plant = plant
                    break
            
            if selected_plant:
                break
            print("Invalid plant selection. Please try again.")
        chance = biome_plants[full_biome][selected_plant]
        player.stamina -= stamina_cost

        if random.random() < chance:
            amount = random.randint(1, 3)
            print(f"\nSuccess! You gathered {amount} {selected_plant}(s)")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        else:
            print(f"\nFailed to gather {selected_plant}")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        # Inside gather_plants method, replace the creature encounter section with:
        if random.random() < self.gathering_encounter_chances[full_biome]:
            creatures = self.biomes[full_biome]
            num_creatures = random.randint(1, 2)
            
            # Create the creature instances
            self.creatures = []
            for creature in random.choices(creatures, k=num_creatures):
                new_creature = Creature(
                    creature.name,
                    creature.abbreviation,
                    creature.biome,
                    creature.damage,
                    creature.health,  # This sets both health and max_health
                    creature.drops,
                    creature.exp_range,
                    creature.is_predator,
                    creature.status_effects.copy()  # Make a copy of status effects
                )
                new_creature.reset_health()  # Explicitly reset health
                self.creatures.append(new_creature)
            
            # Display encounter message with specific details
            creature_counts = {}
            for creature in self.creatures:
                creature_counts[creature.name] = creature_counts.get(creature.name, 0) + 1
            
            # Clear screen and display formatted encounter message
            print("\n" * 3)  # Print 21 empty lines to clear screen
            print("\n=== ENCOUNTER ===")
            print("")
            encounter_message = "While gathering, you've encountered: "
            encounter_details = [f"{count} {name}" for name, count in creature_counts.items()]
            print(encounter_message + ", ".join(encounter_details) + "!")
            print("")
            print("\n=== ENCOUNTER ===")
            
            self.start_battle()

    def prompt_for_players(self):
        num_players = int(input("Enter the number of players (0 for none at the beginning): "))
        if num_players > 0:
            for _ in range(num_players):
                player_stats = PlayerCharacter.from_input()
                self.players.append(player_stats)
        else:
            print("No players will be created. Starting with an empty game.")
            return False  # Indicate no players were created
        return True  # Indicate players were created

    def choose_action(self):
        while True:
            print("\n" * 21)
            action = input("What are you doing?").strip().lower()

            if action == 'b':
                if not self.players:  # If no players exist
                    self.prompt_for_players()
                
                if self.players:  # Proceed with battle if players exist
                    self.initiate_battle()
                    continue  # Continue the loop for the next action

    # Add to existing choose_action method
            elif action == 'f':
                farming = FarmingSystem()
                while True:
                    print("\n" * 10)
                    print("\n=== FARMING MENU ===")
                    print("1. Plant and harvest crop")
                    print("2. Exit farming")
                    
                    choice = input("Choose an option: ")
                    
                    if choice == "1":
                        farming.plant_and_harvest()
                    elif choice == "2":
                        break
                    else:
                        print("Invalid choice!")
                        
            elif action == 's':
                if not self.players:
                    self.prompt_for_players()
                if self.players:
                    self.sell_items(self.players[0])
                continue
                
            elif action == 'r':
                if not self.players:
                    self.prompt_for_players()
                
                if self.players:
                    self.recover_menu(self.players[0])
                    continue

            elif action == 'l':
                self.shadow_lottery()
                continue

            elif action == 't':
                if not self.players:  # If no players exist
                    self.prompt_for_players()
                
                if self.players:  # Proceed with travel if players exist
                    self.travel(self.players[0])  # Assuming you want to travel with the first player
                    continue  # Continue the loop for the next action
                
            elif action == 're':
                print("Refreshing the game...")
                self.players.clear()  # Clear all players
                self.creatures.clear()  # Clear all creatures
                self.current_creature_index = 0  # Reset creature index
                self.total_drops.clear()  # Clear drops
                self.total_exp = 0  # Reset experience
                self.prompt_for_players()  # Start fresh with new players
                continue
            
            elif action == 'g':
                if not self.players:
                    self.prompt_for_players()
                if self.players:  # Only proceed if there are players
                    self.gather_plants(self.players[0])  # Use the first player for gathering
                continue
            elif action == "h":
                if not self.players:
                    self.prompt_for_players()
                if self.players:
                    self.hunt_prey()  # Using self.hunt_prey() instead of hunt_prey()
                continue
            
            elif action == 'c':
                if not self.players:
                    self.prompt_for_players()
                
                if self.players:
                    self.craft_menu(self.players[0])
                continue
            
            elif action == 'bo':
                self.show_bounties()
                continue
            else:
                print("Invalid action. Try again.")

    def recover_menu(self, player):
        """Handle recovery options for the player."""
        while True:
            print("")
            print("")
            print("\nRecovery Options:")
            print("1. Nap (Recover 10 stamina)")
            print("2. Sleep (Recover 25 stamina)")
            print("3. Use Item")
            print("4. Back")
            print("")
            print("")
            
            choice = input("Choose an option: ").strip()
            
            if choice == '1':
                player.stamina = min(player.stamina + 10, player.max_stamina)
                print(f"{player.name} takes a nap and recovers 10 stamina. Current stamina: {player.stamina}/{player.max_stamina}")
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
            elif choice == '2':
                player.stamina = min(player.stamina + 25, player.max_stamina)
                print(f"{player.name} gets some sleep and recovers 25 stamina. Current stamina: {player.stamina}/{player.max_stamina}")
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
            elif choice == '3':
                # Use the Battle class's items list instead of player inventory
                if self.items:
                    self.use_item(player)
                else:
                    print("No items available!")
                    
            elif choice == '4':
                break
                
            else:
                print("Invalid option. Please try again.")

    def travel(self, player):
        """Handle multiple players traveling from one biome to another using full names or abbreviations."""
        # Get starting biome
        start_input = input("Where are you starting from? (name or abbreviation): ").strip()
        starting_biome = None
        
        # Check for both full name and abbreviation
        for biome, abbrev in BIOME_ABBREVIATIONS.items():
            if start_input.upper() == abbrev or start_input.lower() == biome.lower():
                starting_biome = biome
                break
        
        if not starting_biome or starting_biome not in self.biomes:
            print("Invalid starting biome. Please choose a valid biome.")
            return

        # Get destination biome
        dest_input = input("Which biome would you like to travel to? (name or abbreviation): ").strip()
        destination_biome = None
        
        # Check for both full name and abbreviation
        for biome, abbrev in BIOME_ABBREVIATIONS.items():
            if dest_input.upper() == abbrev or dest_input.lower() == biome.lower():
                destination_biome = biome
                break
        
        if not destination_biome or destination_biome not in self.biomes:
            print("Invalid destination biome. Please choose a valid biome.")
            return

        stamina_cost = self.travel_costs.get((starting_biome, destination_biome))
        if stamina_cost is None:
            print(f"You cannot travel from {starting_biome} to {destination_biome}.")
            return

        # Check if all players have enough stamina
        for player in players:
            if player.stamina < stamina_cost:
                print("\n" * 21)
                print(f"{player.name} does not have enough stamina to travel to {destination_biome}.")
                return

        # If we get here, all players have enough stamina, so deduct it
        for player in players:
            player.stamina -= stamina_cost
            print("\n" * 21)
            print(f"{player.name} travels from {starting_biome} to {destination_biome} and it takes {stamina_cost} stamina.")

            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
        encounter_chance = random.randint(1, 100)

        if encounter_chance <= 20:
        
            print("During travel, the group encountered bad weather, losing 10 stamina each.")
            for player in players:
                player.stamina -= 10
                if player.stamina < 0:
                    print("\n" * 21)
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                    print(f"\n=== PLAYER LINE ===")
                    print(f"{player.name} cannot continue and the travel failed due to low stamina!")
                    return

        elif encounter_chance <= 50:
            event_type = random.choice(["cache", "healer"])
            if event_type == "cache":
                print("\n" * 21)
                
                print(f"\n=== PLAYER LINE ===")
                print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                print(f"\n=== PLAYER LINE ===")
                print("During your travel, the group found a hidden cache and each received a free prize!")
            elif event_type == "healer":
                for player in players:
                    player.health = player.max_health
                    player.stamina = player.max_stamina
                    print("\n" * 21)
                    print(f"{player.name}'s stats are now: HP={player.health}/{player.max_health}, Stamina={player.stamina}/{player.max_stamina}")
                print("During your travel, you encountered a healer who restored everyone's stats to full!")

        else:
            self.creatures.clear()
            self.current_creature_index = 0  # Reset the creature index
            creatures = self.biomes[destination_biome]
            num_creatures = random.randint(1, 3)

            self.creatures = []
            for creature in random.choices(creatures, k=num_creatures):
                new_creature = Creature(
                    creature.name,
                    creature.abbreviation,
                    creature.biome,
                    creature.damage,
                    creature.health,
                    creature.drops,
                    creature.exp_range,
                    creature.is_predator,
                    creature.status_effects.copy()
                )
                new_creature.reset_health()
                self.creatures.append(new_creature)

            print(f"During travel, the group encountered {len(self.creatures)} creatures!")
            self.start_battle()

    def use_item(self, player):
        print("\n" * 21)
        print("Choose an item to use by typing its abbreviation:")

        abbrev = input("Enter item abbreviation: ").upper()
        item = next((i for i in self.items if i.abbreviation == abbrev), None)
        
        if item:
            # For healing/support items, allow targeting other players
            if item.item_type in ['heal', 'remove_status', 'stamina', 'boost']:
                print("\nChoose target player:")
                for idx, player in enumerate(self.players, 1):
                    print(f"{idx}. {player.name} - HP: {player.health}/{player.max_health}")
                
                try:
                    target_idx = int(input("Enter player number: ")) - 1
                    if 0 <= target_idx < len(self.players):
                        target = self.players[target_idx]
                        
                        # Apply item effect based on type
                        if item.item_type == 'heal':
                            target.health = min(target.health + item.effect_value, target.max_health)
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"{target.name} healed for {item.effect_value} HP!")
                        elif item.item_type == 'remove_status':
                            if target.status_effects:
                                target.status_effects.clear()
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print(f"Removed all status effects from {target.name}!")
                        elif item.item_type == 'stamina':
                            target.stamina = min(target.stamina + item.effect_value, target.max_stamina)
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"{target.name} recovered {item.effect_value} stamina!")
                        elif item.item_type == 'boost':
                            target.damage += item.effect_value
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print(f"\n=== STAT INCREASE ===")
                            print(f"{target.name}'s damage increased by {item.effect_value}!")
                            print(f"\n=== STAT INCREASE ===")
                            print("")
                            
                        self.items_used[item.name] = self.items_used.get(item.name, 0) + 1
                    else:
                        print("Invalid target selection.")
                except ValueError:
                    print("Please enter a valid number.")
            else:
                # For offensive items, show all possible targets
                print("\nChoose target:")
                all_targets = []
                
                # Add creatures to targets
                for creature in self.creatures:
                    if creature.health > 0:
                        all_targets.append(('creature', creature))
                
                # Add players to targets
                for player in self.players:
                    all_targets.append(('player', player))
                
                # Display all targets
                for idx, (target_type, target) in enumerate(all_targets, 1):
                    print(f"{idx}. {target.name} ({target_type}) - HP: {target.health}/{target.max_health}")
                
                try:
                    target_idx = int(input("Enter target number: ")) - 1
                    if 0 <= target_idx < len(all_targets):
                        target_type, target = all_targets[target_idx]
                        if item.item_type == 'damage':
                            target.health -= item.effect_value
                            print(f"{target.name} felt sick and took {item.effect_value} damage!")

                            print(f"\n=== PLAYER LINE ===")
                            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
                            print(f"\n=== PLAYER LINE ===")
                        self.items_used[item.name] = self.items_used.get(item.name, 0) + 1
                    else:
                        print("Invalid target selection.")
                except ValueError:
                    print("Please enter a valid number.")
        else:
            print("Item not found.")

    def join_new_player(self):
        """Handle the joining of a new player during the battle."""
        print("")
        print("")
        print("")
        print("\n--- A new player wants to join the battle! ---")
        new_player = PlayerCharacter.from_input()  # Create a new player character
        self.players.append(new_player)  # Add to the existing list of players
        print(f"{new_player.name} has joined the battle!")
        print("\n---                                        ---")

    def roar_of_need(self):
        # Get the current player (assuming it's the first player's turn)
        current_player = self.players[0]

        # Check if player has enough stamina
        if current_player.stamina >= 10:  # Cost of ability
            current_player.stamina -= 10
            new_player = PlayerCharacter.from_input()  # Create a new player character
            self.players.append(new_player)  # Add to the existing list of players
            print(f"{new_player.name} has joined the battle!")
            print("\n---                                        ---")
        else:
            print(f"Not enough stamina! Required: 10, Current: {current_player.stamina}")

    def sell_items(self, player):
        has_trader = input("Do you have the Budgeteer title? (y/n): ").lower() == 'y'
        price_multiplier = 1.2 if has_trader else 1.0
        
        # Define base item prices with abbreviations
        item_prices = {
            # Armor prices
            "Ethereal Crown": {"price": 250, "abbrev": "EC"},
            "Ethereal Robes": {"price": 300, "abbrev": "ER"},
            "Ethereal Greaves": {"price": 300, "abbrev": "EG"},
            
            "Shadow Hood": {"price": 200, "abbrev": "SH"},
            "Shadow Cloak": {"price": 300, "abbrev": "SC"},
            "Shadow Boots": {"price": 250, "abbrev": "SHB"},
            
            "Ashen Helm": {"price": 200, "abbrev": "AH"},
            "Ashen Breastplate": {"price": 250, "abbrev": "ABP"},
            "Ashen Treads": {"price": 300, "abbrev": "AT"},

            "Crimson Scale Helm": {"price": 200, "abbrev": "CH"},
            "Crimson Scale Breastplate": {"price": 300, "abbrev": "CB"},
            "Crimson Scale Legguards": {"price": 250, "abbrev": "CS"},

            "Spectral Helm": {"price": 200, "abbrev": "SPH"},
            "Spectral Chestplate": {"price": 300, "abbrev": "SPC"},
            "Spectral Greaves": {"price": 250, "abbrev": "SG"},

            "Obsidian Helm": {"price": 250, "abbrev": "OH"},
            "Obsidian Breastplate": {"price": 350, "abbrev": "OB"},
            "Obsidian Legguards": {"price": 300, "abbrev": "OL"},

            "Crimson Longbow": {"price": 150, "abbrev": "CL"},
            "Wraith Dagger": {"price": 150, "abbrev": "WD"},
            "Flamebrand Sword": {"price": 150, "abbrev": "FS"},
            
            # Materials prices
            "Wraith Silk": {"price": 50, "abbrev": "WS"},
            "Spectral Essence": {"price": 60, "abbrev": "SE"},
            "Phantom Threads": {"price": 55, "abbrev": "PT"},
            "Infernal Core": {"price": 60, "abbrev": "IC"},
            
            # Food prices
            "Wraith-Warmed Root Stew": {"price": 50, "abbrev": "WR"},
            "Asparagus Medley": {"price": 50, "abbrev": "AS"},
            "Twilight Broccoli Bliss": {"price": 50, "abbrev": "TB"},
            "Frostbitten Vegetable Stir-Fry": {"price": 50, "abbrev": "FV"},

            "Gloomy Carrot Delight": {"price": 60, "abbrev": "GC"},
            "Shadow Pea Salad": {"price": 55, "abbrev": "SS"},
            "Asparagus Pea Medley": {"price": 55, "abbrev": "AA"},
            "Twilight Broccoli Fusion": {"price": 55, "abbrev": "TF"},

            "Cursed Radish Medley": {"price": 55, "abbrev": "CR"},
            "Shadow Pea & Tiny Meat Skewers": {"price": 55, "abbrev": "SM"},
            "Grilled Medium Meat & Frosted Kale Salad": {"price": 55, "abbrev": "GM"},
            "Gloomy Carrot": {"price": 4, "abbrev": "CA"},
            "Shadow Peas": {"price": 4, "abbrev": "PE"},
            "Ebon Asparagus": {"price": 4, "abbrev": "AS"},
            "Twilight Broccoli": {"price": 4, "abbrev": "BR"},
            "Cursed Radishes": {"price": 4, "abbrev": "RA"},
            "Frosted Kale": {"price": 4, "abbrev": "KA"},
            "Tiny Meat": {"price": 4, "abbrev": "TI"},
            "Medium Meat": {"price": 12, "abbrev": "ME"},
            "Large Meat": {"price": 15, "abbrev": "LA"},
            
            # Drops prices
            "Fiber": {"price": 3, "abbrev": "FBR"},
            "Leaves": {"price": 2, "abbrev": "LVS"},
            "Essence": {"price": 5, "abbrev": "ES"},
            "Scale": {"price": 4, "abbrev": "SC"},
            "Claw": {"price": 6, "abbrev": "CL"},
            "Feather": {"price": 3, "abbrev": "FT"},
            "Hide": {"price": 5, "abbrev": "HD"},
            "Bone": {"price": 4, "abbrev": "BN"}
        }
        
        print("\n=== SELLING MENU ===")
        if has_trader:
            print("Trader title active: +20% selling prices!")
        
        # Create reverse lookup dictionary for abbreviations
        abbrev_to_item = {info["abbrev"]: item_name for item_name, info in item_prices.items()}
        
        item_input = input("\nWhat would you like to sell? (full name or abbreviation, or 'exit'): ").upper()
        if item_input.lower() == 'exit':
            return
            
        # Check if input matches either full name or abbreviation
        item_to_sell = None
        if item_input in abbrev_to_item:
            item_to_sell = abbrev_to_item[item_input]
        elif item_input in item_prices:
            item_to_sell = item_input
            
        if item_to_sell:
            quantity = int(input(f"How many {item_to_sell} would you like to sell?: "))
            base_price = item_prices[item_to_sell]["price"]
            adjusted_price = int(base_price * price_multiplier)
            total_price = adjusted_price * quantity
            print(f"\nSold {quantity}x {item_to_sell} for {total_price} Glowstone!")
        else:
            print("That item cannot be sold!")
    
    def initiate_battle(self):
        #print("Choose a creature to fight:")
    
        #for creature in self.creature_templates:
            #print(f"{creature.abbreviation}: {creature.name}")

        creature_abbrev = input("Enter the abbreviation of the creature to battle: ").strip().upper()

        # Find the selected creature
        selected_creature = next((c for c in self.creature_templates if c.abbreviation == creature_abbrev), None)
        if not selected_creature:
            print("Invalid creature abbreviation.")
            return

        num_creatures = random.randint(1, 4)  # Roll for 1 to 4 of the selected creature
        self.creatures = [Creature(
            selected_creature.name,
            selected_creature.abbreviation,
            selected_creature.biome,
            selected_creature.damage,
            selected_creature.max_health,
            selected_creature.drops,
            selected_creature.exp_range,
            selected_creature.is_predator,
            selected_creature.status_effects
        ) for _ in range(num_creatures)]
        print("\n" * 21)
        print("\n--- Creatures Encountered ---")
        print(f"You will face {num_creatures} {selected_creature.name}(s)!")

        # Display the creatures being fought
        for creature in self.creatures:
            print(f"- {creature}")
        

        self.current_creature_index = 0  # Reset index for the new battle
        self.start_battle()

    def start_battle(self):
        current_creature = self.creatures[self.current_creature_index]
    
        # Display battle status
        print(f"\nBattle with {current_creature.name}")
        print(f"{current_creature.name}'s Health: {current_creature.health}")
        
        # Display each player's health
        for player in self.players:
            print(f"{player.name}'s Health: {player.health}")
        # Reset total drops and experience for the new battle
        self.total_drops = {}
        self.total_exp = 0

        # Ensure every creature starts with full health
        for creature in self.creatures:
            creature.reset_health()

        battle_ended = False
        while not battle_ended:
            self.update_temp_boosts()
            if self.current_creature_index >= len(self.creatures):
                print("All creatures have been defeated!")
                battle_ended = True
                break

            # Get the currently active creature
            active_creature = self.creatures[self.current_creature_index]

            # Check if the active creature is still alive
            while active_creature.health <= 0:
                print(f"{active_creature.name} has fallen!")
                self.current_creature_index += 1
                if self.current_creature_index >= len(self.creatures):
                    print("All creatures have been defeated!")
                    return  # End battle
                active_creature = self.creatures[self.current_creature_index]
            print("")
            print("\n--- Current Creature ---")
            print(f"\nYou are facing a {active_creature.name} with {active_creature.health} HP.")
            print("\n---                  ---")
            print("")
            # Player's turn to act
            for player in self.players:
                if player.health <= 0:  # Skip if the player is already defeated
                    continue
                
                # Apply status effects before the player's turn
                if not player.apply_status_effects():  # This must happen before the player acts

                    if player.health > 0:  # Allow only alive players to act
                        print(f"\n{player.name}'s turn!")
                        action = input("Enter an action: ").strip().lower()

                        if action == 'a':
                            # Directly target the active creature
                            target_creature = active_creature
                            # Calculate hit chance based on luck comparison
                            miss_chance = 0.15  # Base 5% miss chance for players
                            if player.luck < target_creature.luck:
                                luck_diff = target_creature.luck - player.luck
                                miss_chance += luck_diff * 0.08  # Each point of luck difference adds 8% miss chance
                                miss_chance = min(miss_chance, 0.75)  # Cap total miss chance at 40%
                            
                            # Check if attack misses
                            if random.random() < miss_chance:
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print("")
                                print(f"\n{player.name}'s attack misses {target_creature.name}!")
                                print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")

                                print("")
                                # Add the creature's attack message here
                                if active_creature.health > 0:
                                    damage_dealt = max(active_creature.damage - player.protection, 0)
                                    player.health -= damage_dealt
                                    print(f"{active_creature.name} attacks {player.name} for {damage_dealt} damage after protection!")
                                    print(f"{player.name}'s Health: {player.health}/{player.max_health}")
                                print("")
                                continue
                            
                            # Calculate damage considering player's damage stat
                            damage = player.damage

                            # 20% chance for critical hit
                            if random.random() <= 0.20:
                                damage *= 2  # Double the damage
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                            
                            # Apply damage to creature
                            target_creature.health -= damage
                            
                            # Print attack message
                            print("\n" * 21)
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print("")
                            print(f"{player.name} hits for {damage} damage!")
                            print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                            print("")
                            # Check if creature is defeated
                            if target_creature.health <= 0:
                                print(f"{target_creature.name} is defeated!")
                                
                                # Generate and display drops
                                drops, exp_gained = target_creature.generate_drops()
                                
                                # Update total drops
                                for item, quantity in drops.items():
                                    self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                
                                self.total_exp += exp_gained
                                
                                print(f"Drops gained: {drops}")
                                print(f"Experience gained: {exp_gained}")
                                
                                # Move to next creature
                                self.current_creature_index += 1
                                break



                        elif action == 's':
                            # Show current stats
                            print("\n" * 21)
                            print(f"\n=== {player.name}'s Current Stats ===")
                            print(f"Health: {player.health}/{player.max_health}")
                            print(f"Stamina: {player.stamina}/{player.max_stamina}")
                            print(f"Damage: {player.damage}")
                            print(f"Protection: {player.protection}")
                            print(f"Status Effects: {', '.join(player.status_effects) if player.status_effects else 'None'}")
                            print(f"\n===                               ===")
                            # Show active creature stats
                            print(f"\n=== {active_creature.name}'s Stats ===")
                            print(f"Health: {active_creature.health}/{active_creature.max_health}")
                            print(f"Damage: {active_creature.damage}")
                            print(f"\n===                               ===")
                            
                            # Allow another action after viewing stats
                            print(f"\n{player.name}'s turn!")
                            follow_up_action = input("Choose your action: ").strip().lower()
    
                            # Process the follow-up action by recursively calling the same action handling logic
                            if follow_up_action == 'a':
                                # Directly target the active creature
                                target_creature = active_creature
                                # Calculate hit chance based on luck comparison
                                miss_chance = 0.15  # Base 5% miss chance for players
                                if player.luck < target_creature.luck:
                                    luck_diff = target_creature.luck - player.luck
                                    miss_chance += luck_diff * 0.08  # Each point of luck difference adds 8% miss chance
                                    miss_chance = min(miss_chance, 0.75)  # Cap total miss chance at 40%
                                
                                # Check if attack misses
                                if random.random() < miss_chance:
                                    print("\n" * 21)
                                    print(f"\n--- Actions during {player.name}'s turn ---")
                                    print("")
                                    print(f"\n{player.name}'s attack misses {target_creature.name}!")
                                    print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                                    print("")

                                    # Add the creature's attack message here
                                    if active_creature.health > 0:
                                        damage_dealt = max(active_creature.damage - player.protection, 0)
                                        player.health -= damage_dealt
                                        print(f"{active_creature.name} attacks {player.name} for {damage_dealt} damage after protection!")
                                        print(f"Health: {target.health}")
                                    print("")
                                    continue
                                
                                # Calculate damage considering player's damage stat
                                damage = player.damage

                                # 20% chance for critical hit
                                if random.random() <= 0.20:
                                    damage *= 2  # Double the damage
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                    print(f"\n--- !!CRITICAL HIT!! THEIR ATTACK DOES DOUBLE DAMAGE ---")
                                
                                # Apply damage to creature
                                target_creature.health -= damage
                                
                                # Print attack message
                                print("\n" * 21)
                                print(f"\n--- Actions during {player.name}'s turn ---")
                                print("")
                                print(f"{player.name} hits for {damage} damage!")
                                print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                                print("")
                                # Check if creature is defeated
                                if target_creature.health <= 0:
                                    print(f"{target_creature.name} is defeated!")
                                    
                                    # Generate and display drops
                                    drops, exp_gained = target_creature.generate_drops()
                                    
                                    # Update total drops
                                    for item, quantity in drops.items():
                                        self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                    
                                    self.total_exp += exp_gained
                                    
                                    print(f"Drops gained: {drops}")
                                    print(f"Experience gained: {exp_gained}")
                                    
                                    # Move to next creature
                                    self.current_creature_index += 1
                                    break
                                
                                if target_creature.health <= 0:
                                    print(f"{target_creature.name} is defeated!")
                                    drops, exp_gained = target_creature.generate_drops()
                                    for item, quantity in drops.items():
                                        self.total_drops[item] = self.total_drops.get(item, 0) + quantity
                                    self.total_exp += exp_gained
                                    print(f"Drops gained: {drops}")
                                    print(f"Experience gained: {exp_gained}")
                                    self.current_creature_index += 1
                                    break
                            elif follow_up_action == 't':
                                target_player = self.choose_target(for_heal=True)
                                if target_player:
                                    player.triage(target_player)
                                
                            elif follow_up_action == 'as':
                                target_player = self.choose_target(for_heal=True)
                                if target_player:
                                    player.aid_surge(target_player)

                            elif follow_up_action == 'i':
                                player.iron_bastion()

                            elif follow_up_action == 'f':
                                player.fortify()

                            elif follow_up_action == 'eh':
                                target_player = self.choose_target()
                                if target_player:
                                    player.emergency_heal(target_player)

                            elif follow_up_action == 'bb':
                                target_player = self.choose_target()
                                if target_player:
                                    player.body_bash(target_player)

                            elif follow_up_action == 'p':
                                target_player = self.choose_target()
                                if target_player:
                                    player.power_attack(target_player)

                            elif follow_up_action == 'cp':
                                target_player = self.choose_target()
                                if target_player:
                                    player.critical_precision(target_player)
                                    
                            elif follow_up_action == 'pg':
                                target_player = self.choose_target()
                                if target_player:
                                    player.poison_gas(target_player)

                            elif follow_up_action == 'cb':
                                target_player = self.choose_target()
                                if target_player:
                                    player.crushing_blow(target_player)

                            elif follow_up_action == 'gs':
                                target_player = self.choose_target()
                                if target_player:
                                    player.guardian_slam(target_player)

                            elif follow_up_action == 'r':
                                target_player = self.choose_target()
                                if target_player:
                                    player.ravage(target_player)

                            elif follow_up_action == 'd':
                                target_player = self.choose_target()
                                if target_player:
                                    player.double_strike(target_player)

                            elif follow_up_action == 'ra':
                                player.rally()

                            elif follow_up_action == 'e':
                                if self.attempt_escape(player, active_creature):
                                    return  # End the battle if escape was successful
                                
                            elif follow_up_action == 'rn':
                                self.roar_of_need()
                                
                            elif follow_up_action == 'j':
                                self.join_new_player()
                                print(f"{player.name} can now take another action.")
                                break  # Break to allow the player to take an additional action

                            elif follow_up_action == 'ui':
                                self.use_item(player)  # Correctly pass the player to use_item
                            
                            else:
                                print("Invalid action.")
                                # Add other action handlers similarly
                            
                        elif action == 't':
                            target_player = self.choose_target(for_heal=True)
                            if target_player:
                                player.triage(target_player)
                                
                        elif action == 'as':
                            target_player = self.choose_target(for_heal=True)
                            if target_player:
                                player.aid_surge(target_player)

                        elif action == 'i':
                            player.iron_bastion()

                        elif action == 'f':
                            player.fortify()

                        elif action == 'eh':
                            target_player = self.choose_target()
                            if target_player:
                                player.emergency_heal(target_player)

                        elif action == 'bb':
                            target_player = self.choose_target()
                            if target_player:
                                player.body_bash(target_player)
                            
                        elif action == 'pg':
                            target_player = self.choose_target()
                            if target_player:
                                player.poison_gas(target_player)

                        elif action == 'p':
                            target_player = self.choose_target()
                            if target_player:
                                player.power_attack(target_player)

                        elif action == 'cp':
                            target_player = self.choose_target()
                            if target_player:
                                player.critical_precision(target_player)

                        elif action == 'cb':
                            target_player = self.choose_target()
                            if target_player:
                                player.crushing_blow(target_player)

                        elif action == 'gs':
                            target_player = self.choose_target()
                            if target_player:
                                player.guardian_slam(target_player)

                        elif action == 'r':
                            target_player = self.choose_target()
                            if target_player:
                                player.ravage(target_player)

                        elif action == 'd':
                            target_player = self.choose_target()
                            if target_player:
                                player.double_strike(target_player)

                        elif action == 'ra':
                            player.rally()

                        elif action == 'e':
                            if self.attempt_escape(player, active_creature):
                                return  # End the battle if escape was successful
                            
                        elif action == 'rn':
                            self.roar_of_need()
                            
                        elif action == 'j':
                            self.join_new_player()
                            print(f"{player.name} can now take another action.")
                            break  # Break to allow the player to take an additional action

                        elif action == 'ui':
                            self.use_item(player)  # Correctly pass the player to use_item
                        
                        else:
                            print("Invalid action.")

                # Creature's turn after all players have acted
                if active_creature.health > 0:
                    alive_players = [p for p in self.players if p.health > 0]
                    if not alive_players:  # If there are no alive players left
                        break

                    target_player = random.choice(alive_players)  # Choose a random alive player
                    active_creature.attack(player)  # Creatures attack players
                    
             # At the end of the battle loop, check if all creatures are defeated
            if all(creature.health <= 0 for creature in self.creatures):
                battle_ended = True
                break
            
            # Check if all players are defeated
            if all(player.health <= 0 for player in self.players):
                print("All players have been defeated!")
                battle_ended = True
                break

        # Call end_battle when the battle is over
        if battle_ended:
            self.end_battle()

                    

    def end_battle(self):
        for player in self.players:
            player.clear_temp_stats()
        for player_name, boosts in self.temp_boosts.items():
            if boosts['damage'] > 0 or boosts['protection'] > 0:
                player = next(p for p in self.players if p.name == player_name)
                player.damage -= boosts['damage']
                player.protection -= boosts['protection']
                boosts['damage'] = 0
                boosts['protection'] = 0
                boosts['turns_remaining'] = 0
        print("")
        print("")
        print("")
        print("\n--- End of Battle Stats ---")
        for player in self.players:
            # Show current player stats
            status_effects = ','.join(player.status_effects) if player.status_effects else "None"
            print("")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
            print("")
            print(f"Health: {player.health}/{player.max_health}")
            print(f"Stamina: {player.stamina}/{player.max_stamina}")
            print(f"Damage: {player.damage}")
            print(f"Protection: {player.protection}")
            print(f"Status Effects: {', '.join(player.status_effects) if player.status_effects else 'None'}")
            print("")
            print("")
            # Only remove 'daze' status effect after battle
            if 'daze' in player.status_effects:
                player.status_effects.remove('daze')
                print(f"Daze effect removed from {player.name}")

        # Show total drops and EXP from the battle
        print("\n--- Total Drops Gained ---")
        if self.total_drops:
            for item, amount in self.total_drops.items():
                print(f"{item}: {amount}")
        else:
            print("No drops were gained.")

        print(f"Total Experience Gained: {self.total_exp}")

        print("\n--- Items Used During Battle ---")
        if self.items_used:
            for item_name, count in self.items_used.items():
                print(f"{item_name}: {count}")
        else:
            print("No items were used.")


    def attempt_escape(self, player, active_creature):
        if random.random() < 0.4:  # 40% chance to escape
            print(f"{player.name} successfully escaped from {active_creature.name}!")
            print(f"\n=== PLAYER LINE ===")
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")
            print(f"\n=== PLAYER LINE ===")
            return True  # Return True to indicate the battle should end
        else:
            # Calculate damage when escape fails
            damage_dealt = max(active_creature.damage - player.protection, 0)
            player.health -= damage_dealt
            
            print(f"{player.name} failed to escape and takes {damage_dealt} damage from {active_creature.name}!")
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
            return False  # Return False to indicate the battle continues
