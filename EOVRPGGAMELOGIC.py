import random


# Ohm,200,200, 50, 50,50,5,1,15

# Define constants for status effects and travel outcomes
BLEED_DAMAGE = 5
BURN_DAMAGE = 3
POISON_DAMAGE = 3
SHADOW_SHROUD_DAMAGE = 5  
DAZE_PROBABILITY = 0.05

BURN_CHANCE = 0.02
BLEED_CHANCE = 0.03
POISON_CHANCE = 0.05
SHADOW_CHANCE = 0.05

BIOME_ABBREVIATIONS = {
    "Veilmarsh": "VM",
    "Shattered Plains": "SP",
    "Obsidian Dunes": "OD",
    "Gloom Peaks": "GP",
    "Cinderglade": "CG"
}

PLANT_ABBREVIATIONS = {
    "Fiber": "FBR",
    "Carrots": "CRT",
    "Leaves": "LVS",
    "Resin": "RSN",
    "Peas": "PEA",
    "Pulp": "PLP",
    "Shards": "SHD",
    "Essence": "ESS",
    "Frostshard Wood": "FSW",
    "Kale": "KLE",
    "Broccoli": "BRC",
    "Crystal": "CRY",
    "Emberbark": "EMB",
    "Asparagus": "ASP",
    "Radishes": "RAD"
}

class BountySystem:
    def __init__(self):
        # Define creature types and their base rewards
        self.creature_rewards = {
            "Murk Wraith": 10,
            "Sporefang": 10,
            "Crimson Cracker": 15,
            "Shadow Stalker": 15,
            "Gloom Thicket": 20,
            "Crystal Rabbit": 20,
            "Fissure Frolicker": 30,
            "Dune Dancer": 35,
            "Ashen Hopper": 30,
            "Charseed Buncher": 30,
            "Ember Revenant": 30,
            "Flamewretch": 30
        }
        
        # Define item types and their base rewards
        self.item_rewards = {
            "Essence": 5,
            "Pelt": 8,
            "Scale": 6,
            "Fissure Pulp": 7,
            "Obsidian Fang": 7,
            "Crystal": 8,
            "Emberbark": 9,
            "Feather": 6,
            "Hide": 7,
            "Claw": 9
        }
    
    def generate_bounty(self):
        bounty_type = random.choice(["combat", "delivery", "mixed"])
        
        if bounty_type == "combat":
            return self._generate_combat_bounty()
        elif bounty_type == "delivery":
            return self._generate_delivery_bounty()
        else:
            return self._generate_mixed_bounty()
    
    def _generate_combat_bounty(self):
        num_creatures = random.randint(2, 5)
        creature = random.choice(list(self.creature_rewards.keys()))
        base_reward = self.creature_rewards[creature]
        total_reward = base_reward * num_creatures * 1.02  # 20% bonus for combat
        
        return {
            "type": "combat",
            "task": f"Defeat {num_creatures} {creature}s",
            "reward": int(total_reward)
        }
    
    def _generate_delivery_bounty(self):
        num_items = random.randint(3, 8)
        item = random.choice(list(self.item_rewards.keys()))
        base_reward = self.item_rewards[item]
        total_reward = base_reward * num_items * 1.04  # 10% bonus for delivery
        
        return {
            "type": "delivery",
            "task": f"Deliver {num_items} {item}",
            "reward": int(total_reward)
        }
    
    def _generate_mixed_bounty(self):
        # Combine combat and delivery
        num_creatures = random.randint(1, 3)
        num_items = random.randint(2, 5)
        
        creature = random.choice(list(self.creature_rewards.keys()))
        item = random.choice(list(self.item_rewards.keys()))
        
        total_reward = (self.creature_rewards[creature] * num_creatures + 
                       self.item_rewards[item] * num_items) * 1.5  # 50% bonus for mixed
        
        return {
            "type": "mixed",
            "task": f"Defeat {num_creatures} {creature}s and collect {num_items} {item}",
            "reward": int(total_reward)
        }
    
    def get_available_bounties(self):
        """Generate 3 random bounties"""
        bounties = []
        for _ in range(3):
            bounties.append(self.generate_bounty())
        return bounties


# Define the creature class
class Creature:
    def __init__(self, name, abbreviation, biome, damage, health, drops, exp_range, is_predator, status_effects=[], special_ability=None):
        player.name = name
        self.abbreviation = abbreviation
        self.biome = biome
        self.damage = damage
        self.health = health
        self.max_health = health
        self.drops = drops  # A dictionary of item drops and their chances
        self.exp_range = exp_range  # Tuple for EXP range (min, max) for random EXP drop
        self.is_predator = is_predator
        self.status_effects = status_effects  # Define possible status effects for this creature
        self.special_ability = special_ability

    def __repr__(self):
        return f"{player.name} (Biome: {self.biome}) - Damage: {self.damage}, Health: {self.health}"

    def reset_health(self):
        """Reset the creature's health to its maximum value."""
        self.health = self.max_health

    def attack(self, target):
        # 20% chance to use special ability if one exists
        if self.special_ability and random.random() <= 0.20:
            self.use_special_ability(target)
            return
        """Attack the target and apply effects if applicable."""
        damage_dealt = max(self.damage - target.protection, 0)
        
        # Basic attack message
        print("")
        print(f"{player.name} attacks {target.name} for {damage_dealt} damage after protection!")
        print("\n---                   ---")
        print("")
        # Apply damage
        target.health -= damage_dealt
        
        # Apply status effects with proper list handling
        if hasattr(target, 'status_effects'):
            for effect in self.status_effects:
                if effect == 'poison' and 'poison' not in target.status_effects:
                    if random.random() < POISON_CHANCE:
                        target.status_effects.append('poison')
                        print(f"{player.name}'s venomous attack poisons {target.name}!")
                
                elif effect == 'bleeding' and 'bleeding' not in target.status_effects:
                    if random.random() < BLEED_CHANCE:
                        target.status_effects.append('bleeding')
                        print(f"{player.name}'s savage attack causes {target.name} to bleed!")
                elif effect == 'burn' and 'burn' not in target.status_effects:
                    if random.random() < BURN_CHANCE:
                        target.status_effects.append('burn')
                        print(f"{player.name}'s fiery scratch causes {target.name} to burn!")
                
                elif effect == 'shadow_shroud' and 'shadow shroud' not in target.status_effects:
                    if random.random() < SHADOW_CHANCE:
                        target.status_effects.append('shadow shroud')
                        print(f"{player.name}'s dark presence envelops {target.name} in shadows!")
        
        if target.health <= 0:
            print(f"{target.name} has been defeated!")

    def use_special_ability(self, target):
        if self.special_ability == "double_strike":
            damage = self.damage * 2
            print(f"{player.name} uses Double Strike for {damage} damage!")
            target.health -= damage
            
        elif self.special_ability == "quake_stomp":
            damage = self.damage * 1.5
            print(f"{player.name} uses Quake Stomp for {damage} damage!")
            target.health -= damage

        elif self.special_ability == "scorching_grasp":
            damage = self.damage * 3
            print(f"{player.name} uses Scorching Grasp for {damage} damage!")
            target.health -= damage

        elif self.special_ability == "reflective_dive":
            damage = self.damage * 2
            print(f"{player.name} attacks twice using Reflective Dive for {damage} damage!")
            target.health -= damage

        elif self.special_ability == "inferno_charge":
            damage = self.damage * 1.8
            print(f"{player.name} uses Inferno Charge for {damage} damage!")
            target.health -= damage
            
        elif self.special_ability == "life_drain":
            damage = int(self.damage * 1.5)
            heal = int(damage * 0.5)
            print(f"{player.name} uses Life Drain for {damage} damage and heals for {heal}!")
            target.health -= damage
            self.health = min(self.max_health, self.health + heal)
            
        elif self.special_ability == "tremor_stomp":
            damage = int(self.damage * 0.75)
            print(f"{player.name} uses Tremor Stomp for {damage} damage!")
            target.health -= damage
            if random.random() <= 0.5:  # 50% chance to stun
                target.status_effects.append('dazed')
                print(f"{target.name} is stunned!")


    def apply_status_effects(self, target):
        """Apply ongoing effects if applicable."""
        for effect in self.status_effects:
            if effect == 'poison' and 'poison' not in target.status_effects:
                if random.random() < POISON_CHANCE:
                    print(f"{player.name}'s venomous attack poisons {target.name}!")
                    target.status_effects.append('poison')
            
            elif effect == 'bleeding' and 'bleeding' not in target.status_effects:
                if random.random() < BLEED_CHANCE:
                    print(f"{player.name}'s savage attack causes {target.name} to bleed!")
                    target.status_effects.append('bleeding')
            
            elif effect == 'shadow_shroud' and 'shadow shroud' not in target.status_effects:
                if random.random() < SHADOW_CHANCE:
                    print(f"{player.name}'s dark presence envelops {target.name} in shadows!")
                    target.status_effects.append('shadow shroud')

    def generate_drops(self):
        """Generate drops based on drop percentages and return the total EXP earned."""
        drops_gained = {}
        for item, chance in self.drops.items():
            if random.random() < chance:
                quantity = random.randint(1, 3)  # Randomly determine a quantity (1 to 3) of the item to drop
                drops_gained[item] = drops_gained.get(item, 0) + quantity  # Increment the drop count
        
        # Generate EXP from the defined range
        exp_earned = random.randint(*self.exp_range)
        return drops_gained, exp_earned

class Plant:
    def __init__(self, name, biome, gather_chance, effects=None):
        player.name = name
        self.biome = biome
        self.gather_chance = gather_chance  # Chance to successfully gather (0.0 to 1.0)
        self.effects = effects or {}  # Dictionary of effects this plant can have
        

# Define the item class
class Item:
    def __init__(self, name, item_type, effect_value):
        player.name = name
        self.abbreviation = name[:2].upper()
        self.item_type = item_type  # "heal", "stamina", "both", "boost", "damage"
        self.effect_value = effect_value  # Value of the effect
    @classmethod
    def get_items(cls):
        return [
            cls("Healing Wraps", "remove_status", 35),  # Removed abbreviation parameter
            cls("Asparagus Pea Medley", "heal", 15),
            cls("Frostbitten Meal", "heal", 22),
            cls("Carrot Delight", "heal", 10),
            cls("Pea Salad", "heal", 8),
            cls("Asparagus Medley", "heal", 12),
            cls("Broccoli Fusion", "heal", 9),
            cls("Radish Medley", "heal", 6),
            cls("Kale Bowl", "heal", 8),
            cls("Meat Skewers", "heal", 18),
            cls("Kale Salad", "heal", 30),
            cls("Tiny Meat Stir", "heal", 16),
            cls("Roasted Tiny Meat", "heal", 5),
            cls("Roasted Medium Meat", "heal", 10),
            cls("Roasted Large Meat", "heal", 15),
            cls("Spore Balm", "remove_status", 30),
            cls("Embercool Salve", "remove_status", 25),
            cls("Vital Essence Wrap", "stamina", 50),
            cls("Revitalizing Grain Bar", "stamina", 30),
            cls("Mighty Elixir", "boost", 5),
            cls("Poison Gas", "damage", 10),
            cls("Purification Crystal", "cure_status", 0),
            cls("Etheric Infusion", "full_restore", 999),
            cls("Ironhide Tonic", "protection", 15)
            ]

    def use(self, target):
        if self.item_type == "remove_status":
                # Define which effects each item can remove
                effect_removers = {
                    "Healing Wraps": "bleeding",
                    "Spore Balm": "poison",
                    "Embercool Salve": "burn"
                }
                
                effect_to_remove = effect_removers.get(player.name)
                if effect_to_remove:  # Only proceed if we have a valid effect to remove
                    if effect_to_remove in target.status_effects:
                        target.status_effects.remove(effect_to_remove)
                        print(f"{target.name} uses {player.name} and removes the {effect_to_remove} status effect!")
                    else:
                        print(f"{target.name} doesn't have {effect_to_remove} status effect!")
                else:
                    print(f"{player.name} cannot remove any status effects!")
                    return

        if self.item_type == "protection":
            target.protection += self.effect_value
            print(f"{target.name} uses {player.name} and gains {self.effect_value} protection!")
        
        elif self.item_type == "full_restore":
            target.health = target.max_health
            target.stamina = target.max_stamina
            print(f"{target.name} uses {player.name} and fully restores all stats!")
            
        elif self.item_type == "cure_status":
            target.status_effects.clear()
            print(f"{target.name} uses {player.name} and removes all status effects!")
            
        elif self.item_type == "full_heal":
            target.health = target.max_health
            print(f"{target.name} uses {player.name} and fully restores HP!")
            
        elif self.item_type == "full_stamina":
            target.stamina = target.max_stamina
            print(f"{target.name} uses {player.name} and fully restores stamina!")
            
        elif self.item_type == "heal":
            target.health = min(target.max_health, target.health + self.effect_value)
            print(f"{target.name} uses {player.name} and heals {self.effect_value} HP!")
            
        elif self.item_type == "stamina":
            target.stamina = min(target.stamina + self.effect_value, target.max_stamina)  # Updated
            print(f"{target.name} uses {player.name} and recovers {self.effect_value} stamina!")

        elif self.item_type == "both":
            target.health = min(target.max_health, target.health + self.effect_value[0])
            target.stamina = min(target.stamina + self.effect_value[1], target.max_stamina)  # Updated
            print(f"{target.name} uses {player.name} and heals {self.effect_value[0]} HP and recovers {self.effect_value[1]} stamina!")

        elif self.item_type == "boost":
            target.damage += self.effect_value
            print(f"{target.name} uses {player.name} and increases their damage by {self.effect_value}!")

        elif self.item_type == "damage":
            target.health -= self.effect_value
            print(f"{target.name} uses {player.name} and takes {self.effect_value} damage!")


        status_effects = ','.join(target.status_effects) if target.status_effects else "None"
        print(f"{target.name},{target.max_health},{target.health},{target.stamina},{target.max_stamina},{target.luck},{target.protection},{target.light},{target.damage},{status_effects}")

class ShadowLottery:
    def __init__(self):
        self.prizes = {
            'Armor': ['Ethereal crown', 'Ethereal Robes', 'Ethereal Greaves', 'Shadow Hood', 'Shadow Cloak', 'Shadow Boots', 'Ashen Helm', 'Ashen Breastplate', 'Ashen Treads', 'Crimson Scale Helm', 'Crimson Scale Breastplate', 'Crimson Scale Legguards', 'Spectral Helm', 'Spectral Chesplate', 'Spectral Greaves', 'Obsidian Helm', 'Obsidian Breastplate', 'Obsidian Legguards'],
            'Weapons': ['Wraith Dagger', 'Crimson Longbow', 'Flamebrand Sword', 'Mirage Lantern'],
            'Accessories': ['Small Traveler’s Pouch', 'Medium Adventurer’s Pack', 'Large Explorer’s Satchel'],
            'Materials': ['Essence', 'Feather', 'Pelt', 'Hide', 'Claw', 'Fiber', 'leaves', 'scale', 'Resin', 'Pulp', 'Eye', 'Shards', 'Petal Essence', 'Nector', 'Obsidian Fang', 'Emberbark', 'Frostshard Wood', 'Crystal'],
            'Consumables': ['Healing Wraps', 'Spore Balm', 'Etheric Infusion', 'Embercool Salve'],
            'Food': ['Wraith-Warmed Root Stew', 'Ebon Asparagus and Shadow Pea Medley', 'Twilight Broccoli Bliss Bake', 'Frostbitten Vegetable Stir-Fry', 'Gloomy Carrot Delight', 'Shadow Pea Salad', 'Ebon Asparagus Medley', 'Twilight Broccoli Fusion', 'Cursed Radish Medley', 'Frosted Kale Bowl ', 'Shadow Pea & Tiny Meat Skewers', 'Grilled Medium Meat & Frosted Kale Salad', 'Cursed Radish & Tiny Meat Stir-Fry', 'Roasted Tiny Meat', 'Roasted Medium Meat', 'Roasted Large Meat']
        }
        
    def draw_lottery(self, num_draws=1):
        results = []
        for _ in range(num_draws):
            # Choose a random category
            category = random.choice(list(self.prizes.keys()))
            # Choose only one random item from that category
            item = random.choice(self.prizes[category])
            
            # 30% chance to get glowstone (between 100-1000)
            glowstone = random.randint(100, 400) if random.random() < 0.3 else 0
            
            results.append({
                'category': category,
                'item': item,
                'glowstone': glowstone
            })
        return results

class CraftingSystem:
    def __init__(self):
        # Define potion abbreviations in the CraftingSystem class
        self.recipes = {
            "HP": {  # Health Potion
                "ingredients": {
                    "Healing Herb": 2,
                    "Mountain Flower": 1
                },
                "success_rate": 0.8,
                "result_quantity": 1
            },
            "SP": {  # Stamina Potion
                "ingredients": {
                    "Prairie Grass": 2,
                    "Valley Mushroom": 1
                },
                "success_rate": 0.75,
                "result_quantity": 1
            },
            "SE": {  # Shadow Elixir
                "ingredients": {
                    "Shadow Root": 2,
                    "Highland Moss": 1
                },
                "success_rate": 0.6,
                "result_quantity": 1
            }
        }

    def craft_item(self, player, recipe_name, inventory):
        if recipe_name not in self.recipes:
            print(f"Recipe for {recipe_name} not found!")
            return False

        recipe = self.recipes[recipe_name]
        
        # Attempt crafting without checking or consuming ingredients
        if random.random() <= recipe["success_rate"]:
            print(f"Successfully crafted {recipe['result_quantity']} {recipe_name}!")
            return True
        else:
            print(f"Failed to craft {recipe_name}!")
            return False


# Define player character class
class PlayerCharacter:
    def __init__(self, name, max_health, health, stamina, max_stamina, luck, protection, light, damage, status_effects):
        player.name = name
        self.max_health = max_health
        self.health = health
        self.stamina = stamina
        self.max_stamina = max_stamina  # New attribute for max stamina
        self.luck = luck
        self.protection = protection
        self.light = light
        self.damage = damage
        self.status_effects = status_effects.split(';') if status_effects else []  # List to track status effects
        self.inventory = []  # Initialize inventory for items

    def __repr__(self):
        return f"{player.name}: HP={self.health}/{self.max_health}, Stamina={self.stamina}/{self.max_stamina}, Luck={self.luck}, Protection={self.protection}, Light={self.light}, Damage={self.damage}, Status Effects={self.status_effects}"

    @staticmethod
    def from_input():
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        data_line = input("Who is doing this action?): ")
        name, max_health, health, stamina, max_stamina, luck, protection, light, damage, *status_effects = data_line.split(",")
        return PlayerCharacter(
            name.strip(),
            int(max_health),
            int(health),
            int(stamina),
            int(max_stamina),  # Use the input for max stamina
            int(luck),
            int(protection),
            int(light),
            int(damage),
            ';'.join(status_effects).strip()  # Join back the effects if there are multiple
        )

    def heal(self, target):
        heal_amount = 20  # Base healing amount
        target.health = min(target.health + heal_amount, target.max_health)  # Prevent overhealing
        print(f"{player.name} heals {target.name} for {heal_amount} HP!")
        print(f"{target.name}'s health is now {target.health}/{target.max_health}")

    # Ability to heal another player or self
    def triage(self, target):
        if self.stamina >= 3:  # Cost of ability
            heal_amount = 25  # Amount to heal
            self.stamina -= 5  # Cost of ability
            target.health = min(target.max_health, target.health + heal_amount)
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} uses TRIAGE and heals {target.name} for {heal_amount} HP!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to use TRIAGE!")

    def aid_surge(self, target):
        if self.stamina >= 3:  # Cost of ability
            heal_amount = 50  # Amount to heal
            self.stamina -= 20  # Cost of ability
            target.health = min(target.max_health, target.health + heal_amount)
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} uses AID SURGE and heals {target.name} for {heal_amount} HP!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to use AID SURGE!")
# double_strike
    # Ability to add protection
    def fortify(self):
        if self.stamina >= 3:  # Cost of ability
            self.stamina -= 3
            additional_protection = 5  # Extra protection
            self.protection += additional_protection
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} uses FORTIFY and gains {additional_protection} protection!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to use FORTIFY!")

    def iron_bastion(self):
        if self.stamina >= 5:  # Cost of ability
            self.stamina -= 5
            additional_protection = 10  # Extra protection
            self.protection += additional_protection
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} uses IRON BASTION and gains {additional_protection} protection!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to use IRON BASTION!")

    # Power attack ability for extra damage
    def power_attack(self, target):
        if self.stamina >= 7:  # Cost of ability
            self.stamina -= 7
            extra_damage = 10  # Extra damage
            total_damage = self.damage + extra_damage
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} performs a power attack on {target.name} for {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to perform a power attack!")

    def critical_precision(self, target):
        if self.stamina >= 7:  # Cost of ability
            self.stamina -= 7
            extra_damage = 15  # Extra damage
            total_damage = self.damage + extra_damage
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} performs a CRITICAL PRECISION on {target.name} for {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to perform a CRITICAL PRECISION!")

    def crushing_blow(self, target):
        if self.stamina >= 15:  # Cost of ability
            self.stamina -= 15
            extra_damage = 30  # Extra damage
            total_damage = self.damage + extra_damage
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} performs a CRUSHING BLOW on {target.name} for {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to perform a CRUSHING BLOW!")

    def ravage(self, target):
        if self.stamina >= 20:  # Cost of ability
            self.stamina -= 20
            damage_per_hit = self.damage
            total_damage = damage_per_hit * 3
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} RAVAGES {target.name} and deals {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to use RAVAGE!")
    
    # Double strike ability to attack twice
    def double_strike(self, target):
        if self.stamina >= 6:  # Cost of ability
            self.stamina -= 6
            damage_per_hit = self.damage
            total_damage = damage_per_hit * 2
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} hits {target.name} with a DOUBLE STRIKE for {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to perform a DOUBLE STRIKE!")
    def guardian_slam(self, target):
        if self.stamina >= 10:  # Cost of ability
            self.stamina -= 10
            damage_per_hit = self.damage
            total_damage = damage_per_hit * 3
            target.health -= total_damage
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} uses GUARDIAN SLAM and deals {total_damage} damage!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to perform a GUARDIAN SLAM!")

    # Rally ability to boost another player's damage
    def rally(self, target):
        if self.stamina >= 4:  # Cost of ability
            self.stamina -= 4
            damage_boost = 5  # Extra damage
            target.damage += damage_boost
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} rallies {target.name}, increasing their damage by {damage_boost}!")
        else:
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print("")
            print(f"\n--- Actions during {player.name}'s turn ---")
            print(f"{player.name} does not have enough stamina to rally!")

    # Use an item
    def use_item(self, item):
        item.use(self)

    def apply_status_effects(self):
        """Apply ongoing effects like bleeding, poison, or shadow shroud, if active."""
        damage_taken = 0

        if 'shadow shroud' in self.status_effects:
            damage_taken += SHADOW_SHROUD_DAMAGE
            print(f"{player.name} is under Shadow Shroud and loses {SHADOW_SHROUD_DAMAGE} HP!")

        if 'bleeding' in self.status_effects:
            damage_taken += BLEED_DAMAGE
            print(f"{player.name} is bleeding and loses {BLEED_DAMAGE} HP!")

        if 'burn' in self.status_effects:
            damage_taken += BURN_DAMAGE
            print(f"{player.name} is burning and loses {BLEED_DAMAGE} HP!")

        if 'poison' in self.status_effects:
            damage_taken += POISON_DAMAGE
            print(f"{player.name} is poisoned and loses {POISON_DAMAGE} HP!")

        # Apply the total damage taken
        self.health -= damage_taken

        # Check for dazed status and handle it
        if 'dazed' in self.status_effects:
            print(f"{player.name} is dazed and cannot act this turn.")
            # Remove dazed status after it has been processed
            self.status_effects.remove('dazed')
            return True  # Indicate that the player cannot act

        return False  # Indicate that the player can act

# Battle system
class Battle:
    def __init__(self, players):
        self.players = players
        self.creatures = []
        self.current_creature_index = 0  # Track which creature is currently active
        self.total_drops = {}  # To store total drops from this battle
        self.total_exp = 0  # To store total experience gained in this battle
        self.items_used = {}

        # Create items
        self.items = [
            Item("Asparagus Pea Medley ", "heal", 15),
            Item("Frostbitten ", "heal", 22),
            Item("Carrot Delight", "heal", 10),
            Item("Pea Salad", "heal", 8),
            Item("Asparagus Medley", "heal", 12),
            Item("Fusion", "heal", 9),
            Item("Radish Medley", "heal", 6),
            Item("Kale Bowl", "heal", 8),

            Item("Meat Skewers", "heal", 18),
            Item("Medium Meat & Frosted Kale Salad", "heal", 30),
            Item("Tiny Meat Stir", "heal", 16),
            Item("R Tiny Meat", "heal", 5),
            Item("R Medium Meat", "heal", 10),
            Item("R Large Meat", "heal", 15),

            Item("Healing Wraps", "remove_status", 35),  # Heals 20 HP
            Item("Spore Balm", "remove_status", 30),
            Item("Stamina Potion", "stamina", 15),  # Restores 15 stamina
            Item("Rage-Fused Binding", "boost", 15),
            Item("Adrenaline Bar", "boost", 10),  # Boosts damage by 5
            Item("Poison Gas", "damage", 10),  # Deals 10 damage to a target
            Item("Purification Crystal", "cure_status", 0),  # Removes all status effects

            Item("Etheric Infusion", "full_restore", 999),  # Fully restores HP and stamina
            Item("Embercool Salve", "remove_status", 25)  # New item for single status removal
        ]

        # Define creatures with possible status effects and EXP ranges
        self.creature_templates = [
            Creature("Shadow Stalker", "SS", "Veilmarsh", 5, 65, 
                    {"tiny meat": 0.5, "fiber": 0.3, "leaves": 0.2, "fur": 0.2}, 
                    (10, 20), True, ['bleeding'], 
                    special_ability="double_strike"),
            Creature("Murk Wraith", "MW", "Veilmarsh", 10, 50, 
                    {"essence": 0.5,"feather": 0.2}, 
                    (10, 20), True, ["bleeding"], 
                    special_ability=""),
            Creature("Gloom Thicket", "GT", "Veilmarsh", 3, 70, 
                    {"tiny meat": 0.5,"leaves": 0.2}, 
                    (10, 20), False, [], 
                    special_ability=""),
            Creature("Sporefang", "SP", "Veilmarsh", 11, 40, 
                    {"pelt": 0.5,"claw": 0.2}, 
                    (10, 20), True, ["poison"],
                     special_ability=""),
            
            Creature("Crystal Rabbit", "CR", "Shattered Plains", 7, 100, 
                    {"tiny meat": 0.7,"resin": 0.2,"fur":0.8}, 
                    (10, 20), False, [], 
                    special_ability=""),
            Creature("Fissure Frolicker", "FF", "Shattered Plains", 8, 140, 
                    {"medium meat": 0.7,"pulp": 0.2,"pelt":0.8}, 
                    (10, 20), True, ["poison"], 
                    special_ability=""),
            Creature("Crimson Cracker", "CC", "Shattered Plains", 11, 100, 
                    {"scale": 0.7,"claw": 0.2}, 
                    (10, 20), False, [], 
                    special_ability="quake_stomp"),
            Creature("Dune Dancer", "DD", "Shattered Plains", 8, 140, 
                    {"scale": 0.7,"pelt":0.8}, 
                    (10, 20), False, [], 
                    special_ability=""),
            
            Creature("Ashen Hopper", "AH", "Cinderglade", 10, 200, 
                    {"tiny meat": 0.7,"fiber": 0.8}, 
                    (10, 20), False, [], 
                    special_ability=""),
            Creature("Charseed Buncher", "CB", "Cinderglade", 10, 210, 
                    {"tiny meat": 0.7,"emberbark": 0.4}, 
                    (10, 20), False, [], 
                    special_ability="life_drain"),
            Creature("Ember Revenant", "ER", "Cinderglade", 14, 78, 
                    {"hide": 0.7,"scale": 0.8}, 
                    (10, 20), True, ["burn"], 
                    special_ability=""),
            Creature("Flamewretch", "FW", "Cinderglade", 10, 210, 
                    {"hide": 0.7,"claw": 0.4}, 
                    (10, 20), True, ["burn"], 
                    special_ability=""),

            Creature("Silhouette Slinker", "SSL", "Obsidian Dunes", 3, 230, 
                    {"tiny meat": 0.7,"shards": 0.8}, 
                    (10, 20), False, [], 
                    special_ability=""),
            Creature("Cinder Wisp", "CW", "Obsidian Dunes", 5, 300, 
                    {"medium meat": 0.6,"fur": 0.4,"essence":0.5}, 
                    (40, 120), False, [''], 
                    special_ability="inferno_charge"),
            Creature("Mirage Stalker", "MS", "Obsidian Dunes", 10, 250, 
                    {"pelt": 0.7,"claw": 0.8,"Obsidian Fragment":0.4}, 
                    (10, 20), False, [], 
                    special_ability=""),
            Creature("Reflex Vulture", "RV", "Obsidian Dunes", 8, 230, 
                    {"eye": 0.6,"feather": 0.4}, 
                    (40, 120), False, [''], 
                    special_ability="reflective_dive"),

            Creature("Cloudwalker", "CWA", "Gloom Peaks", 5, 300, 
                    {"tiny meat": 0.6,"frostshard wood": 0.4,"feather":0.5}, 
                    (40, 120), False, [''], 
                    special_ability=""),        
            Creature("Peak Nibbler", "PN", "Gloom Peaks", 25, 70, 
                    {"medium meat": 0.6, "wool": 0.4,"crystal":0.4}, 
                    (40, 120), False, [''], 
                    special_ability=""),
            Creature("Shadowdrake", "SD", "Gloom Peaks", 14, 300, 
                    {"scale": 0.6,"claw": 0.4,"feather":0.5}, 
                    (40, 120), False, [''], 
                    special_ability=""),        
            Creature("Sable Maw", "SM", "Gloom Peaks", 10, 360, 
                    {"pelt": 0.6, "bone": 0.4,"obsidian Fang":0.4}, 
                    (40, 120), True, [''], 
                    special_ability="tremor_stomp")
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
            "Veilmarsh": 0.3,    # 30% chance to encounter creatures
            "Shattered Plains": 0.4, # 40% chance to encounter creatures
            "Obsidian Dunes": 0.2 # 20% chance to encounter creatures
        }

        self.biomes = {
            "Veilmarsh": self.creature_templates[:1],  # Only Wolves
            "Obsidian Dunes": self.creature_templates[1:2],  # Only Bears
            "Shattered Plains": self.creature_templates[2:3],  # Only Deer
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

    def show_bounties(self):
        bounty_system = BountySystem()
        available_bounties = bounty_system.get_available_bounties()
    
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
            return selected_bounty
        return None


    def hunt_prey(self):
    # Dictionary of prey types and their point values
        prey_types = {
            "Pup": (1, 5),
            "Pangolin": (5, 10),
            "Wispfly": (10, 20),
            "Shardlizard": (15, 25)
        }
        
        # Get prey type from user
        print("Available prey:", ", ".join(prey_types.keys()))
        prey = input("What prey are you hunting? ").lower()
        
        if prey not in prey_types:
            print("That prey is not available to hunt!")
            return
        
        # Get number of prey to hunt
        try:
            num_prey = int(input("How many would you like to hunt? "))
            if num_prey < 1:
                print("You must hunt at least 1!")
                return
        except ValueError:
            print("Please enter a valid number!")
            return
            
        # Track successful hunts and total glowstone
        successful_hunts = 0
        total_glowstone = 0
        
        # Hunt the specified number of prey
        for i in range(num_prey):
            # Randomly determine which direction prey runs
            prey_direction = random.choice(["left", "right"])
            
            # Get player's guess
            guess = input(f"\nPrey #{i+1} is running! Guess left or right: ").lower()
            
            if guess == prey_direction:
                print("Success! You caught the prey!")
                successful_hunts += 1
                # Award random glowstone within prey's range
                glowstone = random.randint(*prey_types[prey])
                total_glowstone += glowstone
                print(f"You earned {glowstone} glowstone!")
            else:
                print(f"The prey got away! It ran {prey_direction}!")
                
        # Display results        
        print(f"\nHunting Results:")
        print(f"Prey Caught: {successful_hunts}/{num_prey}")
        print(f"Total Glowstone Earned: {total_glowstone}")

    def craft_menu(self, player):
        crafting = CraftingSystem()
        
        while True:
            print("\n=== Crafting Menu ===")
            print("Available Recipes:")
            for recipe, details in crafting.recipes.items():
                print(f"\n{recipe}:")
                print("Ingredients needed:")
                for ingredient, amount in details["ingredients"].items():
                    print(f"- {ingredient}: {amount}")
                print(f"Success Rate: {details['success_rate']*100}%")
                print(f"Creates: {details['result_quantity']}")

            print("\n1. Craft Item")
            print("2. View Inventory")

            choice = input("Choose an option: ")

            if choice == "1":
                recipe_name = input("Enter the name of the item to craft: ")
                crafting.craft_item(player, recipe_name, player.inventory)
            elif choice == "2":
                break
            else:
                print("Invalid option!")

    def shadow_lottery(self):
        lottery = ShadowLottery()
    
        print("\n=== SHADOW LOTTERY ===")
        print("How many draws would you like? (Each draw gives one item and a chance for glowstone)")
        
        try:
            num_draws = int(input("Enter number of draws: "))
            if num_draws < 1:
                print("Must draw at least once!")
                return
                
            results = lottery.draw_lottery(num_draws)
            
            print("\n=== LOTTERY RESULTS ===")
            for i, result in enumerate(results, 1):
                print(f"\nDraw #{i}:")
                print(f"Category: {result['category']}")
                print(f"Item won: {result['item']}")
                if result['glowstone'] > 0:
                    print(f"Bonus: {result['glowstone']} glowstone!")
                
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
        else:
            print(f"\nFailed to gather {selected_plant}")

        # Inside gather_plants method, replace the creature encounter section with:
        if random.random() < self.gathering_encounter_chances[full_biome]:
            creatures = self.biomes[full_biome]
            num_creatures = random.randint(1, 2)
            
            # Create the creature instances
            self.creatures = [Creature(
                creature.name,
                creature.abbreviation,
                creature.biome,
                creature.damage,
                creature.health,
                creature.drops,
                creature.exp_range,
                creature.is_predator,
                creature.status_effects
            ) for creature in random.choices(creatures, k=num_creatures)]
            
            # Display encounter message with specific details
            creature_counts = {}
            for creature in self.creatures:
                creature_counts[creature.name] = creature_counts.get(creature.name, 0) + 1
            
            encounter_message = "\nDuring gathering, you've encountered: "
            encounter_details = [f"{count} {name}" for name, count in creature_counts.items()]
            print(encounter_message + ", ".join(encounter_details) + "!")
            
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
            action = input("What are you doing?").strip().lower()

            if action == 'b':
                if not self.players:  # If no players exist
                    self.prompt_for_players()
                
                if self.players:  # Proceed with battle if players exist
                    self.initiate_battle()
                    continue  # Continue the loop for the next action
                
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
                
            elif choice == '2':
                player.stamina = min(player.stamina + 25, player.max_stamina)
                print(f"{player.name} gets some sleep and recovers 25 stamina. Current stamina: {player.stamina}/{player.max_stamina}")
                
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
        """Handle player traveling from one biome to another."""
        starting_biome = input("Where are you starting from?: ").strip().capitalize()
        
        if starting_biome not in self.biomes:
            print("Invalid starting biome. Please choose a valid biome.")
            return

        destination_biome = input("Which biome would you like to travel to?: ").strip().capitalize()
        
        if destination_biome not in self.biomes:
            print("Invalid destination biome. Please choose a valid biome.")
            return

        stamina_cost = self.travel_costs.get((starting_biome, destination_biome))

        if stamina_cost is None:
            print(f"You cannot travel from {starting_biome} to {destination_biome}.")
            return

        if player.stamina < stamina_cost:
            print(f"{player.name} does not have enough stamina to travel to {destination_biome}.")
            return
        
        player.stamina -= stamina_cost
        print(f"{player.name} travels from {starting_biome} to {destination_biome} and it takes {stamina_cost} stamina.")

        encounter_chance = random.randint(1, 100)

        if encounter_chance <= 20: 
            print("During travel, you encountered bad weather, losing 10 stamina.")
            player.stamina -= 10
            if player.stamina < 0:
                print(f"{player.name} cannot continue and the travel failed due to low stamina!")
                return

        elif encounter_chance <= 50:
            event_type = random.choice(["cache", "healer"])
            if event_type == "cache":
                print("During travel, you found a hidden cache and received a free prize!")
            elif event_type == "healer":
                player.health = player.max_health
                player.stamina = player.max_stamina  
                print(f"During travel, you encountered a healer who restored all your stats to full!")
                print(f"{player.name}'s stats are now: HP={player.health}/{player.max_health}, Stamina={player.stamina}/{player.max_stamina}")

        else:
            # Clear the creatures list before encountering new creatures
            self.creatures.clear()
            
            # Generates new creatures for the encounter
            creatures = self.biomes[destination_biome]
            num_creatures = random.randint(1, 3)  
            
            self.creatures = [Creature(
                creature.name,
                creature.abbreviation,
                creature.biome,
                creature.damage,
                creature.health,
                creature.drops,
                creature.exp_range,
                creature.is_predator,
                creature.status_effects
            ) for creature in random.choices(creatures, k=num_creatures)]
            
            # Reset health for each encountered creature before the battle starts
            for creature in self.creatures:
                creature.reset_health()  

            print(f"During travel, you encountered {len(self.creatures)} creatures!")
            
            # Start the battle with the encountered creatures
            self.start_battle()

    def use_item(self, player):
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print(f"\n--- Actions during {player.name}'s turn ---")
        print("")
        print("Choose an item to use by typing its abbreviation:")
        #for item in self.items:
            #print(f"{item.abbreviation} - {item.name} ({item.item_type})")

        abbrev = input("Enter item abbreviation: ").upper()
        item = next((i for i in self.items if i.abbreviation == abbrev), None)
        
        if item:
            player.use_item(item)
            self.items_used[item.name] = self.items_used.get(item.name, 0) + 1
        else:
            print("Item not found.")

    def choose_target(self, for_heal=False):
        """Get target character for abilities, including players and creatures."""
        print("Choose a target:")

        # List players
        for index, player in enumerate(self.players):
            if player.health > 0:  # Only list alive players
                print(f"{index + 1}: {player.name} (Player)")

        # List creatures
        for index, creature in enumerate(self.creatures):
            if creature.health > 0:  # Only list alive creatures
                print(f"{len(self.players) + index + 1}: {creature.name} (Creature)")

        target_index = int(input("Enter the number of the target: ")) - 1

        # Determine if the target is a player or a creature
        if target_index < len(self.players):
            # Target is a player
            if 0 <= target_index < len(self.players) and self.players[target_index].health > 0:
                if for_heal:
                    return self.players[target_index]  # Return target for healing
                return self.players[target_index]  # Return chosen target for attacks
        else:
            # Target is a creature
            creature_index = target_index - len(self.players)
            if creature_index >= 0 and creature_index < len(self.creatures) and self.creatures[creature_index].health > 0:
                return self.creatures[creature_index]  # Return chosen target (creature)

        print("Invalid target.")
        return None  # Return None if no valid target is selected

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
            selected_creature.health,
            selected_creature.drops,
            selected_creature.exp_range,
            selected_creature.is_predator,
            selected_creature.status_effects
        ) for _ in range(num_creatures)]

        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("")
        print("\n--- Creatures Encountered ---")
        print(f"You will face {num_creatures} {selected_creature.name}(s)!")

        # Display the creatures being fought
        for creature in self.creatures:
            print(f"- {creature}")
        

        self.current_creature_index = 0  # Reset index for the new battle
        self.start_battle()

    def start_battle(self):
        # Reset total drops and experience for the new battle
        self.total_drops = {}
        self.total_exp = 0

        # Ensure every creature starts with full health
        for creature in self.creatures:
            creature.reset_health()

        battle_ended = False
        while not battle_ended:
            if self.current_creature_index >= len(self.creatures):
                print("All creatures have been defeated!")
                battle_ended = True
                break

            # Get the currently active creature
            active_creature = self.creatures[self.current_creature_index]

            # Check if the active creature is still alive
            while active_creature.health <= 0:
                print(f"{active_creature.name} has already been defeated!")
                self.current_creature_index += 1
                if self.current_creature_index >= len(self.creatures):
                    print("All creatures have been defeated!")
                    return  # End battle
                active_creature = self.creatures[self.current_creature_index]
            print("")
            print("\n--- Current Creature ---")
            print(f"\nYou are facing {active_creature.name} with {active_creature.health} HP.")
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
                        action = input("Choose an action (stats/attack/defend/run/join/use_item/heal/protect/power/double/rally): ").strip().lower()

                        if action == 'a':
                            # Directly target the active creature
                            target_creature = active_creature
                            
                            # Calculate damage considering player's damage stat
                            damage = player.damage

                            # 20% chance for critical hit
                            if random.random() <= 0.20:
                                damage *= 2  # Double the damage
                                print(f"CRITICAL HIT! {player.name}'s attack deals double damage!")
                            
                            # Apply damage to creature
                            target_creature.health -= damage
                            
                            # Print attack message
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print(f"\n--- Actions during {player.name}'s turn ---")
                            print("")
                            print(f"{player.name} attacks {target_creature.name} for {damage} damage!")
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
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
                            print("")
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
                            follow_up_action = input("Choose your action (attack/defend/run/join/use_item/heal/protect/power/double/rally): ").strip().lower()
    
                            # Process the follow-up action by recursively calling the same action handling logic
                            if follow_up_action == 'a':
                                target_creature = active_creature
                                damage = player.damage
                                target_creature.health -= damage
                                print(f"{player.name} attacks {target_creature.name} for {damage} damage!")
                                print(f"{target_creature.name} has {target_creature.health}/{target_creature.max_health} HP remaining!")
                                
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

                            elif follow_up_action == 'p':
                                target_player = self.choose_target()
                                if target_player:
                                    player.power_attack(target_player)

                            elif follow_up_action == 'cp':
                                target_player = self.choose_target()
                                if target_player:
                                    player.critical_precision(target_player)

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
                                target_player = self.choose_target()
                                if target_player:
                                    player.rally(target_player)

                            elif follow_up_action == 'e':
                                if self.attempt_escape(player, active_creature):
                                    return  # End the battle if escape was successful

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
                            target_player = self.choose_target()
                            if target_player:
                                player.rally(target_player)

                        elif action == 'e':
                            if self.attempt_escape(player, active_creature):
                                return  # End the battle if escape was successful

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
        print("\n--- End of Battle Stats ---")
        for player in self.players:
            # Show current player stats
            status_effects = ','.join(player.status_effects) if player.status_effects else "None"
            print(f"{player.name},{player.max_health},{player.health},{player.stamina},{player.max_stamina},{player.luck},{player.protection},{player.light},{player.damage},{status_effects}")

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
            return True  # Return True to indicate the battle should end
        else:
            damage_dealt = max(active_creature.damage - player.protection, 0)
            print(f"{player.name} failed to escape and takes {damage_dealt} damage from {active_creature.name}!")
            player.health -= damage_dealt
            if player.health <= 0:
                print(f"{player.name} has been defeated!")
            return False  # Return False to indicate the battle continues

# Main Execution
players = []  # Start with an empty list of players

# Initialize battle
battle = Battle(players)

# Start the game and prompt for actions immediately
battle.choose_action()

