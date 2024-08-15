from time import sleep
from classes import Colors
from get_type import *

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

def run_combat(hostiles, currant_room, player):
    hostiles = _start_combat(hostiles=hostiles, player=player)

    while len(hostiles) > 0 and player.health > 0:
        print(Colors.red, end=" ")
        # getting the hostiles to attack the player
        for i in hostiles:
            i.attack(None)
            sleep(.5)
        player_turn_fin = False
        while not player_turn_fin:
            action = input(f"{Colors.orange}What action do you want to take?\nH: Heal\nW: Whirl strike\n[any]: attack\n").strip().lower()
            # running the action the player wants
            if len(action) <= 0:
                print("Invalid: need a input")
                pass
            elif action[0] == "h":
                print(Colors.blue, end="")
                player.heal()
                player_turn_fin = True
            elif action[0] == "w":
                print(Colors.blue)
                player.whirl_strike()
                player_turn_fin = True
            elif action == "run":
                for i in player.enemys:
                    i.enemys.remove(player)
                return True
            else:
                # getting a valid target 
                
                if action.isnumeric():
                    if int(action)-1 in range(0, len(player.enemys)):
                        action = int(action)-1
                    else:
                        print("Not in range.")
                else:
                    # attacking the first creature with the name the player inputted
                    for i in range(len(player.enemys)):
                        if player.enemys[i].name == action:
                            action = i
                if type(action) == int:
                    # displaying the players hit 
                    print(Colors.blue, end="")
                    xp = player.attack(hit=action)
                    player_turn_fin = True

                    if xp > 0:
                        print(f"{player} got {xp}xp")
                        print(f"{player} now has {player.xp}xp")
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            print(Colors.red, "You are attacked by:")

            for i in range(len(hostiles)):
                print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
        else:
            print("\nNo more hostiles.\n")
        sleep(1)

    currant_room.hostiles = hostiles
    while not get_accept():
        print("ok")
    
    return False