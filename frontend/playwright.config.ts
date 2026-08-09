import { defineConfig } from '@playwright/test';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { shellTestServer } from './e2e/support/testServer';

const frontendRoot = resolve(__dirname);
const repositoryRoot = resolve(frontendRoot, '..');
const bundledPython = resolve(
  repositoryRoot,
  'tmp',
  'toolchains',
  'f01a',
  'runtimes',
  'python-3.14.6',
  'python.exe',
);
const demoPython = process.env.PROJECTB_PYTHON
  ?? (existsSync(bundledPython) ? bundledPython : process.platform === 'win32' ? 'python' : 'python3');

export default defineConfig({
  testDir: resolve(frontendRoot, 'e2e'),
  fullyParallel: false,
  retries: 0,
  timeout: 15_000,
  expect: { timeout: 5_000 },
  reporter: 'line',
  use: {
    baseURL: 'http://127.0.0.1:4173',
    trace: 'retain-on-failure',
  },
  webServer: [
    { ...shellTestServer, cwd: frontendRoot },
    {
      command: `${JSON.stringify(demoPython)} e2e/support/demo_server.py`,
      cwd: frontendRoot,
      url: 'http://127.0.0.1:7860/api/settings',
      reuseExistingServer: false,
      timeout: 60_000,
      gracefulShutdown: { signal: 'SIGTERM', timeout: 5_000 },
    },
  ],
  projects: [
    { name: 'mobile-360', use: { viewport: { width: 360, height: 800 } } },
    { name: 'tablet-768', use: { viewport: { width: 768, height: 1024 } } },
    { name: 'desktop-1440', use: { viewport: { width: 1440, height: 900 } } },
  ],
});
