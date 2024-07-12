from g_print import *
from get_type import *
from random import *
from time import sleep
from classes import *



creature_types = [["rat", 10], ["spider", 5]]

player = Player()

def make_enemys(min, max):
    count = randint(min, max)
    ret = []
    for i in range(count):
        ret.append(Creature(choice(creature_types)))

    return ret

def combat():
    print(f"You have {player.health}HP")

    hostile = make_enemys(1, 4)

    g_print_str("You are attacked by:")
    for i in hostile:
        i.enemys.append(player)
        g_print_str(f"    -   {i}")
    
    sleep(1)

    print()

    player.enemys = hostile

    while len(hostile) > 0 and player.health > 0:
        for i in hostile:
            i.attack(None)
            sleep(1)

        action = get_int(first_out="Do you want to \n1: Heal \n2: Attack\n", output="\nDo you want to \n1: Heal \n2: Attack\n", vaid_range=[1, 3])

        if action == 1:
            player.heal()
        elif action == 2:
            attacking = get_int(output="Who do you want to attack?: ", vaid_range=[0, len(hostile)+1])-1

            player.attack(attacking)
        sleep(1)



def play():
    combat()


def main():
    if __name__ == "__main__":
        play()

main()