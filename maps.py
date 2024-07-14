from classes import Room

# the staring map
map1 = [
    [Room(), Room(), None,],
    [None, Room(hostiles=2), Room(),],
    [Room(hostiles=1), Room(), None,],
    [Room(uniq="next"), None, Room(),],
]

map2 = [
    [Room(), None,],
    [Room(), Room(uniq="exit"),],
]

next = {"map1": ["map2", map2]}