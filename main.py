from get_type import *
from random import *
from time import sleep
from classes import *
from rich.console import Console
from maps import *

player = Player()

# telling the Room classes the adjacent rooms
def make_map(new_map) -> Room:
    # going though each element of the 2d list
    for y in range(len(new_map)):
        for x in range(len(new_map[y])):
            # skipping empty cells
            if new_map[y][x] == None:
                continue

            # making sure that there are cells above below and next to, so that the program wont break
            if x > 0:
                if new_map[y][x-1] != None:
                    new_map[y][x].left = new_map[y][x-1]
                    new_map[y][x].posable_direction.append("L")
            if x < len(new_map[y])-1:
                if new_map[y][x+1] != None:
                    new_map[y][x].right = new_map[y][x+1]
                    new_map[y][x].posable_direction.append("R")
            if y < len(new_map)-1:
                if new_map[y+1][x] != None:
                    new_map[y][x].down = new_map[y+1][x]
                    new_map[y][x].posable_direction.append("D")
            if y > 0:
                if new_map[y-1][x] != None:
                    new_map[y][x].up = new_map[y-1][x]
                    new_map[y][x].posable_direction.append("U")

            if new_map[y][x].uniq == "next":
                new_map[y][x].posable_direction.append("N")
    
    # the first room is always the top left
    return new_map[0][0]

def start_combat(hostiles):
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

def combat(hostiles, currant_room):
    hostiles = start_combat(hostiles=hostiles)

    while len(hostiles) > 0 and player.health > 0:
        print(Colors.red, end=" ")
        # getting the hostiles to attack the player
        for i in hostiles:
            i.attack(None)
            sleep(.5)
        
        action = get_val_str(output=f"{Colors.orange}\nDo you want to \nH: Heal \nA: Attack\n", acceptable=["H", "HEAL", "A", "ATTACK"])
        print()
        # running the action the player wants
        if action == "H":
            print(Colors.blue, end=" ")
            player.heal()
        elif action == "A":
            attacking = "yes"
            # getting a valid target 
            while type(attacking) == str:
                attacking = input("Who do you want to attack?: ").lower()
                
                if attacking.isnumeric():
                    if int(attacking)-1 in range(0, len(player.enemys)):
                        attacking = int(attacking)-1
                    else:
                        print("Not in range.")
                else:
                    # attacking the first creature with the name the player inputted
                    for i in range(len(player.enemys)):
                        if player.enemys[i].name == attacking:
                            attacking = i

            # displaying the players hit 
            print(Colors.blue, end=" ")
            player.attack(hit=attacking)
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            print(Colors.red, "You are attacked by:")

            for i in range(len(hostiles)):
                hostiles[i].enemys.append(player)
                print(f"{i+1}    -   {hostiles[i]} {hostiles[i].health}HP")
        sleep(1)

    currant_room.hostiles = hostiles

def tutorial():
    print("You will be prompted to move")

# a function that hands player movement
def play():
    currant_map: str = "map1"
    currant_room: Creature = make_map(new_map=map1) # starting at map1
    currant_room.initialise()

    while currant_room.uniq != "exit": # intl the player reaches the exit

        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
          output=f"{Colors.orange}Where do you want to go? ({', '.join(currant_room.posable_direction)}): ",
          acceptable=currant_room.posable_direction
        )
        if dire == "N":
            currant_room = make_map(new_map=next[currant_map][1])
            currant_map = next[currant_map][0]
            print(Colors.green, "You go up the stars.")
        else:
            next_room: Creature = currant_room.move(dire) # moving rooms 
            currant_room = next_room.initialise() # initializing the next room

        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
           combat(hostiles=currant_room.hostiles, currant_room=currant_room)
        
    print(Colors.green, "You escaped")


def main():
    if __name__ == "__main__":
        play()

main()