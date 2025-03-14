from backend.trackers.game_tracker import GameTracker
import asyncio
from datetime import datetime
from backend.tools import time_it


class NBATracker(GameTracker):
    def __init__(self, api_key):
        super().__init__(api_key, "nba")

    @time_it
    async def get_live_scores(self):
        """
        API request for live score stats.
        """
        game_data = await self.fetch_all_playbyplay_data()

        live_score_data = []

        for game_info in game_data:
            game = game_info.get(
                self._leagues_stats[self._league]['game']['game_key'])
            status_ = game.get(
                self._leagues_stats[self._league]['game']['status'])

            live_score_data.append({
                'status': status_,
                'game_id': game.get(self._leagues_stats[self._league]['game']["game_id"], 'Unknown'),
                'season': game.get(self._leagues_stats[self._league]['game']["season"], 'Unknown'),
                'game_time': datetime.strptime(game.get(self._leagues_stats[self._league]['game']["game_time"], ''), "%Y-%m-%dT%H:%M:%S").strftime("%B %d, %Y - %I:%M %p") if game.get(self._leagues_stats[self._league]['game']["game_time"], '') else "Unknown",
                'away_team': game.get(self._leagues_stats[self._league]['game']["away_team"], 'Unknown'),
                'away_team_id': game.get(self._leagues_stats[self._league]['game']["away_team_id"], 'Unknown'),
                'home_team': game.get(self._leagues_stats[self._league]['game']["home_team"], 'Unknown'),
                'home_team_id': game.get(self._leagues_stats[self._league]['game']["home_team_id"], 'Unknown'),
                'away_team_score': game.get(self._leagues_stats[self._league]['game']["away_team_score"], 0),
                'home_team_score': game.get(self._leagues_stats[self._league]['game']["home_team_score"], 0),
                'channel': game.get(self._leagues_stats[self._league]['game']["channel"], 'Unknown'),
                'quarter': game.get(self._leagues_stats[self._league]['game']["quarter"], 'Unknown'),
                'minutes_remaining': game.get(self._leagues_stats[self._league]['game']["minutes_remaining"], 'Unknown'),
                'seconds_remaining': game.get(self._leagues_stats[self._league]['game']["seconds_remaining"], 'Unknown')
            })
        return live_score_data

    @time_it
    async def get_last_play(self):
        """
        API request for live last play stats.
        """

        game_data = await self.fetch_all_playbyplay_data()

        last_play_data = []

        for game_info in game_data:
            game = game_info.get(
                self._leagues_stats[self._league]['game']['game_key'])
            status = game.get(
                self._leagues_stats[self._league]['game']["status"], 'Unknown')

            last_play_data.append({
                'game_id': game.get(self._leagues_stats[self._league]['game']["game_id"], 'Unknown'),
                'last_play': game.get(self._leagues_stats[self._league]['game']["last_play"], 'Unknown'),
                'quarter': game.get(self._leagues_stats[self._league]['game']["quarter"], 'Unknown'),
                'minutes_remaining': game.get(self._leagues_stats[self._league]['game']["minutes_remaining"], 'Unknown'),
                'seconds_remaining': game.get(self._leagues_stats[self._league]['game']["seconds_remaining"], 'Unknown')
            })
        return last_play_data

    @time_it
    async def get_quarter_scores(self):
        """
        API request for live quarter stats.
        Name = GameID_quarters
        """
        game_data = await self.fetch_all_playbyplay_data()

        quarters_data = []

        for game_info in game_data:
            game = game_info.get(
                self._leagues_stats[self._league]['game']['game_key'])

            game_id = game.get(
                self._leagues_stats[self._league]['game']["game_id"], 'Unknown')

            quarters_data.append({
                f'{game_id}_quarters': {
                    "game_id": game_id,
                    "quarters": game.get(self._leagues_stats[self._league]['game']["quarters"], {'Unknown'})
                }
            })
        return quarters_data

    @time_it
    async def get_team_stats(self):
        """
        API request for live team stats.
        """
        # Fetch all boxscore data for games
        game_data = await self.fetch_all_boxscore_data()

        # Get the tea stats mapping from the league config
        team_stats_mapping = self._leagues_stats[self._league]['team']

        game_stats_list = []

        # Loops through each game
        for game_info in game_data:
            # Get the stats for both teams
            team_games = game_info.get(
                team_stats_mapping['team_key'], [])

            # Process stats for both teams in the game
            game_stat_both_teams = [
                {key: team.get(value) for key, value in team_stats_mapping.items(
                ) if key not in ['team_key']}
                for team in team_games
            ]

            game_stats_list.append(game_stat_both_teams)

        return game_stats_list

    @time_it
    async def get_player_stats(self):
        game_data = await self.fetch_all_boxscore_data()

        player_stats_mapping = self._leagues_stats[self._league]['players']
        game_stats_mapping = self._leagues_stats[self._league]['game']

        all_players_stats = []
        for game_info in game_data:
            players_stats = game_info.get(
                player_stats_mapping['players_key'], [])

            status = game_info.get(game_stats_mapping['status'], [])

            players_stats_both_teams = [
                {key: player.get(value) for key, value in player_stats_mapping.items(
                ) if key not in ['players_key']}
                for player in players_stats
            ]
            if players_stats_both_teams:
                all_players_stats.append(players_stats_both_teams)

        return all_players_stats
