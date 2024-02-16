// init_charts.js

document.addEventListener('DOMContentLoaded', function () {
    // Parse the embedded game data
    const gameData = JSON.parse(document.getElementById('game_data').textContent);

    // Initialize the points chart
    new Chart(document.getElementById('pointsChart'), {
        type: 'line',
        data: {
            labels: gameData.dates,
            datasets: [{
                label: 'Points',
                data: gameData.points,
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        }
    });

    // Initialize other charts (assists, turnovers, ftm, etc.) similarly...
});
