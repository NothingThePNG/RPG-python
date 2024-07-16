from random import *
import sys
import os
#import ollama

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
        self.damage: int = attributes[2]
        self.armor: int = attributes[3]
        self.regen: int = 15
        self.enemys: list[Creature] = []
        self.items = []
    
    def hurt(self, damage: int, attacker):
        self.health -= (damage - self.armor)

        if attacker not in self.enemys:
            self.enemys.append(attacker)

    # attacking 
    def attack(self, hit) -> None:
        # if there is no enemys in it's list
        if len(self.enemys) <= 0:
            return None
        
        # if there was a specific creature to be attacked it will run on them else it will chose a random
        if hit == None:
            enemy: Creature = choice(seq=self.enemys)
        else:
            enemy: Creature = self.enemys[hit]

        # hurting the enemy and printing the result 
        enemy.hurt(self.damage, self)
        print(f"{self} attacked {enemy} for {self.damage} damage")
        print(f"{enemy} has {enemy.health}HP\n")

        # if the enemy dies it is removed 
        if enemy.health <= 0:
            print(f"{enemy} has died to {self}")
            self.enemys.remove(enemy)

    def __str__(self) -> str:
        return self.name

class Player(Creature):
    # giving the player the unique stats
    def __init__(self) -> None:
        super().__init__(["player", 100, 8, 0])

    def heal(self) -> None:
        self.health += self.regen

        print(f"{self} healed for {self.regen}")
        print(f"{self} has {self.health}HP")

class Room:
    # all attributes the room will need
    def __init__(self, description="A barron room made of stone", 
                 hostiles=[], 
                 uniq=None) -> None:
        self.right = None
        self.left = None
        self.up = None
        self.down = None

        self.posable_direction = []

        self.description = description
        self.hostiles: list[Creature] = hostiles
        self.uniq = uniq
        self.items = []
    
    def initialise(self):
        # ollama.chat(self.description)
        os.system(command="cls")

        print(Colors.purple, end=" ")

        prompt: str = f"Wight a DnD stile description (and only a description of the room) for a {self.description}"

        if self.uniq == "dark":
            prompt = "room to dark to see anything"
        if len(self.hostiles) > 0:
            prompt += f"a there are hostiles consisting of {self.hostiles}"

        
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

        print()

        return self
    
    # making the player move
    def move(self, direction):
        if direction == "R":
            return self.right
        elif direction == "L":
            return self.left
        elif direction == "U":
            return self.up
        elif direction == "D":
            return self.down
        else:
            return "error"
        
    def analyze(self, direction):
        if direction == "R":
            self.right.initialise()
        elif direction == "N":
            self.left.initialise()
        elif direction == "U":
            self.up.initialise()
        elif direction == "D":
            self.down.initialise()
        else:
            print("error")