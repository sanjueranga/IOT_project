// =======================
// WebSocket connection
// =======================
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
    console.log("WebSocket connected to server");
};

ws.onclose = () => {
    console.log("WebSocket disconnected. Trying to reconnect in 2s...");
    setTimeout(() => location.reload(), 2000); // simple reconnect by page reload
};

ws.onerror = (err) => {
    console.error("WebSocket error:", err);
};

// =======================
// Chart setup
// =======================
const humidityChart = new Chart(document.getElementById('humidityChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Humidity (%)', data: [], borderColor: 'blue', borderWidth: 2 }] },
    options: { responsive: true }
});

const tempChart = new Chart(document.getElementById('tempChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            { label: 'Temp (°C)', data: [], borderColor: 'red', borderWidth: 2 },
            { label: 'Temp (°F)', data: [], borderColor: 'orange', borderWidth: 2 }
        ]
    },
    options: { responsive: true }
});

const passengersChart = new Chart(document.getElementById('passengersChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Passengers', data: [], borderColor: 'green', borderWidth: 2 }] },
    options: { responsive: true }
});

const distanceChart = new Chart(document.getElementById('distanceChart').getContext('2d'), {
    type: 'line',
    data: { labels: [], datasets: [{ label: 'Distance (cm)', data: [], borderColor: 'purple', borderWidth: 2 }] },
    options: { responsive: true }
});

// =======================
// Update live values
// =======================
function updateLiveValues(latest) {
    document.getElementById('humidity').textContent = latest?.humidity ?? '-';
    document.getElementById('temp_c').textContent = latest?.temp_c ?? '-';
    document.getElementById('temp_f').textContent = latest?.temp_f ?? '-';
    document.getElementById('passengers').textContent = latest?.passengers ?? '-';
    document.getElementById('distance').textContent = latest?.distance ?? '-';
    document.getElementById('buzzer').textContent = latest?.buzzer ?? '-';
    document.getElementById('latitude').textContent = latest?.latitude ?? '-';
    document.getElementById('longitude').textContent = latest?.longitude ?? '-';
}

// =======================
// WebSocket message handler
// =======================
ws.onmessage = (event) => {
    const latest = JSON.parse(event.data);

    // Update live values
    updateLiveValues(latest);

    // Update charts
    const currentLength = humidityChart.data.labels.length;
    const nextIndex = currentLength + 1;

    // --- Humidity ---
    humidityChart.data.labels.push(nextIndex);
    humidityChart.data.datasets[0].data.push(latest.humidity);
    if (humidityChart.data.labels.length > 50) {
        humidityChart.data.labels.shift();
        humidityChart.data.datasets[0].data.shift();
    }
    humidityChart.update();

    // --- Temperature ---
    tempChart.data.labels.push(nextIndex);
    tempChart.data.datasets[0].data.push(latest.temp_c);
    tempChart.data.datasets[1].data.push(latest.temp_f);
    if (tempChart.data.labels.length > 50) {
        tempChart.data.labels.shift();
        tempChart.data.datasets[0].data.shift();
        tempChart.data.datasets[1].data.shift();
    }
    tempChart.update();

    // --- Passengers ---
    passengersChart.data.labels.push(nextIndex);
    passengersChart.data.datasets[0].data.push(latest.passengers);
    if (passengersChart.data.labels.length > 50) {
        passengersChart.data.labels.shift();
        passengersChart.data.datasets[0].data.shift();
    }
    passengersChart.update();

    // --- Distance ---
    distanceChart.data.labels.push(nextIndex);
    distanceChart.data.datasets[0].data.push(latest.distance);
    if (distanceChart.data.labels.length > 50) {
        distanceChart.data.labels.shift();
        distanceChart.data.datasets[0].data.shift();
    }
    distanceChart.update();

    // --- Update table ---
    const tableBody = document.querySelector('#dataTable tbody');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${nextIndex}</td>
        <td>${latest.humidity}</td>
        <td>${latest.temp_c}</td>
        <td>${latest.temp_f}</td>
        <td>${latest.distance}</td>
        <td>${latest.buzzer}</td>
        <td>${latest.latitude}</td>
        <td>${latest.longitude}</td>
    `;
    tableBody.appendChild(newRow);
    if (tableBody.rows.length > 10) tableBody.deleteRow(0); // keep last 10 rows
};
