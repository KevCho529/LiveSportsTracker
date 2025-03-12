import asyncio
import aiohttp
from datetime import datetime


class GameTracker():
    def __init__(self, api_key, league):
        self._API_KEY = api_key
        self._METADATA = f"https://replay.sportsdata.io/api/metadata?key={self._API_KEY}"
        self._league = league

    async def fetch_game_urls(self, session):
        try:
            async with session.get(self._METADATA) as response:
                if response.status != 200:
                    print(f"❌ Error {response.status}: {await response.text()}")
                    return []
                try:
                    data = await response.json()
                except Exception as e:
                    print(f"❌ Failed to parse JSON response: {e}")
                    return []
                endpoints = data.get('AvailableEndpoints', [])

                playbyplay_endpoints = [
                    ep for ep in endpoints if "/playbyplay/" in ep]
                game_ids = [ep.split("/playbyplay/")[-1]
                            for ep in playbyplay_endpoints]

                return [f"https://replay.sportsdata.io/api/v3/{self._league}/pbp/json/playbyplay/{game_id}?key={self._API_KEY}" for game_id in game_ids]
        except Exception as e:
            print(f"❌ Failed to fetch game URLs: {e}")
            return []

    async def fetch_valid_game_urls(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as session:
            game_urls = await self.fetch_game_urls(session)

            if not game_urls:
                return []

            async def fetch_game(session, url):
                try:
                    async with session.get(url, timeout=10) as response:
                        if response.status != 200:
                            print(
                                f"⚠️ Skipping {url}, Status: {response.status}")
                            return None
                        return await response.json()
                except Exception as e:
                    print(f"❌ Failed to fetch {url}: {e}")
                    return None

            # All the items are couroutine objects, so use gather to start all couritines at once
            tasks = [fetch_game(session, url)
                     for url in game_urls]
            results = await asyncio.gather(*tasks)

            return [game for game in results if game is not None]
