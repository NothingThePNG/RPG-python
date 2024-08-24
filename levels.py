from classes import *

enim = {"rat": ["rat", 15, 5, 0, 3, 4, 1], "spider": ["spider", 5, 10, 0, 3, 2, 0], 
        "wisdom rat": ["wisdom rat", 2, 1, 4, 0, 40, 2]}

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

    
    # the first room is always the top left
    return new_map

# the staring map
map1 = make_map(new_map=[
    [Room(), None, Room(hostiles=[Creature(attributes=enim["wisdom rat"], items=[["rusty armor", "A", 1]])]),],
    [Room(hostiles=[Creature(attributes=enim["rat"])]), Room(),Room()],
    [Room(), Room(), Room(),],
    [Room(uniq="next", hostiles=[Creature(attributes=enim["spider"]), Creature(attributes=enim["spider"])]), None, Room(items=[["small hammer", "W", 1, 2]]),],
])

map2 = make_map(new_map=[
    [Room(), None,],
    [Room(), Room(uniq="exit"),],
])

next = [map1, map2]