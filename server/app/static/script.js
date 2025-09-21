// =======================
// Performance Optimizations & DOM Update Throttling
// =======================

// Global variables for location tracking
let currentLatitude = null;
let currentLongitude = null;

// Performance optimization variables
let pendingUpdate = false;
let latestData = null;
let updateQueue = [];
const MAX_CHART_POINTS = 30; // Reduced from 50 for better performance
const MAX_TABLE_ROWS = 8;    // Reduced from 10 for better performance
const UPDATE_THROTTLE_MS = 100; // Minimum time between DOM updates

// Throttled update using requestAnimationFrame
function throttledDOMUpdate() {
    if (pendingUpdate || !latestData) return;

    pendingUpdate = true;
    requestAnimationFrame(() => {
        try {
            updateLiveValues(latestData);
            updateChartsOptimized(latestData);
            updateTableOptimized(latestData);
        } catch (error) {
            console.error('Error during DOM update:', error);
        } finally {
            pendingUpdate = false;
            latestData = null;
        }
    });
}

// Batch DOM updates with debouncing
let updateTimeout = null;
function scheduleUpdate(data) {
    latestData = data; // Always keep the latest data

    if (updateTimeout) {
        clearTimeout(updateTimeout);
    }

    updateTimeout = setTimeout(() => {
        throttledDOMUpdate();
        updateTimeout = null;
    }, UPDATE_THROTTLE_MS);
}

// =======================
// Function definitions (moved to top to ensure availability)
// =======================

// Function to locate the bus with current GPS coordinates
function locateBus() {
    console.log('Locate Bus button clicked!');
    console.log('Current coordinates:', currentLatitude, currentLongitude);

    // For testing - always navigate to map page
    // Get the latest coordinates from the display or use default
    let lat = currentLatitude;
    let lng = currentLongitude;

    // If no coordinates, try to get from the display elements
    if (!lat || !lng) {
        const latElement = document.getElementById('latitude');
        const lngElement = document.getElementById('longitude');

        if (latElement && lngElement) {
            lat = parseFloat(latElement.textContent) || null;
            lng = parseFloat(lngElement.textContent) || null;
        }
    }

    // Store coordinates (even if null, the map page will handle it)
    localStorage.setItem('busLatitude', lat || '7.259723'); // Default to Kandy if no GPS
    localStorage.setItem('busLongitude', lng || '80.599636');
    localStorage.setItem('lastUpdate', new Date().toLocaleString());

    // Always navigate to show the map
    console.log('Navigating to bus_location.html...');
    window.location.href = '/static/bus_location.html';
}

// Test function to verify JavaScript is working
function testButton() {
    alert('JavaScript is working! Current coordinates: ' + currentLatitude + ', ' + currentLongitude);
    console.log('Test button clicked');
}

// Update WebSocket status display
function updateWSStatus(status) {
    const statusElement = document.getElementById('wsStatus');
    if (statusElement) {
        statusElement.textContent = status;
        statusElement.style.color = status === 'Connected' ? 'green' : 'red';
    }
}

// Update location status based on GPS availability
function updateLocationStatus() {
    const statusElement = document.getElementById('locationStatus');
    if (statusElement) {
        if (currentLatitude && currentLongitude) {
            statusElement.textContent = `GPS: ${currentLatitude}, ${currentLongitude}`;
            statusElement.style.color = 'green';
        } else {
            statusElement.textContent = 'GPS: No signal';
            statusElement.style.color = 'red';
        }
    }
}

// =======================
// WebSocket connection with exponential backoff
// =======================
let reconnectAttempts = 0;
const MAX_RECONNECT_DELAY = 30000; // 30 seconds max
const BASE_RECONNECT_DELAY = 1000;  // 1 second base

function connectWebSocket() {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => {
        console.log("WebSocket connected to server");
        updateWSStatus("Connected");
        reconnectAttempts = 0; // Reset on successful connection
    };

    ws.onclose = () => {
        console.log("WebSocket disconnected. Attempting to reconnect...");
        updateWSStatus("Disconnected");

        // Exponential backoff with jitter
        const delay = Math.min(
            BASE_RECONNECT_DELAY * Math.pow(2, reconnectAttempts),
            MAX_RECONNECT_DELAY
        );
        const jitter = Math.random() * 1000; // Add up to 1s jitter

        reconnectAttempts++;
        console.log(`Reconnect attempt ${reconnectAttempts} in ${(delay + jitter) / 1000}s`);

        setTimeout(() => {
            connectWebSocket();
        }, delay + jitter);
    };

    ws.onerror = (err) => {
        console.error("WebSocket error:", err);
        updateWSStatus("Error");
    };

    ws.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            scheduleUpdate(data); // Use throttled update instead of immediate
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    };

    return ws;
}

// Initialize WebSocket connection
const ws = connectWebSocket();

// =======================
// Optimized Chart setup with reduced animation
// =======================
const chartOptions = {
    responsive: true,
    animation: {
        duration: 0 // Disable animations for performance
    },
    interaction: {
        intersect: false,
        mode: 'index'
    },
    scales: {
        x: {
            display: false // Hide x-axis labels for performance
        }
    },
    plugins: {
        legend: {
            display: true
        }
    }
};

const humidityChart = new Chart(document.getElementById('humidityChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Humidity (%)', data: [], borderColor: 'blue', borderWidth: 2, fill: false }] },
    options: chartOptions
});

const tempChart = new Chart(document.getElementById('tempChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Temp (°C)', data: [], borderColor: 'red', borderWidth: 2, fill: false },
            { label: 'Temp (°F)', data: [], borderColor: 'orange', borderWidth: 2, fill: false }
        ]
    },
    options: chartOptions
});

const passengersChart = new Chart(document.getElementById('passengersChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Passengers', data: [], borderColor: 'green', borderWidth: 2, fill: false }] },
    options: chartOptions
});

const distanceChart = new Chart(document.getElementById('distanceChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Distance (cm)', data: [], borderColor: 'purple', borderWidth: 2, fill: false }] },
    options: chartOptions
});

// =======================
// Optimized Update Functions
// =======================
let chartDataIndex = 0;

function updateLiveValues(latest) {
    // Batch DOM reads/writes to minimize reflow
    const elements = {
        humidity: document.getElementById('humidity'),
        temp_c: document.getElementById('temp_c'),
        temp_f: document.getElementById('temp_f'),
        passengers: document.getElementById('passengers'),
        distance: document.getElementById('distance'),
        buzzer: document.getElementById('buzzer'),
        latitude: document.getElementById('latitude'),
        longitude: document.getElementById('longitude')
    };

    // Update all elements in one pass
    elements.humidity.textContent = latest?.humidity ?? '-';
    elements.temp_c.textContent = latest?.temp_c ?? '-';
    elements.temp_f.textContent = latest?.temp_f ?? '-';
    elements.passengers.textContent = latest?.passengers ?? '-';
    elements.distance.textContent = latest?.distance ?? '-';
    elements.buzzer.textContent = latest?.buzzer ?? '-';
    elements.latitude.textContent = latest?.latitude ?? '-';
    elements.longitude.textContent = latest?.longitude ?? '-';

    // Store current GPS coordinates
    if (latest?.latitude && latest?.longitude) {
        currentLatitude = latest.latitude;
        currentLongitude = latest.longitude;
        updateLocationStatus();
    }
}

function updateChartsOptimized(latest) {
    chartDataIndex++;

    // Humidity Chart
    humidityChart.data.labels.push(chartDataIndex);
    humidityChart.data.datasets[0].data.push(latest.humidity);
    if (humidityChart.data.labels.length > MAX_CHART_POINTS) {
        humidityChart.data.labels.shift();
        humidityChart.data.datasets[0].data.shift();
    }

    // Temperature Chart
    tempChart.data.labels.push(chartDataIndex);
    tempChart.data.datasets[0].data.push(latest.temp_c);
    tempChart.data.datasets[1].data.push(latest.temp_f);
    if (tempChart.data.labels.length > MAX_CHART_POINTS) {
        tempChart.data.labels.shift();
        tempChart.data.datasets[0].data.shift();
        tempChart.data.datasets[1].data.shift();
    }

    // Passengers Chart
    passengersChart.data.labels.push(chartDataIndex);
    passengersChart.data.datasets[0].data.push(latest.passengers);
    if (passengersChart.data.labels.length > MAX_CHART_POINTS) {
        passengersChart.data.labels.shift();
        passengersChart.data.datasets[0].data.shift();
    }

    // Distance Chart
    distanceChart.data.labels.push(chartDataIndex);
    distanceChart.data.datasets[0].data.push(latest.distance);
    if (distanceChart.data.labels.length > MAX_CHART_POINTS) {
        distanceChart.data.labels.shift();
        distanceChart.data.datasets[0].data.shift();
    }

    // Update all charts efficiently (batch the updates)
    Promise.resolve().then(() => {
        humidityChart.update('none'); // 'none' mode = no animation
        tempChart.update('none');
        passengersChart.update('none');
        distanceChart.update('none');
    });
}

function updateTableOptimized(latest) {
    const tableBody = document.querySelector('#dataTable tbody');
    if (!tableBody) return;

    // Create new row efficiently
    const newRow = tableBody.insertRow(0); // Insert at top
    newRow.innerHTML = `
        <td>${chartDataIndex}</td>
        <td>${latest.humidity}</td>
        <td>${latest.temp_c}</td>
        <td>${latest.temp_f}</td>
        <td>${latest.distance}</td>
        <td>${latest.buzzer}</td>
        <td>${latest.latitude}</td>
        <td>${latest.longitude}</td>
    `;

    // Remove excess rows efficiently
    while (tableBody.rows.length > MAX_TABLE_ROWS) {
        tableBody.deleteRow(tableBody.rows.length - 1);
    }
}
