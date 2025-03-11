from game_tracker import GameTracker
import asyncio
import aiohttp
import re
from datetime import datetime
from tools import time_it


class NFLTracker(GameTracker):
    def __init__(self, api_key):
        super().__init__(api_key, "nfl")

    # USE REGEX TO FILTER THE URLS THAT ARE THE ACTUAL LIVE GAMES AND NOT THE FINAL GAMES

    async def fetch_game_urls(self):
        live_pattern = re.compile(
            r"^\d{4}reg/\d{2}/[a-z]{2,3}$", re.IGNORECASE)

        async with aiohttp.ClientSession() as session:
            async with session.get(self._METADATA) as response:
                if response.status != 200:
                    print("Error", response.status_code, response.text)

                data = await response.json()
                endpoints = data.get('AvailableEndpoints', [])

                playbyplay_endpoints = [
                    ep for ep in endpoints if "/playbyplay/" in ep]
                split_eps = [ep.split("/playbyplay/")[-1]
                             for ep in playbyplay_endpoints]
                valid_ids = [id for id in split_eps if live_pattern.match(id)]

                return [f"https://replay.sportsdata.io/api/v3/{self._league}/pbp/json/playbyplay/{valid_id}?key={self._API_KEY}" for valid_id in valid_ids]

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

        valid_games = [{
            'game_data': game,
            'game_key': game.get('Score', {}).get('GameKey')
        } for game in results if game is not None]

        unique_gamekeys = set()
        filtered_games = []

        for game in valid_games:
            game_key = game['game_key']
            if game_key not in unique_gamekeys:
                unique_gamekeys.add(game_key)
                filtered_games.append(game.get('game_data', {}))

        return filtered_games

    @time_it
    async def game_progresses(self):
        valid_games = await self.fetch_valid_game_urls()
        if not valid_games:
            print("📅 No games scheduled or in progress at the moment.")
            return

        scheduled_games = []
        ongoing_games = []
        completed_games = []

        for game_data in valid_games:
            league = {
                'nfl': {
                    'results': 'Score',
                    'status': 'Status',
                    'away_team': 'AwayTeam',
                    'home_team': 'HomeTeam',
                    'away_team_score': 'AwayScore',
                    'home_team_score': 'HomeScore',
                    'game_time': 'DateTime'
                },
            }
            game_info = game_data[league[self._league]["results"]]

            status = game_info.get(league[self._league]["status"], 'Unknown')
            away_team = game_info.get(
                league[self._league]["away_team"], 'Unknown')
            home_team = game_info.get(
                league[self._league]["home_team"], 'Unknown')
            away_team_score = game_info.get(
                league[self._league]["away_team_score"], 0)
            home_team_score = game_info.get(
                league[self._league]["home_team_score"], 0)
            datetime_str = game_info.get(league[self._league]["game_time"], '')

            if datetime_str:
                game_datetime = datetime.strptime(
                    datetime_str, "%Y-%m-%dT%H:%M:%S")
                game_time = game_datetime.strftime("%B %d, %Y - %I:%M %p")

            if status == 'Scheduled':
                scheduled_games.append(
                    f"🕒 {away_team} vs {home_team} is scheduled to start at {game_time} EST")
            elif status == "Final":
                completed_games.append(
                    f"✅ Final Score: {away_team} {away_team_score} - {home_team} {home_team_score}")
            else:
                ongoing_games.append(
                    f"Game in progress: {away_team} {away_team_score} - {home_team} {home_team_score} ")

        league_names = {
            "nfl": "🏈 ___NFL Games___ 🏈",
        }

        print(f"\n{league_names.get(self._league, '🏆 **Game Tracker** 🏆')}")

        if ongoing_games:
            print("\n🔥 **Ongoing Games:**")
            print("\n".join(ongoing_games))

        if scheduled_games:
            print("\n📅 **Upcoming Games:**")
            print("\n".join(scheduled_games))

        if completed_games:
            print("\n🏁 **Completed Games:**")
            print("\n".join(completed_games))

        if not (ongoing_games or scheduled_games or completed_games):
            print("📅 No games available at this moment.")
