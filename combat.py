from time import sleep
from classes import Colors

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
            action = input(f"{Colors.orange}What action do you want to take?\nH: Heal\n[any]: attack\n").strip().lower()
            # running the action the player wants
            if action[0] == "h":
                print(Colors.blue, end="")
                player.heal()
                player_turn_fin = True
            else:
                # getting a valid target 
                while type(action) == str:
                    if action == "back":
                        break
                    
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
                    if type(action) == str:
                        action = input("Who do you want to attack?: ").lower().strip()
                else:
                    # displaying the players hit 
                    print(Colors.blue, end="")
                    player.attack(hit=action)
                    player_turn_fin = True
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            print(Colors.red, "You are attacked by:")

            for i in range(len(hostiles)):
                hostiles[i].enemys.append(player)
                print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
        sleep(1)

    currant_room.hostiles = hostiles