from random import *
from get_type import *
import keyboard
import os


# The `Clear_screen` class is designed to clear the terminal screen in a platform-independent way
# using the `os` module in Python.
class Clear_screen:
    import os
    def __init__(self) -> None:
        if os.name == "nt":
            self.do = "cls"
        else:
            self.do = "clear"
    
    def __call__(self):
        os.system(self.do)


clear_screen = Clear_screen()

# This Python class `Select_item` allows users to navigate and select items from a list using keyboard
# inputs for up and down movements.
class Select_item:
    def __init__(self, output, items) -> None:
        self.output: list[str] = output
        self.items: str = items
        self.select = 0

        
    def up(self):
        clear_screen()
        self.select = max(self.select - 1, 0)

        print(self.output)
            
        for i in range(len(self.items)):
            if i == self.select:
                print(f" > {self.items[i]}")
            else:
                print(f" - {self.items[i]}")
    
    def down(self):
        clear_screen()
        self.select = min(self.select + 1, len(self.items) - 1)


        print(self.output)
            
        for i in range(len(self.items)):
            if i == self.select:
                print(f" > {self.items[i]}")
            else:
                print(f" - {self.items[i]}")
    
    def __call__(self) -> int:
        clear_screen()
        print(Colors.orange, end="")

        print(self.output)
            
        for i in range(len(self.items)):
            if i == self.select:
                print(f" > {self.items[i]}")
            else:
                print(f" - {self.items[i]}")

        
        up = keyboard.add_hotkey("up arrow", self.up)
        down = keyboard.add_hotkey("down arrow", self.down)

        input()

        keyboard.remove_hotkey(up)
        keyboard.remove_hotkey(down)

        return self.select

# The `Colors` class defines various color and text formatting codes for use in terminal output.
class Colors:
    reset="\033[0m"
    revers="\u001b[7m"
    under_line="\u001b[4m"
    bold="\u001b[1m"

    orange="\033[33m"
    purple="\033[35m"
    blue="\033[34m"
    red="\033[31m"
    green="\033[32m"

    back_cyan="\u001b[46;1m"

# The `Creature` class represents a creature with attributes like health, damage, armor, and methods
# for attacking and taking damage in a turn-based combat system.
class Creature:
    def __init__(self, attributes, items=[]) -> None:
        self.name: str = attributes[0]
        self.health: int = attributes[1]
        self.max_health: int = attributes[1]
        self.damage: int = attributes[2]
        self.armor_rating: int = attributes[3]
        self.regen: int = attributes[4]
        self.enemys: list[Creature] = []

        self.xp = attributes[5]
        self.level = 1

        self.anti_armor = attributes[6]

        self.items: list = items
    
    def hurt(self, damage: int, attacker, anti_armor=0) -> bool:
        """
        This Python function calculates damage dealt to a character, reduces health accordingly, handles
        attacker information, grants experience points, and transfers items upon defeating the
        character.
        
        :param damage: The `damage` parameter in the `hurt` method represents the amount of damage that
        will be inflicted on the target entity (self). It is an integer value indicating the strength of
        the attack
        :type damage: int
        :param attacker: The `attacker` parameter in the `hurt` method represents the entity or object
        that is causing damage to the entity on which the method is being called. It is used to keep
        track of who is attacking the entity and can be used to perform actions related to the attacker,
        such as gaining
        :param anti_armor: The `anti_armor` parameter in the `hurt` method represents the amount of
        armor penetration or reduction that the attacker has. It is used to calculate the actual damage
        dealt to the target after considering the target's armor rating and the attacker's anti-armor
        value. By subtracting the `anti, defaults to 0 (optional)
        :return: The `hurt` method returns a boolean value. It returns `True` if the health of the
        entity being attacked (`self`) drops to 0 or below, indicating that the entity has been
        defeated. In this case, the method also transfers experience points (`xp`) from the defeated
        entity to the attacker, and transfers any items the defeated entity had to the attacker.
        """
        damage = max((damage / max(self.armor_rating - anti_armor, 1)), 0.5) # applying armor damage reduction and amking sure no less than 0.5 damige is delt
        self.health -= damage

        print(f"{attacker} attacked {self} for {round(damage, 3)} damage\n")
        print(f"{self} has {round(self.health, 3)}HP\n")

        # if it's a new attacker
        if attacker not in self.enemys:
            self.enemys.append(attacker)

        # if the attacked is dead
        if self.health <= 0:
            attacker.xp += self.xp
            print(f"{attacker} ({round((attacker.health), 3)}HP) got {self.xp}xp\n")
            print(f"{attacker} now has {attacker.xp}xp\n")

            # giving the attacker the items self has
            if len(self.items) > 0:
                for item in self.items:
                    attacker.items.append(item)
                    print(f"{attacker} got {item[0]}")
            return True
        return False

    # attacking 
    def attack(self, hit, damage=None) -> bool:
        # if there is no enemys in it's list
        if len(self.enemys) <= 0:
            return 
        
        if damage == None:
            damage = self.damage
        
        # if there was a specific creature to be attacked it will run on them else it will chose a random
        if hit == None:
            enemy: Creature = choice(seq=self.enemys)
        else:
            enemy: Creature = self.enemys[hit]

        # hurting the enemy and printing the result 
        if enemy.hurt(damage, self):
            self.enemys.remove(enemy)
            return True
        return False

    def __str__(self) -> str:
        return self.name

class Player(Creature):
    # giving the player the unique stats
    def __init__(self, attributes: list, ) -> None:
        self.name: str = attributes[0]

        self.xp: int = int(attributes[1])
        self.level: int = int(attributes[2])
        self.xp_need: int = 20 + (5 * self.level)

        self.health: int = int(attributes[3])
        self.max_health: int = int(attributes[4])
        self.regen: int = int(attributes[5])
        self.damage_multi: float = float(attributes[6])
        self.damage: int = 5

        self.enemys: list[Creature] = []

        self.items: list = attributes[7]

        self.armor = attributes[8]
        self.weapon = attributes[9]
        self.anti_armor = 0
        self.armor_rating = 1

        if self.weapon != None:
            self.damage += self.weapon[2] 
            self.damage = round(number=(self.damage * self.damage_multi), ndigits=3)
            self.anti_armor = self.weapon[3]
        else: 
            self.damage = self.damage * self.damage_multi

        if self.armor != None:
            self.armor_rating += self.armor[2]

    def heal(self, regen=0) -> None:
        if regen == 0:
            regen = self.regen

        self.health = (self.health + regen)
        self.health = min(max(self.health, 0), self.max_health)

        print(f"{self} healed for {regen}")
        print(f"{self} has {self.health}HP")
    
    def level_up(self):
        stat = Select_item(output=f"""{Colors.orange}Do you want to upgrade:""", 
                           items=[f"R: regen {self.regen} -> {self.regen + 5}",
    f"M: max health {self.max_health} -> {self.max_health + 10}",
    f"S: strength X{self.damage_multi} -> X{round(number=(self.damage_multi + 0.1), ndigits=3)}"])()

        if stat == 0:
            self.regen += 5
        elif stat == 1:
            self.max_health += 10
        elif stat == 2:
            self.damage_multi += 0.1
            if self.weapon != None:
                self.damage = round(number=((5 + self.weapon[2]) * self.damage_multi), ndigits=3)
            else:
                self.damage = round(number=(5 * self.damage_multi), ndigits=3)

        
        self.xp -= self.xp_need
        self.xp_need += 5
        self.level += 1

    def whirl_strike(self):
        enemy = 0
        while enemy < len(self.enemys):
            if not self.attack(hit=enemy, damage=max(int(self.damage/3), 1)):
                enemy += 1

    def e_armour(self, armor):
        self.armor = armor
        self.armor_rating = armor[2]

    def e_weapon(self, weapon):
        self.weapon = weapon

        self.damage += self.weapon[2] 
        self.damage = self.damage * self.damage_multi
        self.anti_armor = self.weapon[3]


class Room:
    # all attributes the room will need
    def __init__(self,
                 hostiles=[], 
                 uniq=None,
                 items=[])-> None:
        
        # all adjacent rooms that the player can move to
        self.posable_direction = []

        # room info
        self.hostiles: list[Creature] = hostiles
        self.uniq = uniq
        self.items = items

        # map info
        self.has_player = False