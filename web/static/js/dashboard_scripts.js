// path_to_dashboard_scripts.js

document.addEventListener("DOMContentLoaded", function() {

    // Mock Data for Visualization (In a real-world scenario, this would be fetched from your data source or server)
    const clickHeatmapData = [];  // Add data here
    const movementSpeedsData = [];  // Add data here
    const directionalPreferencesData = [];  // Add data here

    function renderClickHeatmap(data) {
        const container = document.getElementById("clickHeatmap");

        // Create a heatmap instance
        const heatmap = heatmapjs.create({
            container: container,
            radius: 10
        });

        heatmap.setData(data);
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
    renderClickHeatmap(clickHeatmapData);
    renderMovementSpeeds(movementSpeedsData);
});
