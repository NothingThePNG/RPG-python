from random import *
from time import sleep
from classes import *
from levels import *
from combat import *
from maps import *
import pickle, keyboard, os

#keyboard.press('f11')

os.system("cls")

def stop_program():
    keyboard.press_and_release("ctrl + c")

keyboard.add_hotkey("F3", stop_program)
    

def tutorial():
    print(Colors.purple)
    print("\n\n-------------------Controls------------------")
    print(" F3 - quit")
    print(" W,A,S,D - move")
    print(" I - inventory")
    print(" E [number] - equip item at selected index")
    print(" D [number] - drop item at selected index")
    print(" [any] - the name of a enemy to attack the first enemy with that name or the number of the enemy")
    print("-------------------Movement------------------")
    print("You will be given a map of the currently explored areas when this stage starts")
    print("The map will have:")
    print("     -     # wall")
    print("     -     @ for the current room")
    print("     -     N for the room that takes you to the next map")
    print("There is only one N room per map and if you are in one there will be no @ on the map only the N")
    print("When you go up a floor you will not be able to go back down so make sure you're done exploring")
    print("\nThere is also lines ie (- |) witch show the directions you can move")
    print("To move you will have a prompt such as")
    print("         Where do you want to go? (I, W, D)")
    print("The game uses W A S and D so this means you can go up or right in the example")
    print("(The I will be covered in inventory)")
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
    print("There are 2 factors weapons effect damage and armor penetration")

    print("\n\n-------------------Colors------------------")
    print("Colors have meaning:")
    print("     -     Purple: description/info")
    print("     -     Red: enemy action")
    print("     -     Blue: player action")
    print("     -     Orange: input")
    print("\n\n-------------------Save/Load------------------")
    print("You save by going to the next level")
    print("This is automatically done each level")
    print("The game will only save at the start of levels")
    print("You load a save by reopening the game where you will be promoted to load a save")
    print("You can chose not to and make a new game or chose to where you will need to input the index of the wanted save")
    print("YOUR CHARACTER WILL ONLY BE SAVED AFTER YOU BEAT THE FIRST LEVEL")
    print("\n\n-------------------Inventory-------------------")
    print("While you are waling you will notice the option (I)")
    print("This is to access your inventory")
    print("In your inventory you will be shown")
    print("\nThen you can enter L to leave and start moving agin")
    print("or you can equip or drop a item")
    print("\nIn order to drop or equip you will need to type e or d then the index of the item to drop")
    print("(If you drop a item you will not get it back)")
    print("You can only have up to 9 items in your inventory the armor and weapon you are using dose not count")
    print("\n\n-------------------Leveling up-------------------")
    print("When you get enough xp you can choose one of 3 attributes to up grade")
    print("You can upgrade your regen so in combat you will heal 5 hp more then before")
    print("Up grade your max health so that you can have 10 more max health")
    print("Or strength which is a number your damage is multiplied by")
    print("Damage is calculated by adding your base damage of 5 adding the damage of your weapon and multiplying it by your strength")
    print("\n")

    input()





def equip(player: Player, num: int):
    if num-1 < len(player.items) and num-1 >= 0:
        item = player.items.pop((num-1))

        if item[1] == "A":
            if player.armor != None:
                player.items.append(player.armor)
            player.e_armour(armor=item)

            print(f"Equipped {player.armor[0]}\n\n")

        if item[1] == "W":
            if player.weapon != None:
                player.items.append(player.weapon)
            player.e_weapon(weapon=item)

            print(f"Equipped {player.weapon[0]}\n\n")
    
    else:
        print("Invalid number")


def drop(player: Player, num: int) -> None:
    if num-1 < len(player.items) and num-1 >= 0:

        print(f"Dropped {player.items[num-1]}")
        del player.items[num-1]
    
    else:
        print("Invalid number")


def display_item(player: Player):
    print(Colors.blue, end="")

    if player.armor != None:
        print(f"Equipped armor: {player.armor[0]} +{player.armor[2]} armor")
    else:
        print("No armor")

    if player.weapon != None:
        print(f"Equipped weapon: {player.weapon[0]} +{round((player.weapon[2] * player.damage_multi), 3)} damage ")
    else:
        print("No weapon")


    for i in range(len(player.items)):
        item = player.items[i]

        if item == None:
            print("None")

        elif item[1] == "A":
            print(f"{i+1} - {item[0]} will give {item[2]} armor")

        elif item[1] == "W":
            print(f"{i+1} - {item[0]} with a {item[2]} damage and {item[3]} armor penetrating")
    
    if len(player.items) <= 0:
        print("\nYou don't have any items")



def inventory(player: Player) -> None:
    os.system("cls")

    display_item(player=player)

    print()

    action = input(f"{Colors.orange}Do you want to \n  -  L: leave\n  -  E [num]: equip\n  - D [num]: drop \n> {Colors.blue}").strip().upper().split()
    
    while action != ["L"]:
        os.system("cls")

        if len(action) == 2:
            if action[0] == "E" and action[1].isdigit():
                equip(player=player, num=int(action[1]))

            elif action[0] == "D" and action[1].isdigit():
                drop(player=player, num=int(action[1]))

            else:
                print("invalid input\n")

        display_item(player=player)

        action = input(f"{Colors.orange}Do you want to \n  -  L: leave\n  -  E [num]: equip\n  - D [num]: drop \n> {Colors.blue}").strip().upper().split()


    os.system("cls")


def stats(player: Player):
    print(f"Damage: {round(player.damage, 3)}, Health: {player.health}")
    print(f"Armor: {player.armor_rating}, Anti-armor: {player.anti_armor}")
    print(f"Level: {player.level}")
    print(f"{player} has {player.xp}/{player.xp_need}xp")



def save(player, savepoint=0):
    # xp, level, health, max_health, regen, damage, armour

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
    os.system("cls")
    if player_attributes[0] == None:
        player_attributes[0] = input(f"{Colors.orange}What is your character's name?\n> {Colors.blue}")

    player: Player = Player(attributes=player_attributes)

    currant_map: list[list] = make_level()

    currant_room: Room = currant_map[hight//2][width//2]

    prev = currant_room

    currant_room.has_player = True

    os.system("cls")

    while currant_room.uniq != "exit": # intl the player reaches the exit


        stats(player=player)
        draw_map(current_map=currant_map) # drawing the map

        while player.xp >= player.xp_need:
            player.level_up() # leveling up the player

        posable_direction = currant_room.posable_direction
        
        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
            output=f"{Colors.orange}What do you want to do? ({', '.join(currant_room.posable_direction)}) {Colors.blue}",
            acceptable=posable_direction
        ) # getting the action the player wants to do

        os.system("cls")

        # going to the next map
        if dire == "N":
            save(player=player, savepoint=savepoint)

            currant_map: list[list] = make_level()

            currant_room: Room = currant_map[hight//2][width//2]

            prev = currant_room

            currant_room.has_player = True

        elif dire == "I":
            inventory(player)
            continue
        
        elif dire == "H":
            player.heal()
            currant_room.uniq = ""
            continue
        
            
        # moving to the next room
        else:
            prev = currant_room
            currant_room.has_player = False
            currant_room = currant_room.move(dire) # moving rooms 
            currant_room.has_player = True
        

        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
            run = run_combat(hostiles=currant_room.hostiles, currant_room=currant_room, player=player)
            if run:
                currant_room.has_player = False
                prev.has_player = True
                currant_room = prev

        if len(currant_room.items) > 0:
            for i in range(len(currant_room.items)):
                if len(player.items) < 10:
                    item = currant_room.items.pop(i)
                    player.items.append(item)
                    print(f"You picked up {item[0]}")
    
    os.system("cls")

    print(Colors.green + "You escaped the Dungeon")
    input()

def ask_tutorial(lode_index=0):
    tutorial_choice = get_accept(output="Do you want a tutorial? (y/n)")

    if tutorial_choice:
        tutorial()

    play(savepoint=lode_index)

def start():
    try:
        with open("_internal/save.dat", "rb") as loading:
            loaded = pickle.load(loading)

    except EOFError:
        with open("_internal/save.dat", "wb") as loading:
            pickle.dump([], loading)
            loaded = []


    print("""


.--------------------------------------------------------------.
|||   / |  / /                                                 |
|||  /  | / /  ___     //  ___      ___      _   __      ___   |
||| / /||/ / //___) ) // //   ) ) //   ) ) // ) )  ) ) //___) )|
|||/ / |  / //       // //       //   / / // / /  / / //       |
||  /  | / ((____   // ((____   ((___/ / // / /  / / ((____    |
'--------------------------------------------------------------'

      
""")

    if len(loaded) > 0:
        print(loaded)

        if get_accept(output="Do you want to load from a save? (y/n):"):
            index = get_int("Which save do you want?\n> ", vaid_range=[0, len(loaded)])

            attributes = loaded[index]

            play(player_attributes=attributes, savepoint=index)


        else:
            ask_tutorial(lode_index=len(loaded))

    else:
        ask_tutorial()




def main():
    if __name__ == "__main__":
        start()

main()