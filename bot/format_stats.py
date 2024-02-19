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

    # Only compare kills if the top weapon remains the same
    kills_change = ""
    if previous_top_weapon and top_weapon_type['weaponName'] == previous_top_weapon['weaponName']:
        kills_change = format_stat_change(top_weapon_type['kills'], previous_top_weapon, "kills")

    return f"🔹 Top Weapon Type: {top_weapon_type['weaponName']} with {top_weapon_type['kills']} kills{kills_change}\n"


def format_top_vehicle(data, previous_data=None):
    top_vehicle = max(data["vehicles"], key=lambda x: x["kills"])
    previous_top_vehicle = find_previous_top_item(previous_data, "vehicles")

    # Only compare kills if the top vehicle remains the same
    kills_change = ""
    if previous_top_vehicle and top_vehicle['vehicleName'] == previous_top_vehicle['vehicleName']:
        kills_change = format_stat_change(top_vehicle['kills'], previous_top_vehicle, "kills")

    return f"🔹 Top Vehicle: {top_vehicle['vehicleName']} with {top_vehicle['kills']} kills{kills_change}\n"


def format_notable_achievements(data):
    achievements = ""
    longest_equipped_weapon = max(data["weapons"], key=lambda x: x["timeEquipped"])
    highest_accuracy_weapon = max([weapon for weapon in data['weapons'] if weapon['type'] not in ['Melee', 'Shotguns']], key=lambda x: x["accuracy"])
    top_distance_vehicle = max(data["vehicles"], key=lambda x: x["distanceTraveled"])
    achievements += f"  🔸 Longest Equipped: {longest_equipped_weapon['weaponName']} for a total of {longest_equipped_weapon['timeEquipped']} seconds\n"
    achievements += f"  🔸 Highest Accuracy: {highest_accuracy_weapon['weaponName']} at {highest_accuracy_weapon['accuracy']}%\n"
    achievements += f"  🔸 Top Vehicle for Distance Traveled: {top_distance_vehicle['vehicleName']}, covering {top_distance_vehicle['distanceTraveled']} meters\n\n"
    return achievements

def format_section_header(title):
    return f"\n**{title}**:\n"

def format_weapons_section(data):
    output = ""
    top_weapons = sorted(data["weapons"], key=lambda x: x['kills'], reverse=True)[:5]
    for weapon in top_weapons:
        output += f"🔹 {weapon['weaponName']}: {weapon['kills']} kills, {weapon['damagePerMinute']} damage per minute\n"
    return output

def format_vehicles_section(data):
    output = ""
    top_vehicles = sorted(data["vehicles"], key=lambda x: x['kills'], reverse=True)[:5]
    for vehicle in top_vehicles:
        output += f"🔹 {vehicle['vehicleName']}: {vehicle['kills']} kills, {vehicle['killsPerMinute']} kills per minute\n"
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
    output += format_notable_achievements(data)
    output += format_section_header("🔫 Top 5 Weapons")
    output += format_weapons_section(data)
    output += format_section_header("🚁 Top 5 Vehicles")
    output += format_vehicles_section(data)
    output += format_section_header("🎯 Accuracy & Efficiency")
    output += format_accuracy_efficiency(data)
    output += format_section_header("💥 Explosive Impact")
    output += format_explosive_impact(data)
    output += format_section_header("️🛡️ Defense & Support")
    output += format_defense_support(data)
    output += format_maps_flags()

    return output