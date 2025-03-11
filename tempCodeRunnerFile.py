                valid_ids = [id for id in split_eps if live_pattern.match(id)]

                return [f"https://replay.sportsdata.io/api/v3/{self._league}/pbp/json/playbyplay/{valid_id}?key={self._API_KEY}" for valid_id in valid_ids]

    async def fetch_valid_game_urls(self):
        game_urls = await self.fetch_game_urls()
        valid_games = []

        async def fetch_game(session, url):
            async with session.get(url, timeout=4) as response:
                if response.status != 200:
                    print(
                        f"Failed to fetch: {url} - Status {response.status}")
                    return None
                return await response.json()

        # Creaste a async session to grab the data
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnect