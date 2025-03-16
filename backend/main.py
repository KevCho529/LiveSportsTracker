from backend.trackers.game_tracker import GameTracker
from backend.trackers.nba_tracker import NBATracker
from backend.trackers.nhl_tracker import NHLTracker
from backend.trackers.nfl_tracker import NFLTracker
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

origins = [
    "http://127.0.0.1:5500",  # Your frontend URL
    "http://localhost:5500",   # Another common local URL for your frontend
]

# Add CORS middleware to allow the frontend to make requests to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specific origins
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],    # Allows all headers
)

NBA_API_KEY = "981418134aae41f1b4933d045d3595d3"
NFL_API_KEY = "2891f655220d43498b23a867ae8606b7"
NHL_API_KEY = "794239259de34523bd2187fe612a09d3"


nba = NBATracker(NBA_API_KEY)
nfl = NFLTracker(NFL_API_KEY)
nhl = NHLTracker(NHL_API_KEY)


# async def run_all_leagues():
#     await asyncio.gather(
#         nba.game_data(),
#         nfl.game_progresses(),
#         nhl.game_progresses()
#     )


@app.get("/")
async def fetch():
    return {"message": "LiveSportsTracker"}


@app.get("/nba/livescore")
async def fetch_nba_live_scores():
    return await nba.get_live_scores()


@app.get("/nba/lastplay")
async def fetch_nba_last_play():
    return await nba.get_last_play()


@app.get("/nba/quarterscores")
async def fetch_nba_quarter_scores():
    return await nba.get_quarter_scores()


@app.get("/nba/teamstats")
async def fetch_nba_team_stats():
    return await nba.get_team_stats()


@app.get("/nba/playerstats")
async def fetch_nba_team_stats():
    return await nba.get_player_stats()


# if __name__ == "__main__":
#     asyncio.run(run_all_leagues())
