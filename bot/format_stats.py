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