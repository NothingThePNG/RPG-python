from time import sleep
from classes import *
from get_type import *
from playsound import playsound

def _start_combat(hostiles, player):
    clear_screen()
    # telling the player what is fighting them
    print(Colors.red, Colors.bold, "You are attacked by:")

    for i in range(len(hostiles)):
        hostiles[i].enemys.append(player)
        print(f"    -   {hostiles[i]} {hostiles[i].health}HP")
    
    sleep(0.5)

    print(Colors.reset, Colors.blue, f"You have {player.health}HP\n")

    sleep(0.2)

    player.enemys = hostiles # getting the player class to know what can be attacked 

    return hostiles

def run_combat(hostiles: list[Creature], currant_room: Room, player: Player):
    hostiles = _start_combat(hostiles=hostiles, player=player)

    while len(hostiles) > 0 and player.health > 0:
        print(Colors.red, Colors.bold, end="")

        attackers = []
        # getting the hostiles to attack the player
        for i in hostiles:
            i.attack(None)
            playsound("_internal/rpg_hit.wav")

            sleep(.5)

            attackers.append(f"{i.name}\n       {i.health}HP")
        
        attackers.append("Whirl strike")
        
        attackers.append("Run")

        print(Colors.reset, end="")

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


        sleep(0.1)
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            print(Colors.red, "You are attacked by:")

            for i in range(len(hostiles)):
                print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
        else:
            print("\nNo more hostiles.\n")
        sleep(1)

    currant_room.hostiles = hostiles
    
    sleep(0.2)
    
    return False