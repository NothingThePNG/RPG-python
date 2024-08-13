from random import *
from time import sleep
from classes import *
from rich.console import Console
from maps import *
from combat import *
from get_type import get_val_str

os.system("cls")

# a function for getting each line of the map
def get_lines(currant_map: list, line_index: int) -> str:
    top = [] # the paths up
    line = "" # the rooms
    out = "" # output
    if line_index > 0:
        for r in currant_map[line_index-1]:
            if r == None:
                top.append(" ")
                
            elif r.discoverd:
                if r.down != None:
                    top.append("|")
                else:
                    top.append(" ")
            else:
                top.append(" ")

    for r in range(len(currant_map[line_index])):
        if currant_map[line_index][r] == None:
            line += "   "
            top.append(" ")
                
        elif currant_map[line_index][r].discoverd:
            if currant_map[line_index][r].left != None:
                line += "-"
            else:
                line += " "
            
            # if the room is the room that lets the plyer go to the next map
            if "N" in currant_map[line_index][r].posable_direction:
                line += "N"

            # the room the player currently is
            elif currant_map[line_index][r].has_player:
                line += "@"
            # a room
            else:
                line += "#"

            # there is a room right
            if currant_map[line_index][r].right != None:
                line += "-"
            # no room right
            else:
                line += " "
            
            # there is a room above
            if currant_map[line_index][r].up != None:
                top[r] = "|"
                
            else:
                top.append(" ")

        else:
            line += "   "
            top.append(" ")

    if top.count("|") > 0:
        out += " " + "  ".join(top) + "\n"

    if line.count(" ") < len(currant_map[line_index])*3-1:
        out += line

    # not preventing unnecessary lines being printed
    if out != "":
        print(out)

# a function that prints each line of the map
def draw_map(current_map):
    os.system("cls")
    print(Colors.purple, end="")

    for y in range(len(current_map)):
        get_lines(currant_map=current_map, line_index=y)

def tutorial():
    print("-------------------Movement------------------")
    print("You will be given a map of the currently explored areas when this stage starts")
    print("You can move or analyze")

# a function that hands player movement
def play():
    name = input(f"{Colors.orange}What is your characters name: ")
    player = Player(name=name)

    currant_map_index: int = 0 # starting at map1
    currant_map: list = next[currant_map_index]

    currant_room: Room = currant_map[0][0] 
    currant_room.initialise()

    while currant_room.uniq != "exit": # intl the player reaches the exit
        draw_map(current_map=currant_map) # drawing the map
        
        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
            output=f"Where do you want to go? ({', '.join(currant_room.posable_direction)}): ",
            acceptable=currant_room.posable_direction
        )

        # going to the next map
        if dire == "N":
            currant_map_index += 1
            try:
                currant_map: list = next[currant_map_index]
            # the final map
            except IndexError:
                print(Colors.green + "You escaped")     
            currant_room: Room = currant_map[0][0] # the starting room is always in the top right corner
            print(Colors.green, "You go up the stars.") # giving feed back to player
            currant_room.initialise() # getting the AI to make a description
        # moving to the next room
        else:
            currant_room.has_player = False
            next_room: Creature = currant_room.move(dire) # moving rooms 
            currant_room = next_room.initialise() # initializing the next room

        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
            run_combat(hostiles=currant_room.hostiles, currant_room=currant_room, player=player)
        

def main():
    if __name__ == "__main__":
        play()

main()