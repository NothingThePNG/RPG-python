from classes import *

hight = 25
width = 20

def _start_level():
    builder ={
    "room count": 600,
    "padding": 1,
    "x": int(width // 2),
    "y": int(hight // 2),
    "exit": 2,
    }

    level = [[None] * width for i in range(hight)]

    return builder, level

enim_level_1 = [["rat", 6, 5, 0, 3, 4, 1], ["spider", 5, 10, 0, 3, 2, 0], 
        ["wisdom rat", 2, 1, 4, 0, 40, 2]]

# telling the Room classes the adjacent rooms
def _make_map(new_map) -> Room:
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
                    new_map[y][x].posable_direction.append("A")
            if x < len(new_map[y])-1:
                if new_map[y][x+1] != None:
                    new_map[y][x].right = new_map[y][x+1]
                    new_map[y][x].posable_direction.append("D")
            if y < len(new_map)-1:
                if new_map[y+1][x] != None:
                    new_map[y][x].down = new_map[y+1][x]
                    new_map[y][x].posable_direction.append("S")
            if y > 0:
                if new_map[y-1][x] != None:
                    new_map[y][x].up = new_map[y-1][x]
                    new_map[y][x].posable_direction.append("W")

            if new_map[y][x].uniq == "next":
                new_map[y][x].posable_direction.append("N")

            elif new_map[y][x].uniq == "heal":
                new_map[y][x].posable_direction.append("H")

    
    # the first room is always the top left
    return new_map

def make_level():
    the_builder, new_level = _start_level() 

    while the_builder["room count"] > 0:
        x = the_builder["x"]
        y = the_builder["y"]

        if new_level[y][x] == None:
            new_room = Room()
            new_level[y][x] = new_room
        the_builder["room count"] -= 1


        
        direction = randint(1, 4)

        if direction == 1:
            if y < (hight - 1 - the_builder["padding"]):
                the_builder["y"] += 1
            else:
                the_builder["y"] -= 1
        elif direction == 2:
            if x < (width - 1 - the_builder["padding"]):
                the_builder["x"] += 1
            else:
                the_builder["x"] -= 1
        elif direction == 3:
            if x > the_builder["padding"]:
                the_builder["x"] -= 1
            else:
                the_builder["x"] += 1
        elif y > the_builder["padding"]:
            the_builder["y"] -= 1
        else:
            the_builder["y"] += 1
    
    if the_builder["exit"] > 0:
        new_level[the_builder["y"]][the_builder["x"]] = Room(uniq="next")
        
    return _make_map(new_map=new_level)