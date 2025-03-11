from game_tracker import GameTracker
from nba_tracker import NBATracker
from nhl_tracker import NHLTracker
from nfl_tracker import NFLTracker
import asyncio


NBA_API_KEY = "f952554550e44ff68a11159411221257"
NHL_API_KEY = "be02dda670b84cbf9563238020b9d2c5"
NFL_API_KEY = "4d54a2ea71454ef09c08a4fcdcdcd850"


def run_all_leagues():
    nba = NBATracker(NBA_API_KEY)
    nfl = NFLTracker(NFL_API_KEY)
    nhl = NHLTracker(NHL_API_KEY)

    asyncio.run(
        nba.game_progresses()
    )
    asyncio.run(
        nfl.game_progresses()
    )
    asyncio.run(
        nhl.game_progresses()
    )


if __name__ == "__main__":
    run_all_leagues()
