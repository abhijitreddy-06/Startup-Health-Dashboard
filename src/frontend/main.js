document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://localhost:5000/api';

    const chartDiv = document.getElementById('fundingChart');
    const predictionForm = document.getElementById('prediction-form');
    const predictionResultDiv = document.getElementById('prediction-result');

    const renderStartupChart = (data) => {
        const states = data.map(d => d.state);
        const startupCounts = data.map(d => d.startup_count);

        const plotData = [{
            x: states,
            y: startupCounts,
            type: 'bar',
            marker: { color: '#2563eb' }
        }];

        const layout = {
            title: 'Total Number of Startups by State',
            xaxis: { title: 'State' },
            yaxis: { title: 'Number of Startups' }
        };

        // The {responsive: true} config helps Plotly adapt
        Plotly.newPlot(chartDiv, plotData, layout, { responsive: true });
    };

    const fetchDashboardData = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats-by-state`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            renderStartupChart(data);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
            chartDiv.innerHTML = '<p style="color: red;">Error loading chart data. Is the Express server running?</p>';
        }
    };

    const handlePrediction = async (event) => {
        event.preventDefault();

        predictionResultDiv.textContent = 'Predicting...';
        predictionResultDiv.style.color = '#333';
        predictionResultDiv.style.background = 'transparent';

        const formData = {
            year: parseInt(document.getElementById('year').value),
            state: document.getElementById('state').value,
            industry: document.getElementById('sector').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

            const result = await response.json();

            if (result.predicted_count !== undefined) {
                const count = Math.round(result.predicted_count);
                predictionResultDiv.textContent = `Predicted Startup Count: ${count}`;
                predictionResultDiv.style.color = '#155724'; // Dark green
                predictionResultDiv.style.backgroundColor = '#d4edda'; // Light green
            } else {
                throw new Error(result.error || 'Prediction failed.');
            }

        } catch (error) {
            console.error('Prediction request failed:', error);
            predictionResultDiv.textContent = 'Error making prediction.';
            predictionResultDiv.style.color = '#721c24'; // Dark red
            predictionResultDiv.style.backgroundColor = '#f8d7da'; // Light red
        }
    };

    // --- INITIALIZE ---
    fetchDashboardData();
    predictionForm.addEventListener('submit', handlePrediction);

    // --- RESPONSIVENESS ---
    // Make the Plotly chart resize when the window size changes.
    // This is a fallback in case the {responsive: true} config isn't enough.
    window.addEventListener('resize', () => {
        Plotly.Plots.resize(chartDiv);
    });
});