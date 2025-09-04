const ctx = document.getElementById('chart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: [],
    datasets: [{
      label: 'Sensor Values',
      data: [],
      borderColor: 'blue',
      borderWidth: 2
    }]
  }
});

async function fetchData() {
  const res = await fetch('/api/data');
  const json = await res.json();
  chart.data.labels = Array.from({ length: json.values.length }, (_, i) => i + 1);
  chart.data.datasets[0].data = json.values;
  chart.update();
}

setInterval(fetchData, 2000);
