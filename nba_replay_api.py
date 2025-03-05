import requests
import asyncio
from datetime import datetime

API_KEY = "2b42ac7c49504dc08e57bf97e2d672fc"
METADATA = "https://replay.sportsdata.io/api/metadata?key=2b42ac7c49504dc08e57bf97e2d672fc"

response = requests.get(METADATA)


def get_game_ids():
    """
    This function collects all of the games from the metadata
    """
    if response.status_code == 200:
        data = response.json()
        endpoints = data['AvailableEndpoints']

        playbyplay_endpoints = [ep for ep in endpoints if "/playbyplay/" in ep]
        game_ids = [ep.split("/playbyplay/")[-1]
                    for ep in playbyplay_endpoints]

    else:
        print("Error", response.status_code, response.text)

    return [f"https://replay.sportsdata.io/api/v3/nba/pbp/json/playbyplay/{game_id}?key={API_KEY}" for game_id in game_ids]


# Checks if the url actually has a game scheduled an is valid

def get_valid_game_ids():
    game_ids = get_game_ids()
    valid_games = []

    for game_id in game_ids:
        game_response = requests.get(game_id)
        if game_response.status_code == 200:
            valid_games.append(game_response.json())

    return valid_games


def game_progresses():
    valid_games = get_valid_game_ids()
    for game_data in valid_games:
        game_info = game_data['Game']

        status = game_info.get('Status', 'Unknown')
        away_team = game_info.get('AwayTeam', 'Unknown')
        home_team = game_info.get('HomeTeam', 'Unknown')
        away_team_score = game_info.get('AwayTeamScore', 0)
        home_team_score = game_info.get('HomeTeamScore', 0)
        datetime_str = game_info.get('DateTime', '')

        if datetime_str:
            game_datetime = datetime.strptime(
                datetime_str, "%Y-%m-%dT%H:%M:%S")
            game_time = game_datetime.strftime("%B %d, %Y - %I:%M %p")

        if status == 'Scheduled':
            print(
                f"🕒 {away_team} vs {home_team} is scheduled to start at {game_time} EST")
        elif status == "Final":
            print(
                f"✅ Final Score: {away_team} {away_team_score} - {home_team} {home_team_score}")
        else:
            print(
                f"🏀 Game in progress: {away_team} {away_team_score} - {home_team} {home_team_score} ")


game_progresses()
