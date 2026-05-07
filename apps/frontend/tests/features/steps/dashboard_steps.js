import { createBdd } from 'playwright-bdd';
import { expect } from '@playwright/test';

const { Given, When, Then } = createBdd();

Given('the dashboard is loaded', async ({ page }) => {
  await page.addInitScript(() => {
    window.WebSocket = class {
      constructor(url) { this.url = url; }
      send() {}
      close() {}
    };
  });
  await page.route('**/api/runs', async route => {
    await route.fulfill({
      headers: { 'Access-Control-Allow-Origin': '*' },
      json: { runs: [{ id: 1, run_date: "2026-05-07T00:00:00Z", avg_latency_ms: 100, avg_tokens_per_sec: 50 }] }
    });
  });
  await page.goto('/');
  await expect(page.locator('#app')).toBeVisible();
});

Then('I should see the historical metrics chart rendered', async ({ page }) => {
  // Chart.js uses a canvas element
  await expect(page.locator('#metricsChart')).toBeVisible();
});

When('I select the {string} runner', async ({ page }, runner) => {
  await page.locator('#runnerSelect').selectOption(runner);
});

When('I enter the model name {string}', async ({ page }, model) => {
  await page.locator('#modelInput').fill(model);
});

When('I enter the dataset ID {string}', async ({ page }, dataset) => {
  await page.locator('#datasetInput').fill(dataset);
});

When('I click the Run Benchmark button', async ({ page }) => {
  // For the tests, we mock the fetch API so it doesn't actually hit the backend
  await page.route('**/api/run', async route => {
    if (route.request().method() === 'OPTIONS') {
      await route.fulfill({
        status: 200,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type'
        }
      });
    } else {
      await route.fulfill({ 
        json: { job_id: 'test-job-123', status: 'pending' },
        headers: { 'Access-Control-Allow-Origin': '*' }
      });
    }
  });
  await page.locator('#runBtn').click();
});

Then('I should see a status indicating the run has started', async ({ page }) => {
  await expect(page.locator('#statusIndicator')).toContainText('Running');
});

Then('the terminal should become visible', async ({ page }) => {
  await expect(page.locator('#terminal')).toBeVisible();
});

Given('a benchmarking run has been started', async ({ page }) => {
  await page.addInitScript(() => {
    window.WebSocket = class {
      constructor(url) { this.url = url; }
      send() {}
      close() {}
    };
  });
  await page.route('**/api/runs', async route => {
    await route.fulfill({
      headers: { 'Access-Control-Allow-Origin': '*' },
      json: { runs: [{ id: 1, run_date: "2026-05-07T00:00:00Z", avg_latency_ms: 100, avg_tokens_per_sec: 50 }] }
    });
  });
  await page.goto('/');
  await page.route('**/api/run', async route => {
    if (route.request().method() === 'OPTIONS') {
      await route.fulfill({
        status: 200,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type'
        }
      });
    } else {
      await route.fulfill({ 
        json: { job_id: 'ws-job-123', status: 'pending' },
        headers: { 'Access-Control-Allow-Origin': '*' }
      });
    }
  });
  // Note: True websocket mocking in Playwright is complex without external tools.
  // For this UI test, we will assert that the DOM updates when the internal log handler is called.
  await page.locator('#modelInput').fill('dummy');
  await page.locator('#runBtn').click();
});

When('the backend sends log messages via WebSocket', async ({ page }) => {
  // We can simulate a websocket message by evaluating JS to trigger our append function directly
  await page.evaluate(() => {
    window.appendLog("Mock log message from daemon...");
  });
});

Then('the terminal should append the log messages to its output', async ({ page }) => {
  await expect(page.locator('#terminal')).toContainText('Mock log message from daemon...');
});
