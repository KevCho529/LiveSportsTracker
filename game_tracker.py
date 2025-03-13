import asyncio
import aiohttp
from datetime import datetime


class GameTracker():
    def __init__(self, api_key, league):
        self._API_KEY = api_key
        self._METADATA = f"https://replay.sportsdata.io/api/metadata?key={self._API_KEY}"
        self._league = league
        self._leagues_stats = {
            'nba': {
                'game': {
                    'game_key': 'Game',
                    'game_id': 'GameID',
                    'status': 'Status',
                    'game_time': 'DateTime',
                    'away_team': 'AwayTeam',
                    'away_team_id': 'AwayTeamID',
                    'home_team': 'HomeTeam',
                    'home_team_id': 'HomeTeamID',
                    'away_team_score': 'AwayTeamScore',
                    'home_team_score': 'HomeTeamScore',
                    'channel': 'Channel',
                    'quarter': 'Quarter',
                    'minutes_remaining': 'TimeRemainingMinutes',
                    'seconds_remaining': 'TimeRemainingSeconds',
                    'last_play': 'LastPlay',
                    'quarters': 'Quarters'
                },
                'team': {
                    'team_key': 'TeamGames',
                    'game_id': 'GameID'
                }
            },
            'nfl': {
                'results': 'Score',
                'status': 'Status',
                'away_team': 'AwayTeam',
                'home_team': 'HomeTeam',
                'away_team_score': 'AwayScore',
                'home_team_score': 'HomeScore',
                'game_time': 'DateTime'
            },
            'nhl': {
                'results': 'Game',
                'status': 'Status',
                'away_team': 'AwayTeam',
                'home_team': 'HomeTeam',
                'away_team_score': 'AwayTeamScore',
                'home_team_score': 'HomeTeamScore',
                'game_time': 'DateTime'
            }
        }

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

    async def fetch_all_game_data(self):
        valid_games = await self.fetch_valid_game_urls()
        if not valid_games:
            print("📅 No games scheduled or in progress at the moment.")
            return

        return [game_data[self._leagues_stats[self._league]['game']["game_key"]] for game_data in valid_games]

    async def fetch_all_team_data(self):
        valid_games = await self.fetch_valid_game_urls()
        if not valid_games:
            print("📅 No games scheduled or in progress at the moment.")
            return

        return valid_games
