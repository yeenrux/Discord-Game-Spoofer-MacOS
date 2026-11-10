import json
from urllib.request import Request, urlopen

def fetch():
    req = Request("https://discord.com/api/v10/applications/detectable", headers={"User-Agent": "Mozilla/5.0"})
    with urlopen(req) as response:
        payload = json.load(response)
    games = {str(item["id"]): item["name"] for item in payload
             if item.get("id") and item.get("name")}
    return sorted(((name, game_id) for game_id, name in games.items()), key=lambda pair: (pair[0].casefold(), pair[1]))
