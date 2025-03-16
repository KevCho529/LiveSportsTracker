// async function fetchAndDisplayData() {
//   try {
//     const [quarterscores, lastplay, playerstats] = await Promise.all([
//       fetchQuarterStats(),
//       fetchLastPlay(),
//       fetchPlayerStats()
//     ])

//     displayQuarters(quarterscores)
//     displayLastPlay(lastplay)
//     displayPlayerStats(playerstats)
//   } catch (error) {
//     console.error('Error fetching or displaying data:', error)
//   }
// }

async function fetchQuarterStats() {
  try {
    const response = await fetch('http://127.0.0.1:8000/nba/quarterscores')
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const quarterscores = await response.json()
    console.log(quarterscores)
    displayQuarters(quarterscores)
  } catch (error) {
    console.error('Error fetching all games:', error)
  }
}

// async function fetchLastPlay() {
//   try {
//     const response = await fetch('http://127.0.0.1:8000/nba/lastplay')
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
//     const lastplay = await response.json()
//     displayLastPlay(lastplay)
//   } catch (error) {
//     console.error('Error fetching all games:', error)
//   }
// }

// async function fetchPlayerStats() {
//   try {
//     const response = await fetch('http://127.0.0.1:8000/nba/playerstats')
//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`);
//     }
//     const playerstats = await response.json()
//     displayPlayerStats(playerstats)
//   } catch (error) {
//     console.error('Error fetching all games:', error)
//   }
// }

function displayQuarters(quarterscores) {
  const scoreSummaryContainer = document.getElementById("score-summary")

  scoreSummaryContainer.innerHTML = ''

  const quarterElement = createQuarterElement(quarterscores)
  scoreSummaryContainer.appendChild(quarterElement)
}

function createQuarterElement(games) {
  const urlParams = new URLSearchParams(window.location.search);

  // Extract the game_id from the URL
  const gameID = urlParams.get("game_id");
  const gameData = games.find(game => game.game_id === Number(gameID))
  if (!gameData) {
    console.error('No data found for game ID:', gameID);
    const errorMessage = document.createElement("p");
    errorMessage.textContent = `No data found for game ID: ${gameID}`;
    return errorMessage;
  }

  const quarterDiv = document.createElement("table");
  const quarterData = gameData.quarters
  console.log(quarterData)

  away_team = gameData.away_team
  away_Q1_score = quarterData[0].AwayScore;
  away_Q2_score = quarterData[1].AwayScore;
  away_Q3_score = quarterData[2].AwayScore;
  away_Q4_score = quarterData[3].AwayScore;
  away_score_total = away_Q1_score + away_Q2_score + away_Q3_score + away_Q4_score


  home_team = gameData.home_team
  home_Q1_score = quarterData[0].HomeScore;
  home_Q2_score = quarterData[1].HomeScore;
  home_Q3_score = quarterData[2].HomeScore;
  home_Q4_score = quarterData[3].HomeScore;
  home_score_total = home_Q1_score + home_Q2_score + home_Q3_score + home_Q4_score

  let content = ''

  content = `
  <thead>
    <tr>
      <th>Team</th>
      <th>Q1</th>
      <th>Q2</th>
      <th>Q3</th>
      <th>Q4</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody id="score-details">
    <tr>
      <td>${away_team}</td>
      <td>${away_Q1_score}</td>
      <td>${away_Q2_score}</td>
      <td>${away_Q3_score}</td>
      <td>${away_Q4_score}</td>
      <td>${away_score_total}</td>
    </tr>
    <tr>
      <td>${home_team}</td>
      <td>${home_Q1_score}</td>
      <td>${home_Q2_score}</td>
      <td>${home_Q3_score}</td>
      <td>${home_Q4_score}</td>
      <td>${home_score_total}</td>
    </tr>
  </tbody>
  `;

  quarterDiv.innerHTML = content
  return quarterDiv
}

// function displayLastPlay(lastplay) {
//   const lastPlay = document.getElementById("last-play")

//   const urlParams = new URLSearchParams(window.location.search);
//   const gameID = urlParams.get("game_id");

//   lastplay.forEach(game => {
//     if (game.game_id === Number(gameID)) {
//       const lastPlayElement = createLastPlayElement(game)
//       lastPlay.appendChild(lastPlayElement)
//     }

//   })
// }

// function createLastPlayElement(game) {
//   const lastPlayDiv = document.createElement("div")

//   let content = ''
//   content = `
//   <p id="last-play-text">${game.last_play || "No last play data available"}</p>
//   `;

//   lastPlayDiv.innerHTML = content;
//   return lastPlayDiv;
// }

// function displayPlayerStats(playerstats) {
//   const awayPlayerStatsContainer = document.getElementById("away-team-box")
//   const homePlayerStatsContainer = document.getElementById("home-team-box")
//   const urlParams = new URLSearchParams(window.location.search);
//   const gameID = urlParams.get("game_id");

//   playerstats.forEach(game => {
//     if (game.game_id == Number(gameID)) {
//       const { awayPlayerStatsTable, homePlayerStatsTable } = createPlayerStatsElement(game)
//       awayPlayerStatsContainer.appendChild(awayPlayerStatsTable)
//       homePlayerStatsContainer.appendChild(homePlayerStatsTable)
//     }
//   })

// }

// function createPlayerStatsElement(game) {
//   const homePlayerStatsTable = document.createElement("table")
//   const awayPlayerStatsTable = document.createElement("table")
//   homePlayerStatsTable.classList.add("player-table")
//   awayPlayerStatsTable.classList.add("player-table")

//   let away_content = `
//       <tr>
//         <th>Player</th>
//         <th>PTS</th>
//         <th>REB</th>
//         <th>AST</th>
//       </tr>
//   `

//   let home_content = `
//       <tr>
//         <th>Player</th>
//         <th>PTS</th>
//         <th>REB</th>
//         <th>AST</th>
//       </tr>
//   `

//   game.forEach(player => {
//     let player_points = (player.two_pointers_made * 2) + (player.three_pointers_made * 3) + player.free_throws_made
//     if (player.home_or_away === "HOME") {

//       home_content += `
//           <tr>
//             <td>${player.name}</td>
//             <td>${player_points}</td>
//             <td>${player.rebounds}</td>
//             <td>${player.assists}</td>
//           </tr>
//       `
//     } else if (player.home_or_away === "AWAY") {
//       player_points = (player.two_pointers_made * 2) + (player.three_pointers_made * 3) + player.free_throws_made
//       away_content += `
//           <tr>
//             <td>${player.name}</td>
//             <td>${player_points}</td>
//             <td>${player.rebounds}</td>
//             <td>${player.assists}</td>
//           </tr>
//       `
//     }
//   })

//   homePlayerStatsTable.innerHTML = home_content
//   awayPlayerStatsTable.innerHTML = away_content

//   return { awayPlayerStatsTable, homePlayerStatsTable }

// }


window.onload = fetchQuarterStats;
