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

function updateLiveValues(latest) {
  document.getElementById('humidity').textContent = latest?.humidity ?? '-';
  document.getElementById('temp_c').textContent = latest?.temp_c ?? '-';
  document.getElementById('temp_f').textContent = latest?.temp_f ?? '-';
  document.getElementById('passengers').textContent = latest?.passengers ?? '-';
  document.getElementById('distance').textContent = latest?.distance ?? '-';
  document.getElementById('buzzer').textContent = latest?.buzzer ?? '-';
}

async function fetchData() {
  const res = await fetch('/api/data');
  const json = await res.json();
  const values = json.values || [];
  const labels = values.map((_, i) => i + 1);

  // Prepare data arrays
  const humidity = values.map(v => v.humidity);
  const temp_c = values.map(v => v.temp_c);
  const temp_f = values.map(v => v.temp_f);
  const passengers = values.map(v => v.passengers);
  const distance = values.map(v => v.distance);

  // Update charts
  humidityChart.data.labels = labels;
  humidityChart.data.datasets[0].data = humidity;
  humidityChart.update();

  tempChart.data.labels = labels;
  tempChart.data.datasets[0].data = temp_c;
  tempChart.data.datasets[1].data = temp_f;
  tempChart.update();

  passengersChart.data.labels = labels;
  passengersChart.data.datasets[0].data = passengers;
  passengersChart.update();

  distanceChart.data.labels = labels;
  distanceChart.data.datasets[0].data = distance;
  distanceChart.update();

  // Update live values
  updateLiveValues(values[values.length - 1]);

  // Update table with latest 10 readings
  const tableBody = document.querySelector('#dataTable tbody');
  tableBody.innerHTML = '';
  const last10 = values.slice(-10);
  last10.forEach((row, idx) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${values.length - last10.length + idx + 1}</td>
      <td>${row.humidity}</td>
      <td>${row.temp_c}</td>
      <td>${row.temp_f}</td>
      <td>${row.distance}</td>
      <td>${row.buzzer}</td>
    `;
    tableBody.appendChild(tr);
  });
}

setInterval(fetchData, 2000);
fetchData();
