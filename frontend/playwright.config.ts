import { defineConfig } from '@playwright/test';
import { resolve } from 'node:path';
import { shellTestServer } from './e2e/support/testServer';

const frontendRoot = resolve(__dirname);

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
  webServer: { ...shellTestServer, cwd: frontendRoot },
  projects: [
    { name: 'mobile-360', use: { viewport: { width: 360, height: 800 } } },
    { name: 'tablet-768', use: { viewport: { width: 768, height: 1024 } } },
    { name: 'desktop-1440', use: { viewport: { width: 1440, height: 900 } } },
  ],
});
