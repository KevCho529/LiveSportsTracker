import asyncio
import aiohttp
from datetime import datetime


class GameTracker():
    def __init__(self, api_key, league):
        self._API_KEY = api_key
        self._METADATA = f"https://replay.sportsdata.io/api/metadata?key={self._API_KEY}"
        self._league = league

    async def fetch_game_urls(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self._METADATA) as response:
                if response.status != 200:
                    print("Error", response.status_code, response.text)

                data = await response.json()
                endpoints = data.get('AvailableEndpoints', [])

                playbyplay_endpoints = [
                    ep for ep in endpoints if "/playbyplay/" in ep]
                game_ids = [ep.split("/playbyplay/")[-1]
                            for ep in playbyplay_endpoints]

                return [f"https://replay.sportsdata.io/api/v3/{self._league}/pbp/json/playbyplay/{game_id}?key={self._API_KEY}" for game_id in game_ids]

    async def fetch_valid_game_urls(self):
        game_urls = await self.fetch_game_urls()
        valid_games = []

        async def fetch_game(session, url):
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return await response.json()

        # Creaste a async session to grab the data
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as session:
            # All the items are couroutine objects, so use gather to start all couritines at once
            tasks = [fetch_game(session, url)
                     for url in game_urls]
            results = await asyncio.gather(*tasks)

        return [game for game in results if game is not None]
