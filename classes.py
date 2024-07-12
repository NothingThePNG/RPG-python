from random import *
from g_print import g_print_str

class Creature:
    def __init__(self, attributes) -> None:
        self.name = attributes[0]
        self.health = attributes[1]
        self.armor = 0
        self.regen = 10
        self.melee = 5
        self.enemys: list[Creature] = []
    
    def hurt(self, damage: int, attacker):
        self.health -= damage

        if attacker not in self.enemys:
            self.enemys.append(attacker)

    def attack(self, hit) -> None:
        if len(self.enemys) <= 0:
            return None
        
        if hit == None:
            enemy: Creature = choice(self.enemys)
        else:
            enemy: Creature = self.enemys[hit]

        enemy.hurt(self.melee, self)
        g_print_str(f"{self} attacked {enemy} for {self.melee} damage")
        g_print_str(f"{enemy} has {enemy.health}HP\n")

        if enemy.health <= 0:
            g_print_str(f"{enemy} has died to {self}")
            self.enemys.remove(enemy)

    def __str__(self) -> str:
        return self.name

class Player(Creature):
    def __init__(self) -> None:
        super().__init__(["player", 100])

    def heal(self) -> None:
        self.health += self.regen
        g_print_str(f"{self} healed for {self.regen}")
        g_print_str(f"{self} has {self.health}HP")