import json

def format_player_stats(data, previous_data=None):
    # Extracting necessary data
    username = data["userName"]
    total_kills = data["kills"]
    top_weapon_type = max(data["weapons"], key=lambda x: x["kills"])
    top_vehicle = max(data["vehicles"], key=lambda x: x["kills"])
    kpm = data["killsPerMinute"]
    level =data["level"]

    # Notable Achievements
    longest_equipped = max(data["weapons"], key=lambda x: x["timeEquipped"])["weaponName"]
    longest_equipped_time = max(data["weapons"], key=lambda x: x["timeEquipped"])["timeEquipped"]
    highest_accuracy_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in  ['Melee', 'Shotguns']], key=lambda x: x["accuracy"])["weaponName"]
    highest_accuracy = max([weapon for weapon in data['weapons'] if weapon['type'] not in  ['Melee', 'Shotguns']], key=lambda x: x["accuracy"])["accuracy"]
    top_distance_vehicle = max(data["vehicles"], key=lambda x: x["distanceTraveled"])

    # Formatting the output
    output = f"🔥 **Player Highlights:**\n🔹 Username: {username} (lvl {level})\n🔹 Total Kills: {total_kills} ({kpm})\n"
    output += f"🔹 Top Weapon Type: {top_weapon_type['weaponName']} with {top_weapon_type['kills']} kills\n"
    output += f"🔹 Top Vehicle: {top_vehicle['vehicleName']} with {top_vehicle['kills']} kills\nNotable Achievements:\n"
    output += f"  🔸 Longest Equipped: {longest_equipped} for a total of {longest_equipped_time} seconds\n"
    output += f"  🔸 Highest Accuracy: {highest_accuracy_weapon} at {highest_accuracy}%\n"
    output += f"  🔸 Top Vehicle for Distance Traveled: {top_distance_vehicle['vehicleName']}, covering {top_distance_vehicle['distanceTraveled']} meters\n\n"

    # Top Weapons
    output += "🔫 **Top 5 Weapons:**\n"
    top_weapons = sorted(data["weapons"], key=lambda x: x['kills'], reverse=True)[:5]
    for weapon in top_weapons:
        output += f"🔹 {weapon['weaponName']}: {weapon['kills']} kills, {weapon['damagePerMinute']} damage per minute\n"

    # Top Vehicles
    output += "\n🚁 **Top 5 Vehicles:**\n"
    top_vehicles = sorted(data["vehicles"], key=lambda x: x['kills'], reverse=True)[:5]
    for vehicle in top_vehicles:
        output += f"🔹 {vehicle['vehicleName']}: {vehicle['kills']} kills, {vehicle['killsPerMinute']} kills per minute\n"

    # Accuracy & Efficiency
    output += "\n🎯 **Accuracy & Efficiency:**\n"
    output += f"🔹 Best Accuracy with a Weapon Type: {highest_accuracy_weapon} at {highest_accuracy}%\n"
    highest_kpm_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in ['Melee']], key=lambda x: x["killsPerMinute"])
    output += f"🔹 Highest Kills Per Minute (Weapon): {highest_kpm_weapon['weaponName']} with {highest_kpm_weapon['killsPerMinute']} KPM\n"
    weapon_with_most_headshots = max(data['weapons'], key=lambda x: x['headshots'])
    output += f"🔹 Weapon with the most Headshots: {weapon_with_most_headshots['weaponName']} with {weapon_with_most_headshots['headshots']} headshots\n"
    highest_kpm_vehicle = max(data["vehicles"], key=lambda x: x["killsPerMinute"])
    output += f"🔹 Highest Kills Per Minute (Vehicle): {highest_kpm_vehicle['vehicleName']} with {highest_kpm_vehicle['killsPerMinute']} KPM\n"

    # Explosive Impact
    output += "\n💥 **Explosive Impact:**\n"
    top_weapon_type = max(data["weapons"], key=lambda x: x["multiKills"])
    output += f"🔹 Most Multi-Kills: {top_weapon_type['weaponName']} with {top_weapon_type['multiKills']} multi-kills\n"
    top_multi_kills_vehicle = max(data["vehicles"], key=lambda x: x["multiKills"])
    output += f"🔹 Top Vehicle for Multi-Kills: {top_multi_kills_vehicle['vehicleName']} with {top_multi_kills_vehicle['multiKills']} multi-kills\n"

    # Defense & Support
    output += "\n🛡️ **Defense & Support:**\n"
    most_vehicles_destroyed = max(data["vehicles"], key=lambda x: x["vehiclesDestroyedWith"])
    output += f"🔹 Most Vehicles Destroyed: {most_vehicles_destroyed['vehicleName']} destroying {most_vehicles_destroyed['vehiclesDestroyedWith']} vehicles\n"
    top_support_vehicle = max(data["vehicles"], key=lambda x: x["assists"])
    output += f"🔹 Top Support Vehicle: {top_support_vehicle['vehicleName']} with {top_support_vehicle['assists']} assists\n"

    # Maps and Flags
    output += "\n🚩 PTFO:\n...Coming Soon\n"

    return output

def format_stat_change(current, previous, key):
    if previous and key in previous:
        change = current - previous[key]
        if change > 0:
            return f" [+{change} 🔼]"
        elif change < 0:
            return f"  [{change} 🔽]"
    return ""

def format_general_info(data, previous_data=None):
    username = data["userName"]
    level = data["level"]
    total_kills = data["kills"]
    kpm = data["killsPerMinute"]

    # Calculate differences if previous_data is provided
    level_change = format_stat_change(level, previous_data, "level") if previous_data else ""
    kills_change = format_stat_change(total_kills, previous_data, "kills") if previous_data else ""
    kpm_change = format_stat_change(kpm, previous_data, "killsPerMinute") if previous_data else ""

    output = f""
    output += f"🔹 Username: {username} (lvl {level}{level_change})\n"
    output += f"🔹 Total Kills: {total_kills}{kills_change}\n"
    output += f"🔹 Kills Per Minute: {kpm}{kpm_change} KPM\n"
    return output


def find_previous_top_weapon(previous_data):
    if previous_data and "weapons" in previous_data:
        return max(previous_data["weapons"], key=lambda x: x["kills"])
    return None


def find_previous_top_item(previous_data, item_type):
    """
    Finds the top item (weapon or vehicle) from the previous data set based on kills.

    :param previous_data: The previous stats data.
    :param item_type: A string indicating the type of items to search ('weapons' or 'vehicles').
    :return: The top item based on kills from the previous data set, or None if not applicable.
    """
    if previous_data and item_type in previous_data:
        return max(previous_data[item_type], key=lambda x: x["kills"], default=None)
    return None

def format_top_weapon(data, previous_data=None):
    top_weapon_type = max(data["weapons"], key=lambda x: x["kills"])
    previous_top_weapon = find_previous_top_item(previous_data, "weapons")

    weapon_change_str = ""
    if previous_top_weapon:
        if top_weapon_type['weaponName'] == previous_top_weapon['weaponName']:
            # If the top weapon is the same, show kills change
            kills_change = format_stat_change(top_weapon_type['kills'], previous_top_weapon, "kills")
            weapon_change_str = f" {kills_change}" if kills_change else ""
        else:
            # If the top weapon has changed, indicate the new and previous top weapon
            weapon_change_str = f" (🔄 {previous_top_weapon['weaponName']}, ⤴️{top_weapon_type['weaponName']})"

    return f"🔹 Top Weapon Type: {top_weapon_type['weaponName']} with {top_weapon_type['kills']} kills{weapon_change_str}\n"


def format_top_vehicle(data, previous_data=None):
    top_vehicle = max(data["vehicles"], key=lambda x: x["kills"])
    previous_top_vehicle = find_previous_top_item(previous_data, "vehicles")

    vehicle_change_str = ""
    if previous_top_vehicle:
        if top_vehicle['vehicleName'] == previous_top_vehicle['vehicleName']:
            # If the top vehicle is the same, show kills change
            kills_change = format_stat_change(top_vehicle['kills'], previous_top_vehicle, "kills")
            vehicle_change_str = f" {kills_change}" if kills_change else ""
        else:
            # If the top vehicle has changed, indicate the new and previous top vehicle
            vehicle_change_str = f" (🔄 {previous_top_vehicle['vehicleName']}, ⤴️ {top_vehicle['vehicleName']})"

    return f"🔹 Top Vehicle: {top_vehicle['vehicleName']} with {top_vehicle['kills']} kills{vehicle_change_str}\n"


def format_notable_achievements(data, previous_data=None):
    achievements = ""

    # Current notable achievements
    longest_equipped_weapon = max(data["weapons"], key=lambda x: x["timeEquipped"])
    highest_accuracy_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in ['Melee', 'Shotguns']],
                                  key=lambda x: x["accuracy"])
    top_distance_vehicle = max(data["vehicles"], key=lambda x: x["distanceTraveled"])

    # Previous notable achievements for comparison
    if previous_data:
        previous_longest_equipped_weapon = max(previous_data["weapons"], key=lambda x: x["timeEquipped"])
        previous_highest_accuracy_weapon = max(
            [weapon for weapon in previous_data['weapons'] if weapon['type'] not in ['Melee', 'Shotguns']],
            key=lambda x: x["accuracy"])
        previous_top_distance_vehicle = max(previous_data["vehicles"], key=lambda x: x["distanceTraveled"])
    else:
        previous_longest_equipped_weapon = previous_highest_accuracy_weapon = previous_top_distance_vehicle = None

    # Calculate and format changes
    longest_equipped_change = format_stat_change(longest_equipped_weapon['timeEquipped'],
                                                 previous_longest_equipped_weapon,
                                                 "timeEquipped") if previous_longest_equipped_weapon else ""
    highest_accuracy_change = format_stat_change(highest_accuracy_weapon['accuracy'], previous_highest_accuracy_weapon,
                                                 "accuracy") if previous_highest_accuracy_weapon else ""
    top_distance_change = format_stat_change(top_distance_vehicle['distanceTraveled'], previous_top_distance_vehicle,
                                             "distanceTraveled") if previous_top_distance_vehicle else ""

    achievements += f"  🔸 Longest Equipped: {longest_equipped_weapon['weaponName']} for a total of {longest_equipped_weapon['timeEquipped']} seconds{longest_equipped_change}\n"
    achievements += f"  🔸 Highest Accuracy: {highest_accuracy_weapon['weaponName']} at {highest_accuracy_weapon['accuracy']}%{highest_accuracy_change}\n"
    achievements += f"  🔸 Top Vehicle for Distance Traveled: {top_distance_vehicle['vehicleName']}, covering {top_distance_vehicle['distanceTraveled']} meters{top_distance_change}\n\n"

    return achievements

def format_section_header(title):
    return f"\n**{title}**:\n"

def calculate_rank_changes(current_top_items, previous_top_items, item_key):
    """
    Calculate the changes in rank for the top items (weapons, vehicles, etc.).
    :param current_top_items: List of the current top items, sorted.
    :param previous_top_items: List of the previous top items, sorted.
    :param item_key: The key in the item dictionary to use for identification (e.g., 'weaponName' or 'vehicleName').
    :return: A dictionary with item names as keys and rank change as values.
    """
    rank_changes = {}
    # Use the provided item_key to identify items
    previous_ranks = {item[item_key]: i for i, item in enumerate(previous_top_items)}

    for i, item in enumerate(current_top_items):
        item_name = item[item_key]
        previous_rank = previous_ranks.get(item_name)
        if previous_rank is None:
            rank_changes[item_name] = "New"
        else:
            change = previous_rank - i
            rank_changes[item_name] = change

    return rank_changes


def format_weapons_section(data, previous_data=None):
    output = ""
    top_weapons = sorted(data["weapons"], key=lambda x: x['kills'], reverse=True)[:5]
    previous_top_weapons = sorted(previous_data["weapons"], key=lambda x: x['kills'], reverse=True)[
                           :5] if previous_data else []

    rank_changes = calculate_rank_changes(top_weapons, previous_top_weapons, 'weaponName')

    for weapon in top_weapons:
        weapon_name = weapon['weaponName']
        rank_change = rank_changes.get(weapon_name)
        change_annotation = ""
        if isinstance(rank_change, int):
            if rank_change > 0:
                change_annotation = f" (🔼{abs(rank_change)} spots)"
            elif rank_change < 0:
                change_annotation = f" (🔽{abs(rank_change)} spots)"
        elif rank_change == "New":
            change_annotation = " (🆕 New Entry)"

        output += f"🔹 {weapon_name}: {weapon['kills']} kills, {weapon['damagePerMinute']} damage per minute{change_annotation}\n"

    return output


def format_vehicles_section(data, previous_data=None):
    output = ""
    top_vehicles = sorted(data["vehicles"], key=lambda x: x['kills'], reverse=True)[:5]
    previous_top_vehicles = sorted(previous_data["vehicles"], key=lambda x: x['kills'], reverse=True)[
                            :5] if previous_data else []

    rank_changes = calculate_rank_changes(top_vehicles, previous_top_vehicles, 'vehicleName')

    for vehicle in top_vehicles:
        vehicle_name = vehicle['vehicleName']
        rank_change = rank_changes.get(vehicle_name)
        change_annotation = ""
        if isinstance(rank_change, int):
            if rank_change > 0:
                change_annotation = f" (🔼{abs(rank_change)} spots)"
            elif rank_change < 0:
                change_annotation = f" (🔽{abs(rank_change)} spots)"
        elif rank_change == "New":
            change_annotation = " (🆕 New Entry)"

        output += f"🔹 {vehicle_name}: {vehicle['kills']} kills, {vehicle['killsPerMinute']} kills per minute{change_annotation}\n"

    return output

def format_accuracy_efficiency(data):
    highest_accuracy_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in ['Melee', 'Shotguns']], key=lambda x: x["accuracy"])
    highest_kpm_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in ['Melee']], key=lambda x: x["killsPerMinute"])
    weapon_with_most_headshots = max(data['weapons'], key=lambda x: x['headshots'])
    highest_kpm_vehicle = max(data["vehicles"], key=lambda x: x["killsPerMinute"])

    output = ""
    output += f"🔹 Best Accuracy with a Weapon Type: {highest_accuracy_weapon['weaponName']} at {highest_accuracy_weapon['accuracy']}%\n"
    output += f"🔹 Highest Kills Per Minute (Weapon): {highest_kpm_weapon['weaponName']} with {highest_kpm_weapon['killsPerMinute']} KPM\n"
    output += f"🔹 Weapon with the Most Headshots: {weapon_with_most_headshots['weaponName']} with {weapon_with_most_headshots['headshots']} headshots\n"
    output += f"🔹 Highest Kills Per Minute (Vehicle): {highest_kpm_vehicle['vehicleName']} with {highest_kpm_vehicle['killsPerMinute']} KPM\n"
    return output

def format_explosive_impact(data):
    top_weapon_multi_kills = max(data["weapons"], key=lambda x: x["multiKills"])
    top_vehicle_multi_kills = max(data["vehicles"], key=lambda x: x["multiKills"])

    output = ""
    output += f"🔹 Most Multi-Kills (Weapon): {top_weapon_multi_kills['weaponName']} with {top_weapon_multi_kills['multiKills']} multi-kills\n"
    output += f"🔹 Top Vehicle for Multi-Kills: {top_vehicle_multi_kills['vehicleName']} with {top_vehicle_multi_kills['multiKills']} multi-kills\n"
    return output

def format_defense_support(data):
    most_vehicles_destroyed = max(data["vehicles"], key=lambda x: x["vehiclesDestroyedWith"])
    top_support_vehicle = max(data["vehicles"], key=lambda x: x["assists"])

    output = ""
    output += f"🔹 Most Vehicles Destroyed: {most_vehicles_destroyed['vehicleName']} destroying {most_vehicles_destroyed['vehiclesDestroyedWith']} vehicles\n"
    output += f"🔹 Top Support Vehicle: {top_support_vehicle['vehicleName']} with {top_support_vehicle['assists']} assists\n"
    return output

def format_maps_flags():
    # Placeholder for future implementation
    return "\n🚩 **PTFO:**\n...Coming Soon\n"

def format_player_stats_v2(data, previous_data=None):
    output = ""

    output += format_section_header("🔥 Player Highlights")
    output += format_general_info(data, previous_data)
    output += format_top_weapon(data, previous_data)
    output += format_top_vehicle(data, previous_data)
    output += format_section_header("🥇 Notable Achievements")
    output += format_notable_achievements(data, previous_data)
    output += format_section_header("🔫 Top 5 Weapons")
    output += format_weapons_section(data, previous_data)
    output += format_section_header("🚁 Top 5 Vehicles")
    output += format_vehicles_section(data, previous_data)
    output += format_section_header("🎯 Accuracy & Efficiency")
    output += format_accuracy_efficiency(data)
    output += format_section_header("💥 Explosive Impact")
    output += format_explosive_impact(data)
    output += format_section_header("️🛡️ Defense & Support")
    output += format_defense_support(data)
    output += format_maps_flags()

    return output