from time import sleep
from classes import *
from get_type import *
#import os

def _start_combat(hostiles, player):
    # telling the player what is fighting them
    print(Colors.red, "You are attacked by:")

    for i in range(len(hostiles)):
        hostiles[i].enemys.append(player)
        print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
    
    sleep(1)

    print(Colors.blue, f"You have {player.health}HP\n")

    sleep(0.2)

    player.enemys = hostiles # getting the player class to know what can be attacked 

    return hostiles

def run_combat(hostiles: list[Creature], currant_room: Room, player: Player):
    hostiles = _start_combat(hostiles=hostiles, player=player)

    while len(hostiles) > 0 and player.health > 0:
        print(Colors.red, end=" ")

        attackers = []
        # getting the hostiles to attack the player
        for i in hostiles:
            i.attack(None)
            sleep(.5)

            attackers.append(f"{i.name}\n       {i.health}HP")
        
        attackers.append("Whirl strike")
        
        attackers.append("Run")
        
        input()
        Clear_screen()
        player_turn_fin = False
        while not player_turn_fin:

            action = Select_item(f"{Colors.orange}Who do you want to attack", attackers)()

            # running the action the player wants
            if action == len(attackers)-1:
                for i in player.enemys:
                    i.enemys.remove(player)
                return True
            elif action == len(attackers)-2:
                print(Colors.blue)
                player.whirl_strike()
                player_turn_fin = True

            else:
                # displaying the players hit 
                print(Colors.blue, end="")
                player.attack(hit=action)
                player_turn_fin = True
        
        input()
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            print(Colors.red, "You are attacked by:")

            for i in range(len(hostiles)):
                print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
        else:
            print("\nNo more hostiles.\n")
        sleep(1)

    currant_room.hostiles = hostiles
    
    sleep(1)
    
    return False