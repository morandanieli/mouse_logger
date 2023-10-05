// path_to_dashboard_scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const movementSpeedsData = [];  // Add data here
    const directionalPreferencesData = [];  // Add data here

    function renderClickHeatmap() {
       fetch('http://localhost:5002/nutrition.html')
        .then(response => response.text())
        .then(html => {
            document.querySelector('#clickHeatmap').innerHTML = html;
            fetch('/clickHeatmapData')
            .then(response => response.json())
            .then(data => {
                // Initialize heatmap instance
                var heatmapInstance = h337.create({
                    container: document.getElementById("clickHeatmap"),
                });
                heatmapInstance.setData({
                    max: Math.max(...data.map(d => d.value)),
                    data: data
                });
            })
            .catch(err => console.error('Error fetching heatmap data:', err));
        })
        .catch(error => console.error('Error fetching questionnaire:', error));

    }


    // Function to visualize mouse movement speeds
    function renderMovementSpeeds(data) {
        const ctx = document.getElementById('speedChart').getContext('2d');

        new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    // Call visualization functions with mock data
    renderClickHeatmap();
    renderMovementSpeeds(movementSpeedsData);
});
