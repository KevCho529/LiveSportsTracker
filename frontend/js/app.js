async function fetchAllGames() {
  try {
    const response = await fetch('http://127.0.0.1:8000/nba/livescore');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const games = await response.json();
    displayGames(games);
  } catch (error) {
    console.error('Error fetching all games:', error)
  }
}

function displayGames(games) {
  const liveGamesContainer = document.getElementById("live-games")
  const upcomingGamesContainer = document.getElementById("upcoming-games")
  const finalGamesContainer = document.getElementById("final-games")

  liveGamesContainer.innerHTML = ''
  upcomingGamesContainer.innerHTML = ''
  finalGamesContainer.innerHTML = ''

  games.forEach(game => {
    const gameElement = createGameElement(game)
    if (game.status === 'InProgress') {
      liveGamesContainer.appendChild(gameElement)
    } else if (game.status === 'Scheduled') {
      upcomingGamesContainer.appendChild(gameElement)
    } else if (game.status === 'Final') {
      finalGamesContainer.appendChild(gameElement)
    }
  });
}


function createGameElement(game) {
  const gameDiv = document.createElement("div");
  gameDiv.classList.add("game-card");

  let quarter_status = '';
  let secondsFormatted = String(game.seconds_remaining).padStart(2, '0');

  // Assuming `game.quarter` is a string representing the quarter
  if (game.quarter === '1') {
    quarter_status = '1st Quarter';
  } else if (game.quarter === '2') {
    quarter_status = '2nd Quarter';
  } else if (game.quarter === '3') {
    quarter_status = '3rd Quarter';
  } else if (game.quarter === '4') {
    quarter_status = '4th Quarter';
  } else if (game.quarter === 'Half') {
    quarter_status = 'Halftime';
  }

  let content = '';
  if (game.status === 'InProgress') {
    content = `
      <div class="team-section">
          <span class="team-left">${game.away_team}</span>
          <span class="vs">vs</span>
          <span class="team-right">${game.home_team}</span>
        </div>
        <div class="score-section">
          <span class="score">${game.away_team_score} - ${game.home_team_score}</span>
        </div>
        <div class="game-details">
          <span class="quarter">${quarter_status}</span>
          <span class="time-remaining">${game.minutes_remaining}:${secondsFormatted}</span>
        </div>
      </div>
    `;
  } else if (game.status === "Scheduled") {
    content = `
      <div class="team-section">
        <div class="team-left">${game.away_team}</div>
        <div class="vs">@</div>
        <div class="team-right">${game.home_team}</div>
      </div>
      <div class="game-details">
        <div class="game-date">${game.game_day}</div>
        <div class="game-time">${game.game_time}</div>
      </div>
    `;
  } else if (game.status === "Final") {
    content = `
      <div class="team-section">
        <div class="team-left">${game.away_team}</div>
        <div class="vs">vs</div>
        <div class="team-right">${game.home_team}</div>
      </div>
      <div class="game-details">
        <div class="final-score">Final: ${game.away_team_score} : ${game.home_team_score}</div> <!-- Final score below -->
      </div>
    `;
  }

  gameDiv.innerHTML = content
  gameDiv.onclick = function () {
    navigateToGameDetails(game.game_id)
  }
  return gameDiv
}

function navigateToGameDetails(gameID) {
  window.location.href = `game-details.html?game_id=${gameID}`;
}

// setInterval(fetchAllGames, 10000)

window.onload = fetchAllGames;