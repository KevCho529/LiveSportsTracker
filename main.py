from game_tracker import GameTracker
from nba_tracker import NBATracker
from nhl_tracker import NHLTracker
from nfl_tracker import NFLTracker
import asyncio
# from fastapi import FastAPI
# from fastapi.middleware.gzip import GZipMiddleware

# app = FastAPI()
# app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

NBA_API_KEY = "f952554550e44ff68a11159411221257"
NHL_API_KEY = "be02dda670b84cbf9563238020b9d2c5"
NFL_API_KEY = "4d54a2ea71454ef09c08a4fcdcdcd850"

nba = NBATracker(NBA_API_KEY)
nfl = NFLTracker(NFL_API_KEY)
nhl = NHLTracker(NHL_API_KEY)


async def run_all_leagues():
    await asyncio.gather(
        nba.game_progresses(),
        nfl.game_progresses(),
        nhl.game_progresses()
    )


# @app.get("/")
# async def fetch(limit):
#     return {"message": "LiveSportsTracker"}


# @app.get("/nba")
# async def fetch_NBA_games():
#     return await nba.fetch_valid_game_urls()


# @app.get("/nfl")
# async def fetch_NFL_games():
#     return await nfl.fetch_valid_game_urls()


# @app.get("/nhl")
# async def fetch_NHL_games():
#     return await nhl.fetch_valid_game_urls()

if __name__ == "__main__":
    asyncio.run(run_all_leagues())
