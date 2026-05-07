import Chart from 'chart.js/auto';

// Global Chart Instance
let metricsChartInstance = null;

// Dynamic API URLs based on current host
const host = window.location.hostname;
const apiHost = (host === 'localhost' || host === '127.0.0.1') ? `${host}:8000` : window.location.host;
const API_BASE_URL = `${window.location.protocol}//${apiHost}`;
const WS_BASE_URL = `${window.location.protocol === 'https:' ? 'wss:' : 'ws:'}//${apiHost}`;

document.addEventListener('DOMContentLoaded', () => {
  initHistoricalMetrics();
  
  const form = document.getElementById('configForm');
  form.addEventListener('submit', handleRunBenchmark);
  
  // Attach a global function for Playwright to simulate WS messages easily
  window.appendLog = appendToTerminal;
});

/**
 * Initialize and render the historical metrics chart.
 */
async function initHistoricalMetrics() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/runs`);
    if (!response.ok) throw new Error('Failed to fetch historical runs');
    
    const data = await response.json();
    renderChart(data.runs);
  } catch (err) {
    console.error("Error loading metrics:", err);
  }
}

/**
 * Renders the Chart.js canvas.
 */
function renderChart(runs) {
  const emptyState = document.getElementById('chartEmptyState');
  const canvas = document.getElementById('metricsChart');
  
  if (!runs || runs.length === 0) {
    emptyState.classList.remove('hidden');
    canvas.classList.add('hidden');
    return;
  } else {
    emptyState.classList.add('hidden');
    canvas.classList.remove('hidden');
  }
  
  // Reverse to show chronological order (oldest to newest)
  runs.reverse();
  
  const labels = runs.map(r => new Date(r.run_date).toLocaleTimeString());
  const latencyData = runs.map(r => r.avg_latency_ms);
  const throughputData = runs.map(r => r.avg_tokens_per_sec);

  const ctx = document.getElementById('metricsChart').getContext('2d');
  
  if (metricsChartInstance) {
    metricsChartInstance.destroy();
  }

  // Set default color for Chart.js to match dark mode
  Chart.defaults.color = '#8b949e';
  Chart.defaults.font.family = "'Inter', sans-serif";

  metricsChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Avg Latency (ms)',
          data: latencyData,
          borderColor: '#58a6ff',
          backgroundColor: 'rgba(88, 166, 255, 0.1)',
          yAxisID: 'y',
          fill: true,
          tension: 0.3
        },
        {
          label: 'Tokens/sec',
          data: throughputData,
          borderColor: '#3fb950',
          backgroundColor: 'rgba(63, 185, 80, 0.1)',
          yAxisID: 'y1',
          fill: true,
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      plugins: {
        legend: {
          position: 'top',
        }
      },
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Latency (ms)'
          },
          grid: {
            color: 'rgba(255,255,255,0.05)'
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Tokens/sec'
          },
          grid: {
            drawOnChartArea: false,
          },
        },
        x: {
          grid: {
            color: 'rgba(255,255,255,0.05)'
          }
        }
      }
    }
  });
}

/**
 * Handles the configuration form submission.
 */
async function handleRunBenchmark(event) {
  event.preventDefault();
  
  const runner = document.getElementById('runnerSelect').value;
  const model = document.getElementById('modelInput').value;
  const dataset = document.getElementById('datasetInput').value;
  const btn = document.getElementById('runBtn');
  
  btn.disabled = true;
  btn.textContent = 'Starting...';
  
  try {
    const response = await fetch(`${API_BASE_URL}/api/run`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        runner_type: runner,
        model_name: model,
        dataset_name: dataset,
        max_items: 5,
        hardware_profile: 'Apple Silicon (M-Series)'
      })
    });
    
    if (!response.ok) throw new Error('API Error');
    
    const data = await response.json();
    
    // Update UI Status
    const statusIndicator = document.getElementById('statusIndicator');
    const indicatorDot = document.querySelector('.status-indicator');
    statusIndicator.textContent = `Running Job: ${data.job_id.substring(0,8)}`;
    indicatorDot.classList.add('running');
    
    // Prep Terminal
    document.getElementById('terminalPlaceholder').classList.add('hidden');
    const terminal = document.getElementById('terminal');
    terminal.classList.remove('hidden');
    terminal.innerHTML = `[System] Connected to Orchestrator. Job ID: ${data.job_id}\n`;
    
    // Open WebSocket
    connectLogsWebSocket(data.job_id);
    
  } catch (err) {
    console.error(err);
    alert('Failed to trigger benchmark.');
    btn.disabled = false;
    btn.textContent = 'Run Benchmark';
  }
}

/**
 * Connects to the backend WebSocket for real-time log streaming.
 */
function connectLogsWebSocket(jobId) {
  const ws = new WebSocket(`${WS_BASE_URL}/api/logs/${jobId}`);
  
  ws.onmessage = (event) => {
    appendToTerminal(event.data);
  };
  
  ws.onclose = () => {
    appendToTerminal("\n[System] Connection closed. Run complete.");
    const btn = document.getElementById('runBtn');
    btn.disabled = false;
    btn.textContent = 'Run Benchmark';
    
    const indicatorDot = document.querySelector('.status-indicator');
    indicatorDot.classList.remove('running');
    document.getElementById('statusIndicator').textContent = 'Ready';
    
    // Refresh historical metrics after run
    initHistoricalMetrics();
  };
  
  ws.onerror = (err) => {
    appendToTerminal(`\n[System Error] ${err}`);
  };
}

/**
 * Appends text to the terminal UI and auto-scrolls.
 */
function appendToTerminal(text) {
  const terminal = document.getElementById('terminal');
  // Simple text sanitization to prevent XSS (if logs were malicious)
  const node = document.createTextNode(text);
  terminal.appendChild(node);
  
  // Auto scroll to bottom
  terminal.scrollTop = terminal.scrollHeight;
}
