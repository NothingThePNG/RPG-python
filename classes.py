from random import *
from g_print import g_print_str
import sys
import os
import ollama

class Creature:
    def __init__(self, attributes) -> None:
        self.name = attributes[0]
        self.health = attributes[1]
        self.armor = 0
        self.regen = 10
        self.damage = attributes[2]
        self.enemys: list[Creature] = []
    
    def hurt(self, damage: int, attacker):
        self.health -= damage

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
        g_print_str(words=f"{self} attacked {enemy} for {self.damage} damage")
        g_print_str(words=f"{enemy} has {enemy.health}HP\n")

        # if the enemy dies it is removed 
        if enemy.health <= 0:
            g_print_str(words=f"{enemy} has died to {self}")
            self.enemys.remove(enemy)

    def __str__(self) -> str:
        return self.name

class Player(Creature):
    # giving the player the unique stats
    def __init__(self) -> None:
        super().__init__(["player", 100, 8])

    def heal(self) -> None:
        self.health += self.regen

        g_print_str(f"{self} healed for {self.regen}")
        g_print_str(f"{self} has {self.health}HP")

class Room:
    # all attributes the room will need
    def __init__(self, description="A barron room", hostiles=0, uniq=None) -> None:
        self.right = None
        self.left = None
        self.up = None
        self.down = None

        self.posable = []

        self.description = description
        self.hostiles = hostiles
        self.uniq = uniq
    
    def initialise(self):
        # ollama.chat(self.description)
        os.system(command="cls")

        stream = ollama.chat(
            model="llama2",
            messages=[{
                "role": "user",
                "content": f"Wight a DnD stile discription for a {self.description}"
            }],
            stream=True
        )
        for chunk in stream:
            sys.stdout.write(chunk["message"]["content"])
            sys.stdout.flush()

        print()

        return self
    
    # making the player move
    def move(self, direction):
        if direction == "r":
            return self.right
        elif direction == "l":
            return self.left
        elif direction == "u":
            return self.up
        elif direction == "d":
            return self.down
        else:
            return "error"