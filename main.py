from random import *
from time import sleep
from classes import *
from rich.console import Console
from levels import *
from combat import *
from maps import *
import pandas
import keyboard
import csv

os.system("cls")

def tutorial():
    print(Colors.purple)
    print("-------------------Movement------------------")
    print("You will be given a map of the currently explored areas when this stage starts")
    print("The map will have:")
    print("     -     # for explored rooms")
    print("     -     @ for the current room")
    print("     -     B for the room that takes you to the prev map")
    print("     -     N for the room that takes you to the next map")
    print("There is only one N and B room per map and if you are in one there will be no @ on the map only the N and B")
    print("When you go up a floor you will not be able to go back down so make sure you're done exploring")
    print("\nThere is also lines ie (- |) witch show the directions you can move")
    print("To move you will have a prompt such as")
    print("         Where do you want to go? (W, D)")
    print("The game uses W A S and D so this means you can go up or right in the example")
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
    print("\n")
    print("\n\n-------------------Save/Load------------------")
    print("")


def save(player, index):
    # xp, level, health, max_health, regen, damage, armour, map_index

    data = [[player.name, player.xp, player.level, player.health, player.max_health, player.regen, player.damage, player.armor, index]]

    with open("save.csv", "a+", newline ='') as save:
        write = csv.writer(save)
        write.writerows(data)


# a function that hands player movement
def play(player_attributes=[None, 50, 50, 5, 0, 5, 0, 1], map_id=0):
    if player_attributes[0] == None:
        player_attributes[0] = input("What is your character's name? \n> ")

    player: Player = Player(player_attributes)

    currant_map_index: int = map_id # starting at map1
    currant_map: list = next[currant_map_index]

    currant_room: Room = currant_map[0][0]
    currant_room.initialise()

    keyboard.add_hotkey(hotkey="F2", callback=save, args=(player, currant_map_index))

    prev = None

    while currant_room.uniq != "exit": # intl the player reaches the exit


        draw_map(current_map=currant_map) # drawing the map
        print(f"{player} has {player.xp}/{player.xp_need}xp")

        while player.xp >= player.xp_need:
            player.level_up()
        
        # using the list of posable path ways to get a input as to which the player will move
        dire: str = get_val_str(
            output=f"{Colors.orange}Where do you want to go? ({', '.join(currant_room.posable_direction)}) ",
            acceptable=currant_room.posable_direction
        )

        # going to the next map
        if dire == "N":


            currant_map_index += 1
            try:
                prev = currant_room
                currant_map: list = next[currant_map_index]
                print(Colors.green, "You go up the stars.") # giving feed back to player
                currant_room, new = currant_map[0][0].initialise() # the starting room is always in the top right corner
            # the final map
            except IndexError:
                print(Colors.green + "You escaped")

        
                
            
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
    
    os.system("cls")

    print(Colors.green + "You escaped the Dungeon")

def ask_tutorial():
    tutorial_choice = get_accept(output="Do you want a tutorial? (y/n) \n> ")

    if tutorial_choice:
        tutorial()

    play()

def start():
    df = pandas.read_csv('save.csv')
    num_lines = df.shape[0]

    if num_lines > 0:
        print(df)
        load_chose = get_accept(output="Do you want to load from a save? (y/n) \n> ")

        if load_chose:
            index = get_int("Which save do you want?\n> ", vaid_range=[0, num_lines])

            with open("save.csv", "r+") as load:

                reader_obj = list(csv.reader(load))
                
                attributes = reader_obj[index+1]
                map_load = attributes.pop()

            play(player_attributes=attributes, map_id=int(map_load))


        else:
            ask_tutorial()

    else:
        ask_tutorial()

def main():
    if __name__ == "__main__":
        start()

main()