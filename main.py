from random import *
from inventory import *
from classes import *
from levels import *
from combat import *
from maps import *
import pickle, keyboard, sys

keyboard.press_and_release('f11')

clear_screen()

def stop_program() -> None:
    """
    The function `stop_program` is designed to stop the program by simulating the keyboard shortcut
    "Ctrl + c" when the hotkey "F12" is pressed.
    """
    keyboard.press_and_release("Ctrl + c")

keyboard.add_hotkey("F12", stop_program)


def tutorial() -> None:
    """
    The `tutorial` function provides information on various topics such as controls, movement, combat,
    colors, save/load, inventory, and leveling up in a text-based game.
    """
    print(Colors.purple)
    learn = 1
    while learn != 0:
        learn = Select_item("What topic do you want to know about", 
                            ["Exit", "Controls", "Movement", "Combat", "Colors", "Save/Load", "Inventory", "Leveling up"])()
        clear_screen()
        print(Colors.purple)
        if learn == 1:
            print("\n\n-------------------Controls------------------")
            print(" F12 - quit")
            print(" W,A,S,D - move")
            print(" I - inventory")
            print(" E [number] - equip item at selected index")
            print(" D [number] - drop item at selected index")
            print(" [any] - the name of a enemy to attack the first enemy with that name or the number of the enemy")
            input()
        elif learn == 2:
            print("-------------------Movement------------------")
            print("You will be given a map of the currently explored areas when this stage starts")
            print("The map will have:")
            print("     -     ^ wall")
            print("     -     @ for the current room")
            print("     -     N for the room that takes you to the next map")
            print("     -     ⌂ healing space (H to heal but they are a one time use)")
            print("     -     H hostiles they will attack you")
            print("There is only one N room per map and if you are in one there will be no @ on the map only the N")
            print("When you go up a floor you will not be able to go back down so make sure you're done exploring")
            print("\nThere is also lines ie (- |) witch show the directions you can move")
            print("To move you will have a prompt such as")
            print("         Where do you want to go? (I, W, D)")
            print("The game uses W A S and D so this means you can go up or right in the example")
            print("(The I will be covered in inventory)")
            input()
        elif learn == 3:
            print("\n\n-------------------Combat------------------")
            print("In combat you will see some thing like:")
            print(f"""{Colors.red}
        You are attacked by:
        1    -   rat 10HP
        2    -   spider 5HP
        {Colors.purple}
        """)
            print("You can then heal buy imputing H")
            print("Or attack by typing: ")
            print("     -     the name of the enemy (it will attack the first enemy with that name)")
            print("     -     type the number of the enemy to attack a specific one (as enemys die the numbers will change)")
            print("The input prompt will loo like:")
            print(f"""{Colors.orange}
        What action do you want to take?
        H: Heal
        [any]: attack
        {Colors.purple}""")
            print("There is also a armor stat")
            print("It's very simple the damage will be divided ageist the armor")
            print("eg a 10HP attack ageist something with 2 armor will be 5 damage dealt")
            print("Anti armor removes armor points")
            print(" so if you have 1 anti armor an attack something with 2 armour it will hit like there is no armour")
            print("I you are in a fight you can't win you can't run away so be careful")
            input()
        elif learn == 4:
            print("\n\n-------------------Colors------------------")
            print("Colors have meaning:")
            print("     -     Purple: description/info")
            print("     -     Red: enemy action")
            print("     -     Blue: player action")
            print("     -     Orange: input")
            input()
        elif learn == 5:
            print("\n\n-------------------Save/Load------------------")
            print("You save by going to the next level")
            print("This is automatically done each level")
            print("The game will only save at the start of levels")
            print("You load a save by reopening the game where you will be promoted to load a save")
            print("You can chose not to and make a new game or chose to where you will need to input the index of the wanted save")
            print("YOUR CHARACTER WILL ONLY BE SAVED AFTER YOU BEAT THE FIRST LEVEL")
            input()
        elif learn == 6:
            print("\n\n-------------------Inventory-------------------")
            print("While you are waling you will notice the option (I)")
            print("This is to access your inventory")
            print("In your inventory you will be shown")
            print("\nThen you can enter L to leave and start moving agin")
            print("or you can equip or drop a item")
            print("\nIn order to drop or equip you will need to type e or d then the index of the item to drop")
            print("(If you drop a item you will not get it back)")
            print("You can only have up to 9 items in your inventory the armor and weapon you are using dose not count")
            input()
        elif learn == 7:
            print("\n\n-------------------Leveling up-------------------")
            print("When you get enough xp you can choose one of 3 attributes to up grade")
            print("You can upgrade your regen so in combat you will heal 5 hp more then before")
            print("Up grade your max health so that you can have 10 more max health")
            print("Or strength which is a number your damage is multiplied by")
            print("Damage is calculated by adding your base damage of 5 adding the damage of your weapon and multiplying it by your strength")
            input()



def stats(player: Player) -> None:
    """
    The function `stats` takes a `Player` object as input and returns a formatted string displaying
    various statistics about the player.
    
    :param player: The `stats` function takes a `Player` object as a parameter and returns a formatted
    string containing various statistics about the player. The `Player` object likely has attributes
    such as `damage`, `health`, `max_health`, `armor_rating`, `anti_armor`, `level`, `xp`,
    :type player: Player
    :return: The `stats` function is returning a formatted string containing various statistics of the
    player object passed as an argument. The string includes information such as damage, health, armor,
    level, experience points, and more.
    """
    ret = ""
    ret += (Colors.blue)
    ret += (f"Damage: {round(player.damage, 3)}, Health: {player.health}/{player.max_health}\n")
    ret += (f"Armor: {player.armor_rating}, Anti-armor: {player.anti_armor}\n")
    ret += (f"Level: {player.level}\n")
    ret += (f"{player} has {player.xp}/{player.xp_need}xp\n")
    return ret



def save(player:Player, savepoint=0) -> None:
    """
    This Python function saves player data to a file at a specified savepoint.
    
    :param player: The `save` function you provided is used to save the player's data to a file named
    "_internal/save.dat". The function takes two parameters:
    :type player: Player
    :param savepoint: The `savepoint` parameter in the `save` function is used to specify the index at
    which the player's data should be saved in the list of saved data. If the `savepoint` provided is
    greater than the current number of saved data entries, a new entry will be added to the, defaults to
    0 (optional)
    """
    # name, xp, level, health, max health, regen, damage multi, items, armor, weapon

    with open("_internal/save.dat", "rb") as read:
        data = pickle.load(read)
    
    if savepoint + 1 > len(data):
        data.append([player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage_multi, player.items, player.armor, player.weapon])
    else:
        data[savepoint] = [player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage_multi, player.items, player.armor, player.weapon]

    with open("_internal/save.dat", "wb") as save:
        pickle.dump(data, save)


def start_play(player_attributes=[None, 0, 1, 50, 50, 10, 1.0, [["rusty nail", "W", 0, 1]]]):
    """
    The function `start_play` initializes a game by creating a player with specified attributes,
    generating a game map, setting the player's initial position in the map, and returning relevant game
    data.
    
    :param player_attributes: The `player_attributes` parameter in the `start_play` function is a list
    that contains various attributes of the player character. Here is a breakdown of the default values
    in the `player_attributes` list:
    :return: The function `start_play` is returning four values: `currant_map`, `currant_room`,
    `player`, and `player_cords`.
    """
    clear_screen()

    if player_attributes[0] == None:
        player_attributes[0] = input(f"{Colors.orange}What is your character's name?\n> {Colors.blue}")

    player: Player = Player(attributes=player_attributes)

    currant_map: list[list] = make_level(player=player)

    currant_room: Room = currant_map[hight//2][width//2]

    player_cords = {
        "x": width//2,
        "y": hight//2,
    }

    currant_room.has_player = True

    return currant_map, currant_room, player, player_cords

def get_actions(currant_room):
    """
    The function `get_actions` returns a list of possible actions based on the current room's unique
    attributes and possible directions.
    
    :param currant_room: The `get_actions` function takes a `currant_room` object as a parameter. The
    function checks the unique attribute of the current room and appends specific actions to the list of
    possible actions based on the room's uniqueness
    :return: The function `get_actions` returns a list of possible actions that can be taken in the
    current room. The list includes the actions "I" (for interact), "H" (for heal, if the current room
    is a healing room), "N" (for next, if the current room is a room leading to the next area), and any
    possible directions that the player can move in from
    """
    posable_action = ["I"]

    if currant_room.uniq == "heal":
        posable_action.append("H") # letting the plyer be abel to heal
    
    if currant_room.uniq == "next":
        posable_action.append("N")  
    
    posable_action.extend(currant_room.posable_direction)

    return posable_action

def movement_input(currant_map, currant_room, player) -> int:
    """
    The function `movement_input` takes the current room, map, and player information, displays
    available actions, stats, and map, prompts the player for input on their desired action, and returns
    the chosen action.
    
    :param currant_room: The `currant_room` parameter likely represents the current room or location
    where the player is situated in the game. It is used to determine the possible actions or movements
    that the player can take within that room
    :param currant_map: The `movement_input` function seems to be designed to handle player movement
    within a game. It takes in the current room, current map, and player information as parameters. The
    function first retrieves possible actions for the current room, then generates output based on
    player stats and the current map. It clears the
    :param player: The `player` parameter in the `movement_input` function seems to represent the player
    object or data structure that contains information about the player's status, such as their current
    position, inventory, health, etc. It is likely used within the function to provide context for the
    player's actions and to update
    :return: The function `movement_input` returns the action that the player wants to take in the
    current room, based on the list of possible actions available in that room.
    """
    posable_action = get_actions(currant_room=currant_room)

    output = stats(player=player)
    output += draw_map(current_map=currant_map) # drawing the map

    clear_screen()

    print(output, flush=True)
    
    # using the list of posable path ways to get a input as to which the player will move
    action: str = get_val_str(
        output=f"{Colors.orange}What do you want to do? ({', '.join(posable_action)}) {Colors.blue}",
        acceptable=posable_action
    ) # getting the action the player wants to do

    return action


# a function that hands player movement
def play(player_attributes=[None, 0, 1, 50, 50, 10, 1.0, [["rusty nail", "W", 0, 1]], None, None], savepoint=0):

    currant_map, currant_room, player, player_cords = start_play(player_attributes=player_attributes)

    clear_screen()

    while currant_room.uniq != "exit": # intl the player reaches the exit

        while player.xp >= player.xp_need:
            player.level_up() # leveling up the player
            clear_screen()

        action = movement_input(currant_map, currant_room, player)

        # generating a new map
        if action == "N":
            save(player=player, savepoint=savepoint)

            currant_map: list[list] = make_level(player=player)

            currant_room: Room = currant_map[hight//2][width//2]

            currant_room.has_player = True

            player_cords = {
                "x": width//2,
                "y": hight//2,
            }

        # accessing the inventory 
        elif action == "I":
            clear_screen()
            inventory(player)
            clear_screen()
            continue
        
        # healing the player and stoping the player from healing repeatedly
        elif action == "H":
            player.heal()
            currant_room.uniq = ""
            continue
        
            
        # moving to the next room
        else:
            currant_room.has_player = False

            # updating coordinates and the room
            if action == "W":
                player_cords["y"] -= 1
                currant_room = currant_map[player_cords["y"]][player_cords["x"]]
            elif action == "D":
                player_cords["x"] += 1
                currant_room = currant_map[player_cords["y"]][player_cords["x"]]
            elif action == "A":
                player_cords["x"] -= 1
                currant_room = currant_map[player_cords["y"]][player_cords["x"]]
            elif action == "S":
                player_cords["y"] += 1
                currant_room = currant_map[player_cords["y"]][player_cords["x"]]

            currant_room.has_player = True
        
        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
            run_combat(hostiles=currant_room.hostiles, currant_room=currant_room, player=player)
            clear_screen()

        if len(currant_room.items) > 0:
            for i in range(len(currant_room.items)):
                if len(player.items) < 10:
                    item = currant_room.items.pop(i)
                    player.items.append(item)
                    sys.stdout.write(f"You picked up {item[0]}")
            
    
    clear_screen()


    print(Colors.green + "You escaped the Dungeon")
    input()

def ask_tutorial():
    tutorial_choice = Select_item(output="Do you want a tutorial?", items=["n", "y"])()

    if tutorial_choice:
        tutorial()

def start():
    """
    The `start()` function loads saved character data from a file, displays a menu of saved characters
    for selection, and then proceeds to play the game with the selected character or start a new game if
    chosen.
    """
    try:
        with open("_internal/save.dat", "rb") as loading:
            loaded = pickle.load(loading)

    except EOFError and FileNotFoundError:
        with open("_internal/save.dat", "wb") as loading:
            pickle.dump([], loading)
            loaded = []
    except:
        with open("_internal/save.dat", "wb") as loading:
            pickle.dump([], loading)
            loaded = []


    possibles = []
    # name, xp, level, health, max health, regen, damage multi, items, armor, weapon
    for character in loaded:
            
        possibles.append(f"""Name: {character[0]}
Level: {character[2]}
Heath: {character[3]}/{character[4]}
""")
        
    possibles.append("New save")

    index = Select_item(
        output=f"""

{Colors.purple} {Colors.bold}
        .--------------------------------------------------------------.
        |||   / |  / /                                                 |
        |||  /  | / /  ___     //  ___      ___      _   __      ___   |
        ||| / /||/ / //___) ) // //   ) ) //   ) ) // ) )  ) ) //___) )|
        |||/ / |  / //       // //       //   / / // / /  / / //       |
        ||  /  | / ((____   // ((____   ((___/ / // / /  / / ((____    |
        '--------------------------------------------------------------'
{Colors.reset}{Colors.orange}

Which save file do you want?
""",
        items=possibles
    )()

    ask_tutorial()

    if index == len(possibles)-1:
        play(savepoint=len(loaded))
    attributes = loaded[index]

    play(player_attributes=attributes, savepoint=index)





def main():
    """
    The main function checks if the script is being run directly and then calls the start function.
    """
    if __name__ == "__main__":
        start()

main()