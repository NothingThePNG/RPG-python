from classes import *
import sys

# a function for getting each line of the map
def get_lines(currant_map: list, line_index: int) -> str:
    line = ""
    for r in range(len(currant_map[line_index])):
        if currant_map[line_index][r] == None:
            sys.stdout.write(f"{Colors.reset}   ")

                
        else:
            room: Room = currant_map[line_index][r]
            # the room the player currently is
            if room.has_player:
                sys.stdout.write(f"{Colors.blue}{Colors.revers} @ ")

            # if the room is the room that lets the plyer go to the next map
            elif room.uniq == "next":
                sys.stdout.write(f"{Colors.reset}{Colors.back_cyan} N ")
            
            elif room.uniq == "heal":
                sys.stdout.write(f"{Colors.green}{Colors.revers} ⌂ ")
            
            elif len(room.hostiles) > 0:
                sys.stdout.write(f"{Colors.red}{Colors.revers} H ")

            # a room
            else:
                sys.stdout.write(f"{Colors.reset}{Colors.revers}   ")
    
    sys.stdout.write("\n")

# a function that prints each line of the map
def draw_map(current_map):
    print(Colors.reset)

    for y in range(len(current_map)):
        get_lines(currant_map=current_map, line_index=y)
    
    sys.stdout.flush()

    print(Colors.purple)