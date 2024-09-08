from random import *
from get_type import *


def clamp(number, minn, maxn):
    return max(min(maxn, number), minn)


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
        damage = max((damage / max(self.armor_rating - anti_armor, 1)), 0.5)
        self.health -= damage

        print(f"{attacker} attacked {self} for {round(damage, 3)} damage")
        print(f"{self} has {round(self.health, 3)}HP\n")

        if attacker not in self.enemys:
            self.enemys.append(attacker)

        if self.health <= 0:
            attacker.xp += self.xp
            print(f"{attacker} ({round((attacker.health), 3)}HP) got {self.xp}xp")
            print(f"{attacker} now has {attacker.xp}xp")

            if len(self.items) > 0:
                for item in self.items:
                    attacker.items.append(item)
                    print(f"{attacker} got {item[0]}")
            return True
        return False

    # attacking 
    def attack(self, hit, damage=None) -> None:
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
        self.health = clamp(number=self.health, minn=0, maxn=self.max_health)

        print(f"{self} healed for {regen}")
        print(f"{self} has {self.health}HP")
    
    def level_up(self):
        stat = get_val_str(output=f"""{Colors.orange}Do you want to upgrade:
    R: regen {self.regen} -> {self.regen + 5}
    M: max health {self.max_health} -> {self.max_health + 10}
    S: strength X{self.damage_multi} -> X{round((self.damage_multi + 0.1), 3)}
>{Colors.blue} """, acceptable=["R", "M", "S"])

        if stat == "R":
            self.regen += 5
        elif stat == "M":
            self.max_health += 10
        elif stat == "S":
            self.damage_multi += 0.1
            self.damage = round(number=((5 + self.weapon[2]) * self.damage_multi), ndigits=3)

        
        self.xp -= self.xp_need
        self.xp_need += 5
        self.level += 1

    def whirl_strike(self):
        for enemy in range(len(self.enemys)):
            self.attack(hit=enemy, damage=max(int(self.damage/3), 1))

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