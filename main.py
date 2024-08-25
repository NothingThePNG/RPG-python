from random import *
from time import sleep
from classes import *
from levels import *
from combat import *
from maps import *
import pickle


os.system("cls")

    

def tutorial():
    print(Colors.purple)
    print("-------------------Movement------------------")
    print("You will be given a map of the currently explored areas when this stage starts")
    print("The map will have:")
    print("     -     # for explored rooms")
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
    print("It's very simple the number of armor points is number of damage adsorbed")
    print("eg a 5HP attack ageist something with 3 armor will do 2HP")
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
    print("\n\n-------------------inventory-------------------")
    print("While you are waling you will notice the option (I)")
    print("This is to access your inventory")
    print("In your inventory you will be shown")
    print("\nThen you can enter L to leave and start moving agin")
    print("or you can equip or drop a item")
    print("\nIn order to drop or equip you will need to type e or d then the index of the item to drop")
    print("(If you drop a item you will not get it back)")
    print("\n")




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

    print(player.items)

    if player.armor != None:
        print(f"Equipped armor: {player.armor[0]}")
    else:
        print("No armor")

    if player.weapon != None:
        print(f"Equipped weapon: {player.weapon[0]}")
    else:
        print("No weapon")


    for i in range(len(player.items)):
        item = player.items[i]

        if item == None:
            print("None")

        elif item[1] == "A":
            print(f"{i+1} - {item[0]} will give +{item[2]} armor")

        elif item[1] == "W":
            print(f"{i+1} - {item[0]} with a extra {item[2]} damage and {item[3]}")
    
    if len(player.items) <= 0:
        print("You don't have any items")



def inventory(player: Player) -> None:
    os.system("cls")

    display_item(player=player)

    print()

    action = input(f"{Colors.orange}Do you want to \n  -  L: leave\n  -  E [num]: equip\n  - D [num]: drop \n> ").strip().upper().split()
    
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

        action = input("Do you want to \n  -  L: leave\n  -  E: equip\n  - D: drop \n> ").strip().upper().split()

    os.system("cls")




def save(player, index):
    # xp, level, health, max_health, regen, damage, armour, map_index

    with open("_internal/save.dat", "rb") as read:
        data = pickle.load(read)

    data.append([player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage, player.items, player.armor, player.weapon, index+1])

    with open("_internal/save.dat", "wb", newline ='') as save:
        pickle.dump(data, save)


# a function that hands player movement
def play(player_attributes=[None, 0, 1, 50, 50, 10, 5, [["rusty nail", "W", 2, 0]], None, None], map_id=0):
    if player_attributes[0] == None:
        player_attributes[0] = input(f"{Colors.orange}What is your character's name? \n> ")

    player: Player = Player(player_attributes)

    currant_map_index: int = map_id # starting at map1
    currant_map: list = next[currant_map_index]

    currant_room: Room = currant_map[0][0]
    currant_room.initialise()

    prev = None
    new = True

    while currant_room.uniq != "exit": # intl the player reaches the exit


        draw_map(current_map=currant_map) # drawing the map
        print(f"{player} has {player.xp}/{player.xp_need}xp")

        while player.xp >= player.xp_need:
            player.level_up()

        posable_direction = currant_room.posable_direction
        
        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
            output=f"{Colors.orange}Where do you want to go? ({', '.join(currant_room.posable_direction)}) ",
            acceptable=posable_direction
        )

        os.system("cls")

        # going to the next map
        if dire == "N":


            currant_map_index += 1
            try:
                prev = currant_room
                currant_map: list = next[currant_map_index]
                print(Colors.green, "You go up the stars.") # giving feed back to player
                currant_room, new = currant_map[0][0].initialise() # the starting room is always in the top right corner

                save(player=player, index=currant_map_index)
            # the final map
            except IndexError:
                print(Colors.green + "You escaped")

        elif dire == "I":
            inventory(player)
            continue
        
            
        # moving to the next room
        else:
            prev = currant_room
            currant_room.has_player = False
            next_room: Room = currant_room.move(dire) # moving rooms 
            currant_room, new = next_room.initialise() # initializing the next room
        
        if new:
            player.heal(regen=2)

        # if there are hostiles combat will start
        if len(currant_room.hostiles) > 0:
            run = run_combat(hostiles=currant_room.hostiles, currant_room=currant_room, player=player)
            if run:
                currant_room.has_player = False
                currant_room, new = prev.initialise()

        if len(currant_room.items) > 0:
            for i in currant_room.items:
                player.items.append(i)
                print(f"You picked up {i[0]}")
    
    os.system("cls")

    print(Colors.green + "You escaped the Dungeon")

def ask_tutorial():
    tutorial_choice = get_accept(output="Do you want a tutorial? (y/n) \n> ")

    if tutorial_choice:
        tutorial()

    play()

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

        if get_accept(output="Do you want to load from a save? (y/n) \n> "):
            index = get_int("Which save do you want?\n> ", vaid_range=[0, len(loaded)])

            attributes = loaded[index]

            map_load = attributes.pop()

            play(player_attributes=attributes, map_id=int(map_load)-1)


        else:
            ask_tutorial()

    else:
        ask_tutorial()



def main():
    if __name__ == "__main__":
        start()


main()