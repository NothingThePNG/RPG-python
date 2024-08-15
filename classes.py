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
    def __init__(self, attributes) -> None:
        self.name: str = attributes[0]
        self.health: int = attributes[1]
        self.max_health: int = attributes[1]
        self.damage: int = attributes[2]
        self.armor: int = attributes[3]
        self.regen: int = attributes[4]
        self.enemys: list[Creature] = []

        self.xp = attributes[5]
        self.level = 1
    
    def hurt(self, damage: int, attacker):
        self.health -= max((damage - self.armor), 0)

        print(f"{attacker} attacked {self} for {damage} damage")
        print(f"{self} has {self.health}HP\n")

        if attacker not in self.enemys:
            self.enemys.append(attacker)

    # attacking 
    def attack(self, hit) -> None:
        # if there is no enemys in it's list
        if len(self.enemys) <= 0:
            return 0
        
        # if there was a specific creature to be attacked it will run on them else it will chose a random
        if hit == None:
            enemy: Creature = choice(seq=self.enemys)
        else:
            enemy: Creature = self.enemys[hit]

        # hurting the enemy and printing the result 
        enemy.hurt(self.damage, self)

        # if the enemy dies it is removed 
        if enemy.health <= 0:
            print(f"{enemy} has died to {self}")
            self.xp += enemy.xp
            self.enemys.remove(enemy)
            return enemy.xp
        return 0

    def __str__(self) -> str:
        return self.name

class Player(Creature):
    # giving the player the unique stats
    def __init__(self, attributes: list, ) -> None:
        self.name: str = attributes[0]

        self.health: int = int(attributes[1])
        self.max_health: int = int(attributes[2])
        self.damage: int = int(attributes[3])
        self.armor: int = int(attributes[4])
        self.regen: int = int(attributes[5])

        self.enemys: list[Creature] = []

        self.xp = int(attributes[6])
        self.level = int(attributes[7])
        self.xp_need = 20
        for i in range(self.level-1):
            self.xp_need += 5

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
    A: armor {self.armor} -> {self.armor + 2}
> """, acceptable=["R", "M", "S", "A"])

        if stat == "R":
            self.regen += 5
        elif stat == "M":
            self.max_health += 10
        elif stat == "S":
            self.damage += 5
        else:
            self.armor += 2
        
        self.xp -= self.xp_need
        self.xp_need += 5
        self.level += 1

    def whirl_strike(self):
        for enemy in self.enemys:
            enemy.hurt(damage=int(self.damage/3), attacker=self)

            if enemy.health <= 0:
                print(f"{enemy} has died to {self}")
                self.xp += enemy.xp
                self.enemys.remove(enemy)
                return enemy.xp


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
        self.posable_direction = []

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