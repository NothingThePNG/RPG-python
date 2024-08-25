import os
from classes import Colors

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

    if line.count(" ") < len(currant_map[line_index])*3:
        out += line

    # not preventing unnecessary lines being printed
    if out != "":
        print(out)

# a function that prints each line of the map
def draw_map(current_map):
    print(Colors.purple, end="")

    for y in range(len(current_map)):
        get_lines(currant_map=current_map, line_index=y)
    print()