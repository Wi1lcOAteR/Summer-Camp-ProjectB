import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('settings keeps credential private across keyboard and responsive flows', async ({ page }) => {
  let configured = false;
  const mutationHeaders: string[] = [];
  await page.route('**/api/session', async (route) => {
    await route.fulfill({ status: 200, headers: { 'x-csrf-token': 'test-token' }, json: {} });
  });
  await page.route('**/api/settings', async (route) => {
    await route.fulfill({ json: { profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: configured } });
  });
  await page.route('**/api/credentials/provider', async (route) => {
    const method = route.request().method();
    if (method !== 'GET') mutationHeaders.push(route.request().headers()['x-csrf-token'] ?? '');
    if (method === 'PUT') configured = true;
    if (method === 'DELETE') configured = false;
    await route.fulfill({ json: { configured, updated_at: configured ? '2026-08-08T00:00:00Z' : null } });
  });

  await page.goto('/settings');
  await expect(page.getByRole('heading', { name: /settings/i })).toBeVisible();
  await expect(page.getByLabel(/provider api key/i)).toHaveAttribute('type', 'password');
  await expect(page.getByRole('heading', { name: 'Privacy' })).toBeVisible();
  await expect(page.getByRole('heading', { name: 'Delete local data' })).toBeVisible();
  await page.getByLabel(/provider api key/i).fill('sk-live-secret');
  await page.getByRole('button', { name: /save provider credential/i }).press('Enter');
  await expect(page.getByText(/status: configured/i)).toBeVisible();
  await expect(page.locator('body')).not.toContainText('sk-live-secret');
  await page.getByRole('button', { name: /clear stored credential/i }).press('Enter');
  await expect(page.getByText(/status: not configured/i)).toBeVisible();
  await expect(page.getByRole('link', { name: /manage material deletion/i })).toHaveAttribute('href', '/mapping');
  expect(mutationHeaders).toEqual(['test-token', 'test-token']);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test('demo settings keeps credential management disabled', async ({ page }) => {
  let credentialStatusRequested = false;
  await page.route('**/api/settings', async (route) => {
    await route.fulfill({ json: { profile: 'demo', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false } });
  });
  await page.route('**/api/credentials/provider', async (route) => {
    credentialStatusRequested = true;
    await route.fulfill({ status: 503, json: { error: { code: 'credential_unavailable' } } });
  });

  await page.goto('/settings');
  await expect(page.getByText(/demo restrictions: credentials/i)).toBeVisible();
  await expect(page.getByLabel(/provider api key/i)).toHaveCount(0);
  expect(credentialStatusRequested).toBe(false);

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
  expect(overflow).toBe(false);
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
