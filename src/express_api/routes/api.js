// src/express_api/routes/api.js
const express = require('express');
const { Pool } = require('pg');
const axios = require('axios');
const router = express.Router();

// --- DATABASE CONNECTION ---
// Make sure these credentials are correct for your setup
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'startup_dashboard_db',
    password: 'Abhi.data',
    port: 5432,
});

// --- API ENDPOINTS ---

// GET /api/stats-by-state (Modified to use 'count' from your data)
router.get('/stats-by-state', async (req, res) => {
    try {
        const query = `
            SELECT
                state,
                SUM(count) AS startup_count,
                MIN(year) AS earliest_year,
                MAX(year) AS latest_year
            FROM startups
            WHERE state IS NOT NULL
            GROUP BY state
            ORDER BY startup_count DESC;
        `;
        const { rows } = await pool.query(query);
        res.json(rows);
    } catch (err) {
        console.error(err.message);
        res.status(500).send('Server Error');
    }
});

// POST /api/predict (Modified for the regression model)
router.post('/predict', async (req, res) => {
    try {
        // The ML service runs on port 5001
        const mlServiceUrl = 'http://localhost:5001/predict';

        // Forward the request body to the Python Flask service
        const response = await axios.post(mlServiceUrl, req.body);

        // Return the prediction from the ML service to the frontend
        res.json(response.data);
    } catch (error) {
        console.error('Error calling ML service:', error.message);
        res.status(500).json({ error: 'Failed to get prediction' });
    }
});

module.exports = router;