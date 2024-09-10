from random import *
from inventory import *
from classes import *
from levels import *
from combat import *
from maps import *
import pickle, keyboard

keyboard.press_and_release('f11')

clear_screen()

def stop_program():
    keyboard.press_and_release("ctrl + c")

keyboard.add_hotkey("F12", stop_program)


def tutorial():
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



def stats(player: Player):
    print(Colors.blue, end="")
    print(f"Damage: {round(player.damage, 3)}, Health: {player.health}/{player.max_health}")
    print(f"Armor: {player.armor_rating}, Anti-armor: {player.anti_armor}")
    print(f"Level: {player.level}")
    print(f"{player} has {player.xp}/{player.xp_need}xp")



def save(player, savepoint=0):
    # name, xp, level, health, max health, regen, damage multi, items, armor, weapon

    with open("_internal/save.dat", "rb") as read:
        data = pickle.load(read)
    
    if savepoint + 1 > len(data):
        data.append([player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage_multi, player.items, player.armor, player.weapon])
    else:
        data[savepoint] = [player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage_multi, player.items, player.armor, player.weapon]

    with open("_internal/save.dat", "wb") as save:
        pickle.dump(data, save)


# a function that hands player movement
def play(player_attributes=[None, 0, 1, 50, 50, 10, 1.0, [["rusty nail", "W", 0, 1]], None, None], savepoint=0):
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

    clear_screen()

    while currant_room.uniq != "exit": # intl the player reaches the exit

        while player.xp >= player.xp_need:
            player.level_up() # leveling up the player
            clear_screen()

        
        posable_action = ["I"]

        if currant_room.uniq == "heal":
            posable_action.append("H") # letting the plyer be abel to heal
        
        if currant_room.uniq == "next":
            posable_action.append("N")  
        
        posable_action.extend(currant_room.posable_direction)

        stats(player=player)
        draw_map(current_map=currant_map) # drawing the map
        
        # using the list of posable path ways to get a input as to which the player will move
        action: str = get_val_str(
            output=f"{Colors.orange}What do you want to do? ({', '.join(posable_action)}) {Colors.blue}",
            acceptable=posable_action
        ) # getting the action the player wants to do

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
        
        clear_screen()

        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
            run_combat(hostiles=currant_room.hostiles, currant_room=currant_room, player=player)
            clear_screen()

        if len(currant_room.items) > 0:
            for i in range(len(currant_room.items)):
                if len(player.items) < 10:
                    item = currant_room.items.pop(i)
                    player.items.append(item)
                    print(f"You picked up {item[0]}")
            
    
    clear_screen()


    print(Colors.green + "You escaped the Dungeon")
    input()

def ask_tutorial():
    tutorial_choice = Select_item(output="Do you want a tutorial?", items=["n", "y"])()

    if tutorial_choice:
        tutorial()

def start():
    try:
        with open("_internal/save.dat", "rb") as loading:
            loaded = pickle.load(loading)

    except EOFError and FileNotFoundError:
        with open("_internal/save.dat", "wb") as loading:
            pickle.dump([], loading)
            loaded = []



    possibles = ["New save"]
    # name, xp, level, health, max health, regen, damage multi, items, armor, weapon
    for character in loaded:
            
        possibles.append(f"""Name: {character[0]}
Level: {character[2]}
Heath: {character[3]}/{character[4]}""")
    

    index = Select_item(
        output=f"""

{Colors.purple}
.--------------------------------------------------------------.
|||   / |  / /                                                 |
|||  /  | / /  ___     //  ___      ___      _   __      ___   |
||| / /||/ / //___) ) // //   ) ) //   ) ) // ) )  ) ) //___) )|
|||/ / |  / //       // //       //   / / // / /  / / //       |
||  /  | / ((____   // ((____   ((___/ / // / /  / / ((____    |
'--------------------------------------------------------------'
{Colors.orange}

Which save file do you want?
""",
        items=possibles
    )()
        
            

    # index = get_int("Which save do you want?\n> ", vaid_range=[0, len(loaded)])

    ask_tutorial()

    if index == 0:
        play(savepoint=len(loaded))
    attributes = loaded[index-1]

    play(player_attributes=attributes, savepoint=index)





def main():
    if __name__ == "__main__":
        start()

main()