from classes import Colors
import sys

# a function for getting each line of the map
def get_lines(currant_map: list, line_index: int) -> str:
    for r in range(len(currant_map[line_index])):
        if currant_map[line_index][r] == None:
            sys.stdout.write("   ")
            sys.stdout.flush()

                
        else:
            # the room the player currently is
            if currant_map[line_index][r].has_player:
                sys.stdout.write(f"{Colors.blue} @ {Colors.reset}")
                sys.stdout.flush()

            # if the room is the room that lets the plyer go to the next map
            elif "N" in currant_map[line_index][r].posable_direction:
                sys.stdout.write(" N ")
                sys.stdout.flush()
            
            elif currant_map[line_index][r].uniq == "heal":
                sys.stdout.write(" ⌂ ")
                sys.stdout.flush()

            # a room
            else:
                sys.stdout.write(" · ")
                sys.stdout.flush()
    
    sys.stdout.write("\n")
    sys.stdout.flush()

# a function that prints each line of the map
def draw_map(current_map):
    print(Colors.reset)

    for y in range(len(current_map)):
        get_lines(currant_map=current_map, line_index=y)

    print(Colors.purple)