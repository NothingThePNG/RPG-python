from classes import *

def equipped(player: Player) -> str:
    """
    This Python function takes a Player object as input and returns a string describing the player's
    equipped armor and weapon, including their respective attributes.
    
    :param player: The function `equipped` takes a `Player` object as input and returns a string
    describing the player's equipped armor and weapon
    :type player: Player
    :return: The function `equipped(player: Player) -> str` returns a string that provides information
    about the player's equipped armor and weapon. If the player has equipped armor, it includes the
    armor's name and the amount of armor it provides. If the player has equipped a weapon, it includes
    the weapon's name, the calculated damage taking into account the player's damage multiplier, and the
    armor penetrating value
    """
    ret = ""
    if player.armor != None:
        ret += f"\n\n{player.name}'s armor: {player.armor[0]} giving +{player.armor[2]} armor\n"
    else:
        ret += f"\n\n{player.name} has no equipped armor\n"
    
    if player.weapon != None:
        ret += f"""\n\n{player.name}'s weapon: {player.weapon[0]} giving 
        {round((player.weapon[2] * player.damage_multi), 3)} damage 
        {player.weapon[3]} armor penetrating
        """
    else:
        ret += f"{player.name} has no weapon\n"

    return ret

def equip(player: Player, num: int) -> None:
    item = player.items.pop((num-1))

    if item[1] == "A":
        if player.armor != None:
            player.items.append(player.armor)
        player.e_armour(armor=item)

    if item[1] == "W":
        if player.weapon != None:
            player.items.append(player.weapon)
        player.e_weapon(weapon=item)


def drop(player: Player, num: int) -> None:
    if num-1 < len(player.items) and num-1 >= 0:

        print(f"Dropped {player.items[num-1]}")
        del player.items[num-1]
    
    else:
        print("Invalid number")


def get_item(player: Player) -> int:
    player_items = []

    for item in player.items:

        if item == None:
            continue

        elif item[1] == "A":
            player_items.append(f"Armor: {item[0]} will give {item[2]} armor")

        elif item[1] == "W":
            player_items.append(f"Weapon: {item[0]} with a {item[2]} damage and {item[3]} armor penetrating")

    player_items.append("Exit")

    return Select_item(f"{equipped(player=player)}\n{Colors.orange}Your items:", items=player_items)()



def inventory(player: Player) -> None:
    """
    This Python function manages a player's inventory by allowing them to interact with items such as
    equipping or dropping them.
    
    :param player: The `inventory` function seems to be a part of a game inventory system where the
    player can interact with their items. It looks like it allows the player to select an item from
    their inventory and then choose to equip, drop, or cancel the action
    :type player: Player
    """
    item_index = get_item(player=player)
    
    
    while item_index != len(player.items):
        clear_screen()

        item = player.items[item_index-1]

        action = Select_item(f"What do you want to do with {item[0]}?", ["Equip", "Cancel", "Drop"])()

        if action == 0:
            equip(player=player, num=item_index)
        
        elif action == 2:
            drop(player=player, num=item_index)
        
        
        item_index = get_item(player=player)

