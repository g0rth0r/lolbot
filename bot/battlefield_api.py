import requests

class BattlefieldAPI:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_player_stats(self, player_id=None, player_name=None, platform='pc'):
        """Fetches player stats from the Battlefield 2042 API."""
        params = {
            "platform": platform,
            "format_values": False
        }
        if player_id:
            params["playerid"] = player_id
        elif player_name:
            params["name"] = player_name
        else:
            raise ValueError("Either player_id or player_name must be provided")

        response = requests.get(f"{self.base_url}/bf2042/stats/", params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch stats: {response.status_code}, {response.text}")
            return None
