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
                    'season': 'Season',
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
                    'game_id': 'GameID',
                    'stat_id': 'StatID',
                    'team_id': 'TeamID',
                    'season': 'Season',
                    'name': 'Name',
                    'team': 'Team',
                    'global_team_id': 'GlobalTeamID',
                    'opponent_id': 'OpponentID',
                    'opponent': 'Opponent',
                    'home_or_away': 'HomeOrAway',
                    'is_game_over': 'IsGameOver',
                    'global_game_id': 'GlobalGameID',
                    'global_opponent_id': 'GlobalOpponentID',
                    'field_goals_made': 'FieldGoalsMade',
                    'field_goals_attempted': 'FieldGoalsAttempted',
                    'field_goals_percentage': 'FieldGoalsPercentage',
                    'effective_field_goals_percentage': 'EffectiveFieldGoalsPercentage',
                    'two_pointers_made': 'TwoPointersMade',
                    'two_pointers_attempted': 'TwoPointersAttempted',
                    'two_pointers_percentage': 'TwoPointersPercentage',
                    'three_pointers_made': 'ThreePointersMade',
                    'three_pointers_attempted': 'ThreePointersAttempted',
                    'three_pointers_percentage': 'ThreePointersPercentage',
                    'free_throws_made': 'FreeThrowsMade',
                    'free_throws_attempted': 'FreeThrowsAttempted',
                    'free_throws_percentage': 'FreeThrowsPercentage',
                    'offensive_rebounds': 'OffensiveRebounds',
                    'defensive_rebounds': 'DefensiveRebounds',
                    'rebounds': 'Rebounds',
                    'offensive_rebounds_percentage': 'OffensiveReboundsPercentage',
                    'defensive_rebounds_percentage': 'DefensiveReboundsPercentage',
                    'total_rebounds_percentage': 'TotalReboundsPercentage',
                    'assists': 'Assists',
                    'steals': 'Steals',
                    'blocked_shots': 'BlockedShots',
                    'turnovers': 'Turnovers',
                    'personal_fouls': 'PersonalFouls',
                    'points': 'Points',
                    'plus_minus': 'PlusMinus',
                    'is_closed': 'IsClosed',
                },
                'players': {
                    'players_key': 'PlayerGames',
                    'stat_id': 'StatID',
                    'team_id': 'TeamID',
                    'game_id': 'GameID',
                    'player_id': 'PlayerID',
                    'name': 'Name',
                    'team': 'Team',
                    'position': 'Position',
                    'started': 'Started',
                    'injury_status': 'InjuryStatus',
                    'injury_body_part': 'InjuryBodyPart',
                    'injury_start_date': 'InjuryStartDate',
                    'injury_notes': 'InjuryNotes',
                    'global_team_id': 'GlobalTeamID',
                    'opponent_id': 'OpponentID',
                    'opponent': 'Opponent',
                    'is_game_over': 'IsGameOver',
                    'global_game_id': 'GlobalGameID',
                    'global_opponent_id': 'GlobalOpponentID',
                    'minutes': 'Minutes',
                    'seconds': 'Seconds',
                    'field_goals_made': 'FieldGoalsMade',
                    'field_goals_attempted': 'FieldGoalsAttempted',
                    'field_goals_percentage': 'FieldGoalsPercentage',
                    'two_pointers_made': 'TwoPointersMade',
                    'two_pointers_attempted': 'TwoPointersAttempted',
                    'two_pointers_percentage': 'TwoPointersPercentage',
                    'three_pointers_made': 'ThreePointersMade',
                    'three_pointers_attempted': 'ThreePointersAttempted',
                    'three_pointers_percentage': 'ThreePointersPercentage',
                    'free_throws_made': 'FreeThrowsMade',
                    'free_throws_attempted': 'FreeThrowsAttempted',
                    'free_throws_percentage': 'FreeThrowsPercentage',
                    'offensive_rebounds': 'OffensiveRebounds',
                    'defensive_rebounds': 'DefensiveRebounds',
                    'rebounds': 'Rebounds',
                    'assists': 'Assists',
                    'steals': 'Steals',
                    'blocked_shots': 'BlockedShots',
                    'turnovers': 'Turnovers',
                    'personal_fouls': 'PersonalFouls',
                    'points': 'Points',
                    'player_efficiency_rating': 'PlayerEfficiencyRating',
                    'usage_rate_percentage': 'UsageRatePercentage',
                    'plus_minus': 'PlusMinus',
                    'is_closed': 'IsClosed',
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
                boxscore_endpoints = [
                    ep for ep in endpoints if "/boxscore/" in ep]

                playbyplay_ids = [ep.split("/playbyplay/")[-1]
                                  for ep in playbyplay_endpoints]
                boxscore_ids = [ep.split("/boxscore/")[-1]
                                for ep in boxscore_endpoints]

                playbyplay_urls = [
                    f"https://replay.sportsdata.io/api/v3/{self._league}/pbp/json/playbyplay/{playbyplay_id}?key={self._API_KEY}" for playbyplay_id in playbyplay_ids]
                boxscore_urls = [
                    f"https://replay.sportsdata.io/api/v3/{self._league}/stats/json/boxscore/{boxscore_id}?key={self._API_KEY}" for boxscore_id in boxscore_ids]
                return playbyplay_urls, boxscore_urls
        except Exception as e:
            print(f"❌ Failed to fetch game URLs: {e}")
            return []

    async def fetch_valid_game_urls(self):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=50)) as session:
            playbyplay_urls, boxscore_urls = await self.fetch_game_urls(session)

            if not playbyplay_urls and not boxscore_urls:
                return [], []

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

            tasks_playbyplay = [fetch_game(session, url)
                                for url in playbyplay_urls]
            tasks_boxscore = [fetch_game(session, url)
                              for url in boxscore_urls]

            playbyplay_results = await asyncio.gather(
                *tasks_playbyplay
            )
            boxscore_results = await asyncio.gather(
                *tasks_boxscore
            )

            return playbyplay_results, boxscore_results

    async def fetch_all_playbyplay_data(self):
        valid_games = await self.fetch_valid_game_urls()
        if not valid_games:
            print("📅 No games scheduled or in progress at the moment.")
            return

        valid_playbyplay_games = valid_games[0]

        playbyplay_games_filtered = self.filter_valid_games(
            valid_playbyplay_games)

        return playbyplay_games_filtered

    async def fetch_all_boxscore_data(self):
        valid_games = await self.fetch_valid_game_urls()
        if not valid_games:
            print("📅 No games scheduled or in progress at the moment.")
            return

        valid_boxscore_games = valid_games[1]

        boxscore_games_filtered = self.filter_valid_games(valid_boxscore_games)

        return boxscore_games_filtered

    def filter_valid_games(self, valid_games):
        valid_games_filtered = [game for game in valid_games if game]

        if not valid_games_filtered:
            print("⚠️ No valid boxscore games found.")
            return

        return [game for game in valid_games_filtered]
