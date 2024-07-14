from g_print import *
from get_type import *
from random import *
from time import sleep
from classes import *
from rich.console import Console
from maps import *

creature_types = [["rat", 10, 3], ["spider", 5, 10]] # hostiles that can be selected from

player = Player()

# a function for making a hostile 
def make_enemys(count):
    ret = []
    for i in range(count):
        ret.append(Creature(choice(creature_types)))

    return ret

def start_combat(hostile_count):
    hostiles = make_enemys(count=hostile_count)

    # telling the player what is fighting them
    g_print_str("You are attacked by:")

    for i in range(len(hostiles)):
        hostiles[i].enemys.append(player)
        g_print_str(words=f"{i+1}    -   {hostiles[i]}")
    
    sleep(1)

    g_print_str(f"You have {player.health}HP\n")

    sleep(0.2)

    player.enemys = hostiles # getting the player class to know what can be attacked 

    return hostiles

def combat(hostile_count, currant_room):
    hostiles = start_combat(hostile_count=hostile_count)

    while len(hostiles) > 0 and player.health > 0:

        # getting the hostiles to attack the player
        for i in hostiles:
            i.attack(None)
            sleep(1)

        action = get_val_str(output="\nDo you want to \nH: Heal \nA: Attack\n", acceptable=["h", "a"])

        # running the action the player wants
        if action == "h":
            player.heal()
        elif action == "a":
            attacking = get_int(output="Who do you want to attack?: ", vaid_range=[0, len(hostiles)+1])-1

            player.attack(hit=attacking)
        
        if len(hostiles) > 0:
            # contiguously displaying the enemies so the player dose not have to remember 
            g_print_str(words="You are attacked by:")

            for i in range(len(hostiles)):
                hostiles[i].enemys.append(player)
                g_print_str(f"{i+1}    -   {hostiles[i]}")
        sleep(1)
    currant_room.hostiles = len(hostiles)

# telling the Room classes the adjacent rooms
def make_map(new_map):
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
                    new_map[y][x].posable.append("l")
            if x < len(new_map[y])-1:
                if new_map[y][x+1] != None:
                    new_map[y][x].right = new_map[y][x+1]
                    new_map[y][x].posable.append("r")
            if y < len(new_map)-1:
                if new_map[y+1][x] != None:
                    new_map[y][x].down = new_map[y+1][x]
                    new_map[y][x].posable.append("d")
            if y > 0:
                if new_map[y-1][x] != None:
                    new_map[y][x].up = new_map[y-1][x]
                    new_map[y][x].posable.append("u")
    
    # the first room is always the top left
    return new_map[0][0]


# a function that hands player movement
def play():
    currant_map = "map1"
    currant_room: Creature = make_map(new_map=map1) # starting at map1
    currant_room.initialise()
    while currant_room.uniq != "exit": # intl the player reaches the exit

        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
          output=f"Where do you want to go? ({', '.join(currant_room.posable)}): ",
          acceptable=currant_room.posable
        )

        next_room: Creature = currant_room.move(dire) # moving rooms 
        currant_room = next_room.initialise() # initializing the next room

        # if there are hostiles combat will start
        if currant_room.hostiles > 0:
           combat(hostile_count=currant_room.hostiles, currant_room=currant_room)
        
        if currant_room.uniq == "next":
            currant_room = make_map(new_map=next[currant_map][1])
            currant_map = next[currant_map][0]
    print("You escaped")


def main():
    if __name__ == "__main__":
        play()

main()