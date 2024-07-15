from classes import *

hostiles = {"rat": ["rat", 10, 3, 0], "spider": ["spider", 5, 10, 0]}

# the staring map
map1 = [
    [Room(), Room(), None,],
    [None, Room(hostiles=[Creature(hostiles["rat"])]), Room(),],
    [Room(hostiles=[Creature(hostiles["spider"]), Creature(hostiles["spider"])]), Room(), None,],
    [Room(uniq="next"), None, Room(),],
]

map2 = [
    [Room(), None,],
    [Room(), Room(uniq="exit"),],
]

next = {"map1": ["map2", map2]}