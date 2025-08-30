// This event listener ensures the script runs after the HTML document is fully loaded.
document.addEventListener('DOMContentLoaded', () => {
    // --- CONFIGURATION ---
    const API_BASE_URL = 'http://localhost:5000/api';

    // --- DOM ELEMENT REFERENCES ---
    const chartDiv = document.getElementById('fundingChart');
    const predictionForm = document.getElementById('prediction-form');
    const predictionResultDiv = document.getElementById('prediction-result');

    // --- FUNCTION TO RENDER THE BAR CHART ---
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

        Plotly.newPlot(chartDiv, plotData, layout);
    };

    // --- FUNCTION TO FETCH INITIAL DATA FOR THE CHART ---
    const fetchDashboardData = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/stats-by-state`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            renderStartupChart(data);
        } catch (error) {
            console.error('Failed to fetch dashboard data:', error);
            chartDiv.innerHTML = '<p style="color: red;">Error loading chart data. Is the Express server running?</p>';
        }
    };

    // --- FUNCTION TO HANDLE THE PREDICTION FORM SUBMISSION ---
    const handlePrediction = async (event) => {
        // Prevent the browser from reloading the page
        event.preventDefault();

        predictionResultDiv.textContent = 'Predicting...';
        predictionResultDiv.style.color = '#333';

        // This object creates the JSON payload.
        // The keys ('year', 'state', 'industry') MUST exactly match what the ML model was trained on.
        const formData = {
            year: parseInt(document.getElementById('founding_year').value),
            state: document.getElementById('state').value,
            industry: document.getElementById('sector').value
        };

        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (result.predicted_count !== undefined) {
                const count = Math.round(result.predicted_count);
                predictionResultDiv.textContent = `Predicted Startup Count: ${count}`;
                predictionResultDiv.style.color = 'green';
            } else {
                throw new Error(result.error || 'Prediction failed.');
            }

        } catch (error) {
            console.error('Prediction request failed:', error);
            predictionResultDiv.textContent = 'Error making prediction.';
            predictionResultDiv.style.color = 'red';
        }
    };

    // --- INITIALIZE THE DASHBOARD ---
    // Fetch data for the chart when the page loads.
    fetchDashboardData();
    // Listen for the form to be submitted.
    predictionForm.addEventListener('submit', handlePrediction);
});