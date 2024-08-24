from random import *
from get_type import *
#import ollama


def clamp(number, minn, maxn):
    return max(min(maxn, number), minn)


class Colors:
    reset="\033[0m"

    orange="\033[33m"
    purple="\033[35m"
    blue="\033[34m"
    red="\033[31m"
    green="\033[32m"

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
        damage = max((damage / max(self.armor_rating - anti_armor, 1)), 1)
        self.health -= damage

        print(f"{attacker} attacked {self} for {damage} damage")
        print(f"{self} has {self.health}HP\n")

        if attacker not in self.enemys:
            self.enemys.append(attacker)

        if self.health <= 0:
            attacker.xp += self.xp
            print(f"{attacker} ({attacker.health}HP) got {self.xp}xp")
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
        self.xp_need: int = 20
        for i in range(self.level-1):
            self.xp_need += 5

        self.health: int = int(attributes[3])
        self.max_health: int = int(attributes[4])
        self.regen: int = int(attributes[5])
        self.damage: int = int(attributes[6])

        self.enemys: list[Creature] = []

        self.items: list = [["rusty sword", "W", 5, 0]]

        self.armor = attributes[7]
        self.weapon = attributes[8]
        self.anti_armor = 0
        self.armor_rating = 0

        if self.weapon != None:
            self.damage += self.weapon[2]
            self.anti_armor = self.weapon[3]

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
        stat = get_val_str(output=f"""Do you want to upgrade:
    R: regen {self.regen} -> {self.regen + 5}
    M: max health {self.max_health} -> {self.max_health + 10}
    S: strength {self.damage} -> {self.damage + 5}
> """, acceptable=["R", "M", "S"])

        if stat == "R":
            self.regen += 5
        elif stat == "M":
            self.max_health += 10
        elif stat == "S":
            self.damage += 5
        
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
        self.anti_armor = self.weapon[3]


class Room:
    # all attributes the room will need
    def __init__(self, description="A barron room made of stone", 
                 hostiles=[], 
                 uniq=None,
                 items=[])-> None:
        # all adjacent rooms that the player can move to
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.posable_direction = ["I"]

        # room info
        self.description = description
        self.hostiles: list[Creature] = hostiles
        self.uniq = uniq
        self.items = items

        # map info
        self.discoverd = False
        self.has_player = False
    
    def initialise(self):
        self.has_player = True

        if not self.discoverd:
            # ollama.chat(self.description)

            self.discoverd = True

            print(Colors.purple, end="")

            prompt: str = f"Wight a DnD stile description (and only a description of the room) for a {self.description}"

            if self.uniq == "dark":
                prompt = "room to dark to see anything"
            else:
                if len(self.hostiles) > 0:
                    prompt += f"a there are hostiles consisting of {self.hostiles}"
                
                prompt += f"with doors leading off ({", ".join(self.posable_direction)})"

            
            # stream = ollama.chat(
            #     model="llama2",
            #     messages=[{
            #         "role": "user",
            #         "content": prompt
            #     }],
            #     stream=True
            # )
            # for chunk in stream:
            #     sys.stdout.write(chunk["message"]["content"])
            #     sys.stdout.flush()
        
            return self, True
        return self, False
    
    # making the player move
    def move(self, direction):
        if direction == "D":
            return self.right
        elif direction == "A":
            return self.left
        elif direction == "W":
            return self.up
        elif direction == "S":
            return self.down
        else:
            return "error"