let chart;

async function loadChart(includePython) {
  const res = await fetch('/chart-data');
  const chartData = await res.json();

  // Filter datasets based on includePython flag
  const filteredDatasets = includePython
    ? chartData.datasets
    : chartData.datasets.filter(ds => ds.label.toLowerCase() !== 'python');

  const ctx = document.getElementById('myChart').getContext('2d');
  if (chart) chart.destroy();

  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: chartData.labels,
      datasets: filteredDatasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: includePython ? 'All Languages' : 'Languages Without Python'
        },
        legend: {
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Frequency'
          },
          ticks: {
            stepSize: 5
          }
        },
        x: {
          title: {
            display: true,
            text: 'Year'
          }
        }
      }
    }
  });
}

// Load default chart with Python on page load
window.onload = () => loadChart(true);