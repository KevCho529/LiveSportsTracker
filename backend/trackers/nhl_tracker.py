from backend.trackers.game_tracker import GameTracker
import asyncio
from datetime import datetime
from backend.tools import time_it


class NHLTracker(GameTracker):
    def __init__(self, api_key):
        super().__init__(api_key, "nhl")

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
            "nhl": "🏒 ___NHL Games___ 🏒",
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
