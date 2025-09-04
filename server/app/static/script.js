// Chart.js chart setup for each sensor field

const humidityChart = new Chart(document.getElementById('humidityChart').getContext('2d'), {
  type: 'line',
  data: { labels: [], datasets: [{ label: 'Humidity (%)', data: [], borderColor: 'blue', borderWidth: 2 }] },
  options: { responsive: true }
});
const tempChart = new Chart(document.getElementById('tempChart').getContext('2d'), {
  type: 'line',
  data: {
    labels: [], datasets: [
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

// --- Step 4: WebSocket connection ---
const ws = new WebSocket("ws://localhost:8000/ws");

ws.onopen = () => {
    console.log("WebSocket connected");
    document.getElementById("wsStatus").textContent = "Connected";
};

ws.onmessage = (event) => {
    const latest = JSON.parse(event.data);
    console.log("Real-time data received:", latest);

    // Update live values
    updateLiveValues(latest);

    // Update charts
    const currentLength = humidityChart.data.labels.length;
    const nextIndex = currentLength + 1;

    // Humidity chart
    humidityChart.data.labels.push(nextIndex);
    humidityChart.data.datasets[0].data.push(latest.humidity);
    if (humidityChart.data.labels.length > 50) {  // keep last 50 points
        humidityChart.data.labels.shift();
        humidityChart.data.datasets[0].data.shift();
    }
    humidityChart.update();

    // Temperature chart
    tempChart.data.labels.push(nextIndex);
    tempChart.data.datasets[0].data.push(latest.temp_c);
    tempChart.data.datasets[1].data.push(latest.temp_f);
    if (tempChart.data.labels.length > 50) {
        tempChart.data.labels.shift();
        tempChart.data.datasets[0].data.shift();
        tempChart.data.datasets[1].data.shift();
    }
    tempChart.update();

    // Passengers chart
    passengersChart.data.labels.push(nextIndex);
    passengersChart.data.datasets[0].data.push(latest.passengers);
    if (passengersChart.data.labels.length > 50) {
        passengersChart.data.labels.shift();
        passengersChart.data.datasets[0].data.shift();
    }
    passengersChart.update();

    // Distance chart
    distanceChart.data.labels.push(nextIndex);
    distanceChart.data.datasets[0].data.push(latest.distance);
    if (distanceChart.data.labels.length > 50) {
        distanceChart.data.labels.shift();
        distanceChart.data.datasets[0].data.shift();
    }
    distanceChart.update();

    // Update table (last 10 readings)
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
    if (tableBody.rows.length > 10) tableBody.deleteRow(0);
};

ws.onclose = () => {
    document.getElementById("wsStatus").textContent = "Disconnected";
};

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

// async function fetchData() {
//   const res = await fetch('/api/data');
//   const json = await res.json();
//   const values = json.values || [];
//   const labels = values.map((_, i) => i + 1);

//   // Prepare data arrays
//   const humidity = values.map(v => v.humidity);
//   const temp_c = values.map(v => v.temp_c);
//   const temp_f = values.map(v => v.temp_f);
//   const passengers = values.map(v => v.passengers);
//   const distance = values.map(v => v.distance);

//   // Update charts
//   humidityChart.data.labels = labels;
//   humidityChart.data.datasets[0].data = humidity;
//   humidityChart.update();

//   tempChart.data.labels = labels;
//   tempChart.data.datasets[0].data = temp_c;
//   tempChart.data.datasets[1].data = temp_f;
//   tempChart.update();

//   passengersChart.data.labels = labels;
//   passengersChart.data.datasets[0].data = passengers;
//   passengersChart.update();

//   distanceChart.data.labels = labels;
//   distanceChart.data.datasets[0].data = distance;
//   distanceChart.update();

//   // Update live values
//   updateLiveValues(values[values.length - 1]);

//   // Update table with latest 10 readings
//   const tableBody = document.querySelector('#dataTable tbody');
//   tableBody.innerHTML = '';
//   const last10 = values.slice(-10);
//   last10.forEach((row, idx) => {
//     const tr = document.createElement('tr');
//     tr.innerHTML = `
//       <td>${values.length - last10.length + idx + 1}</td>
//       <td>${row.humidity}</td>
//       <td>${row.temp_c}</td>
//       <td>${row.temp_f}</td>
//       <td>${row.distance}</td>
//       <td>${row.buzzer}</td>
//       <td>${row.latitude}</td>
//       <td>${row.longitude}</td>
//     `;
//     tableBody.appendChild(tr);
//   });
// }

// setInterval(fetchData, 2000);
// fetchData();