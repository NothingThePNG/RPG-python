from classes import *

# a function for getting each line of the map
def get_lines(currant_map: list, line_index: int) -> str:
    """
    This function takes a current map and a line index as input, and returns a string representing the
    rooms on that line with different colors and symbols based on their properties.
    
    :param currant_map: The `currant_map` parameter is a list representing the current map in the game.
    Each element in the list corresponds to a row in the map, and each element within a row represents a
    room in the map
    :type currant_map: list
    :param line_index: The `line_index` parameter in the `get_lines` function represents the index of
    the line within the `currant_map` list that you want to retrieve. It is used to specify which line
    of the map you are interested in processing within the function
    :type line_index: int
    :return: The function `get_lines` returns a string representing a line of the current map based on
    the provided `currant_map` and `line_index`. The string contains visual representations of different
    types of rooms, such as rooms with players, rooms leading to the next map, healing rooms, rooms with
    hostiles, and empty rooms.
    """
    line = ""
    for r in range(len(currant_map[line_index])):
        if currant_map[line_index][r] == None:
            line += (f"{Colors.reset}   ")

                
        else:
            room: Room = currant_map[line_index][r]
            # the room the player currently is
            if room.has_player:
                line += (f"{Colors.blue}{Colors.revers} @ ")

            # if the room is the room that lets the plyer go to the next map
            elif room.uniq == "next":
                line += (f"{Colors.reset}{Colors.back_cyan} N ")
            
            elif room.uniq == "heal":
                line += (f"{Colors.green}{Colors.revers} ⌂ ")
            
            elif len(room.hostiles) > 0:
                line += (f"{Colors.red}{Colors.revers} H ")

            # a room
            else:
                line += (f"{Colors.reset}{Colors.revers}   ")
    
    line += ("\n")
    return line

def draw_map(current_map) -> str:
    """
    The function `draw_map` iterates through the rows of a given map and constructs a string
    representation of the map.
    
    :param current_map: It looks like you were about to provide some information about the `current_map`
    parameter, but it seems to have been cut off. Could you please provide more details or let me know
    if you need help with anything specific related to the `current_map` parameter?
    :return: The function `draw_map` is returning a string representation of the map based on the input
    `current_map`.
    """

    the_map = ""

    for y in range(len(current_map)):
        the_map += get_lines(currant_map=current_map, line_index=y)
    
    return the_map