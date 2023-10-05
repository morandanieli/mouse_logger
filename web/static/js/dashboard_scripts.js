// path_to_dashboard_scripts.js

document.addEventListener("DOMContentLoaded", function() {
    const movementSpeedsData = [];  // Add data here
    const directionalPreferencesData = [];  // Add data here

    function renderClickHeatmap() {
        fetch('/clickHeatmapData')
        .then(response => response.json())
        .then(data => {
            // Initialize heatmap instance
            var heatmapInstance = h337.create({
                container: document.getElementById("clickHeatmap"),
                radius: 10
            });
            console.log(data);
            heatmapInstance.setData({
                max: Math.max(...data.map(d => d.value)),
                data: data
            });
        })
        .catch(err => console.error('Error fetching heatmap data:', err));
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
