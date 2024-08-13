from classes import *

hostiles = {"rat": ["rat", 10, 3, 0, 3], "spider": ["spider", 5, 10, 0, 3]}

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
    return new_map

# the staring map
map1 = make_map(new_map=[
    [Room(), Room(), None,],
    [None, Room(hostiles=[Creature(attributes=hostiles["rat"])]), Room(),],
    [Room(hostiles=[Creature(attributes=hostiles["spider"]), Creature(attributes=hostiles["spider"])]), Room(), Room(),],
    [Room(uniq="next"), None, Room(),],
])

map2 = make_map(new_map=[
    [Room(), None,],
    [Room(), Room(uniq="exit"),],
])

next = [map1, map2]