from game_tracker import GameTracker
import asyncio
from datetime import datetime
from tools import time_it


class NBATracker(GameTracker):
    def __init__(self, api_key):
        super().__init__(api_key, "nba")

    @time_it
    async def get_live_scores(self):
        """
        API request for live score stats.
        """
        game_data = await self.fetch_all_game_data()

        live_score_data = []

        for game_info in game_data:
            status = game_info.get(
                self._leagues_stats[self._league]['game']["status"], 'Unknown')

            live_score_data.append({
                'status': status,
                'game_id': game_info.get(self._leagues_stats[self._league]['game']["game_id"], 'Unknown'),
                'game_time': datetime.strptime(game_info.get(self._leagues_stats[self._league]['game']["game_time"], ''), "%Y-%m-%dT%H:%M:%S").strftime("%B %d, %Y - %I:%M %p") if game_info.get(self._leagues_stats[self._league]['game']["game_time"], '') else "Unknown",
                'away_team': game_info.get(self._leagues_stats[self._league]['game']["away_team"], 'Unknown'),
                'away_team_id': game_info.get(self._leagues_stats[self._league]['game']["away_team_id"], 'Unknown'),
                'home_team': game_info.get(self._leagues_stats[self._league]['game']["home_team"], 'Unknown'),
                'home_team_id': game_info.get(self._leagues_stats[self._league]['game']["home_team_id"], 'Unknown'),
                'away_team_score': game_info.get(self._leagues_stats[self._league]['game']["away_team_score"], 0),
                'home_team_score': game_info.get(self._leagues_stats[self._league]['game']["home_team_score"], 0),
                'channel': game_info.get(self._leagues_stats[self._league]['game']["channel"], 'Unknown'),
                'quarter': game_info.get(self._leagues_stats[self._league]['game']["quarter"], 'Unknown'),
                'minutes_remaining': game_info.get(self._leagues_stats[self._league]['game']["minutes_remaining"], 'Unknown'),
                'seconds_remaining': game_info.get(self._leagues_stats[self._league]['game']["seconds_remaining"], 'Unknown')
            })
        return live_score_data

    async def get_last_play(self):
        """
        API request for live last play stats.
        """

        game_data = await self.fetch_all_game_data()

        last_play_data = []

        for game_info in game_data:
            status = game_info.get(
                self._leagues_stats[self._league]['game']["status"], 'Unknown')

            last_play_data.append({
                'game_id': game_info.get(self._leagues_stats[self._league]['game']["game_id"], 'Unknown'),
                'last_play': game_info.get(self._leagues_stats[self._league]['game']["last_play"], 'Unknown'),
                'quarter': game_info.get(self._leagues_stats[self._league]['game']["quarter"], 'Unknown'),
                'minutes_remaining': game_info.get(self._leagues_stats[self._league]['game']["minutes_remaining"], 'Unknown'),
                'seconds_remaining': game_info.get(self._leagues_stats[self._league]['game']["seconds_remaining"], 'Unknown')
            })
        return last_play_data

    async def get_quarter_scores(self):
        """
        API request for live quarter stats.
        Name = GameID_quarters
        """
        game_data = await self.fetch_all_game_data()

        quarters_data = []

        for game_info in game_data:
            game_id = game_info.get(
                self._leagues_stats[self._league]['game']["game_id"], 'Unknown')

            quarters_data.append({
                f'{game_id}_quarters': game_info.get(self._leagues_stats[self._league]['game']["quarters"], {'Unknown'})
            })
        return quarters_data

    async def get_team_stats(self):
        """
        API request for live team stats.
        """
        team_data = await self.fetch_all_team_data()

        return team_data

    async def get_player_data(self):
        pass
