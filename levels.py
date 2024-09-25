from classes import *

hight = 20
width = 40

def _start_level():
    """
    The function `_start_level` initializes a builder dictionary and a 2D list representing a level
    layout.
    :return: The function `_start_level` is returning a tuple containing two elements: a dictionary
    named `builder` and a 2D list named `level`.
    """
    builder = {
    "room count": 600,
    "padding": 1,
    "x": int(width // 2),
    "y": int(hight // 2),
    }

    level = [[None] * width for i in range(hight)]

    return builder, level

enem_level_1 = [["rat", 6, 2, 0, 3, 4, 1], ["baby spider", 1, 6, 0, 3, 15, 0], 
        ["wisdom rat", 2, 0.5, 4, 0, 40, 2],]

enem_inpos = [["Lord Death of Murder Mountain", 1000, 1000, 1000, 1000, 1000, 1000]]

#stor = [ ]

items_level_1 = [["Hollow Log", "A", 2]]

def _make_enemys(player: Player):
    """
    This Python function creates a list of enemy creatures based on the player's level.
    
    :param player: The function `_make_enemys` takes a `Player` object as a parameter. The function
    checks the player's level and assigns a list of enemies based on the player's level. It then creates
    a random number of enemy creatures (between 1 and 3) from the selected list and
    :type player: Player
    :return: A list of enemy creatures is being returned. The number of creatures in the list is
    randomly determined between 1 and 3, and the type of enemy creatures added to the list depends on
    the player's level. If the player's level is less than or equal to 5, level 1 enemies are added to
    the list. Otherwise, a different set of enemies is added to the list.
    """
    if player.level <= 5:
        enem = enem_level_1
    else:
        enem = enem_inpos
    
    ret = []

    for i in range(randint(1, 3)):
        enemy = Creature(choice(enem))
        ret.append(enemy)

    return ret

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
                    new_map[y][x].posable_direction.append("A")
            if x < len(new_map[y])-1:
                if new_map[y][x+1] != None:
                    new_map[y][x].posable_direction.append("D")
            if y < len(new_map)-1:
                if new_map[y+1][x] != None:
                    new_map[y][x].posable_direction.append("S")
            if y > 0:
                if new_map[y-1][x] != None:
                    new_map[y][x].posable_direction.append("W")

    
    # the first room is always the top left
    return new_map

def make_level(player: Player):
    the_builder, new_level = _start_level() 

    while the_builder["room count"] > 0:
        x = the_builder["x"]
        y = the_builder["y"]

        if new_level[y][x] == None:
            new_room = Room()
            change_room = randint(0, 30)
            if change_room == 0:
                new_room.uniq = "heal"
            elif change_room > 28 and (the_builder["x"] != int(width // 2) and the_builder["y"] != int(hight//2)):
                new_room.hostiles = _make_enemys(player=player)
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
    
    
    new_level[the_builder["y"]][the_builder["x"]] = Room(uniq="next")
        
    return _make_map(new_map=new_level)