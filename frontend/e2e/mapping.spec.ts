import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('inspects and confirms source mappings without hiding destructive actions', async ({ page }) => {
  let decision: 'confirmed' | undefined;
  let deleted = false;
  await page.route('**/*', async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (!path.startsWith('/api/')) {
      await route.continue();
      return;
    }
    if (path === '/api/courses' && request.method() === 'GET') {
      await route.fulfill({ json: { courses: [{ course_id: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' }] } });
      return;
    }
    if (path === '/api/courses/course-1/materials') {
      await route.fulfill({ json: { materials: deleted ? [] : [{ material_id: 'material-1', filename: '并发讲义.txt', media_type: 'text/plain', status: 'ready', created_at: '2026-08-07T09:00:00Z' }] } });
      return;
    }
    if (path === '/api/materials/material-1/sources') {
      await route.fulfill({ json: { sources: [{ locator_id: 'locator-1', material_version_id: 'version-1', content_hash: 'a'.repeat(64), kind: 'text_lines', line_start: 1, line_end: 1, text: '互斥保证临界区同一时刻只有一个执行者。' }] } });
      return;
    }
    if (path === '/api/courses/course-1/concepts') {
      await route.fulfill({ json: { concepts: [{ concept_id: 'concept-1', name: '互斥', evaluator_id: 'os.mutex.v1', state: 'active', version: 1, coverage: decision ? { decision, locator_ids: ['locator-1'], source_status: 'current', version: 1 } : null }] } });
      return;
    }
    if (path === '/api/session') {
      await route.fulfill({ status: 200, headers: { 'x-csrf-token': 'e2e-csrf' }, json: { status: 'ready' } });
      return;
    }
    if (path === '/api/concepts/concept-1/mapping' && request.method() === 'POST') {
      expect(request.headers()['x-csrf-token']).toBe('e2e-csrf');
      decision = 'confirmed';
      await route.fulfill({ json: { decision, version: 1 } });
      return;
    }
    if (path === '/api/materials/material-1' && request.method() === 'DELETE') {
      expect(request.headers()['x-csrf-token']).toBe('e2e-csrf');
      deleted = true;
      await route.fulfill({ json: { status: 'deleted', retryable: false } });
      return;
    }
    await route.abort();
  });

  await page.goto('/mapping');
  await expect(page.getByRole('heading', { name: '核对来源映射' })).toBeVisible();
  await expect(page.getByText('互斥保证临界区同一时刻只有一个执行者。')).toBeVisible();
  await expect(page.locator('strong').filter({ hasText: '尚未确认' })).toBeVisible();

  await page.getByRole('checkbox', { name: /第 1 行/ }).check();
  const confirm = page.getByRole('button', { name: '确认来源' });
  await confirm.focus();
  await expect(confirm).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('strong').filter({ hasText: '已确认' })).toBeVisible();

  await page.getByRole('button', { name: '删除 并发讲义.txt' }).click();
  const dialog = page.getByRole('dialog', { name: '确认删除材料' });
  const cancelDelete = dialog.getByRole('button', { name: '取消' });
  const confirmDelete = dialog.getByRole('button', { name: '确认删除' });
  await expect(dialog).toBeVisible();
  await expect(cancelDelete).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(confirmDelete).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(cancelDelete).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(dialog).toBeHidden();
  await expect(page.getByRole('button', { name: '删除 并发讲义.txt' })).toBeFocused();

  await page.getByRole('button', { name: '删除 并发讲义.txt' }).click();
  await expect(cancelDelete).toBeFocused();
  await page.keyboard.press('Tab');
  await expect(confirmDelete).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(dialog).toBeHidden();
  await expect(page.getByRole('button', { name: '删除 并发讲义.txt' })).toHaveCount(0);
  await expect(page.getByLabel('选择材料')).toBeFocused();

  const viewport = page.viewportSize()!;
  const width = await page.evaluate(() => Math.max(document.body.scrollWidth, document.documentElement.scrollWidth));
  expect(width).toBeLessThanOrEqual(viewport.width);
  const result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(result.violations.filter(({ impact }) => impact === 'serious' || impact === 'critical')).toEqual([]);
});
