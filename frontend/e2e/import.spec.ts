import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { ensureShellTestServer, shellBaseUrl } from './support/testServer';

let stopServer: (() => Promise<void>) | undefined;

test.beforeAll(async () => {
  stopServer = await ensureShellTestServer();
});

test.afterAll(async () => {
  await stopServer?.();
});

test('imports one file with keyboard controls and keeps the responsive view accessible', async ({ page }) => {
  let imported = false;
  await page.route('**/api/**', async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (path === '/api/courses' && request.method() === 'GET') {
      await route.fulfill({ json: { courses: [{ course_id: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' }] } });
      return;
    }
    if (path === '/api/session' && request.method() === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        headers: { 'x-csrf-token': 'e2e-csrf-token' },
        body: JSON.stringify({ status: 'ready' }),
      });
      return;
    }
    if (path === '/api/courses/course-1/materials/import' && request.method() === 'POST') {
      expect(request.headers()['x-csrf-token']).toBe('e2e-csrf-token');
      imported = true;
      await route.fulfill({ json: { results: [{ status: 'imported', material_id: 'material-2', version_id: 'version-2', retryable: false, content_hash: 'b'.repeat(64) }] } });
      return;
    }
    if (path === '/api/courses/course-1/materials' && request.method() === 'GET') {
      const materials = [
        { material_id: 'material-1', filename: '并发讲义.pdf', media_type: 'application/pdf', content_hash: 'a'.repeat(64), status: 'ready', created_at: '2026-08-07T09:00:00Z' },
      ];
      if (imported) materials.push(
        { material_id: 'material-2', filename: '互斥笔记.md', media_type: 'text/markdown', content_hash: 'b'.repeat(64), status: 'ready', created_at: '2026-08-07T09:05:00Z' },
      );
      await route.fulfill({ json: { materials } });
      return;
    }
    await route.continue();
  });

  await page.goto(`${shellBaseUrl}/import`);
  await expect(page.getByRole('heading', { name: '导入课程材料' })).toBeVisible();
  await expect(page.getByRole('heading', { name: '导入限制' })).toBeVisible();
  await expect(page.getByRole('button', { name: '选择文件' })).toBeVisible();
  await expect(page.getByText('并发讲义.pdf')).toBeVisible();

  const chooseButton = page.getByRole('button', { name: '选择文件' });
  await chooseButton.focus();
  await expect(chooseButton).toBeFocused();
  const focusStyle = await chooseButton.evaluate((element) => getComputedStyle(element).outlineStyle);
  expect(focusStyle).not.toBe('none');

  await page.getByLabel('选择材料文件').setInputFiles({
    name: '互斥笔记.md',
    mimeType: 'text/markdown',
    buffer: Buffer.from('# 互斥'),
  });
  const importButton = page.getByRole('button', { name: '开始导入' });
  await importButton.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByText('已成功导入 1 个文件')).toBeVisible();
  await expect(page.getByText('2 份本地材料')).toBeVisible();

  const viewport = page.viewportSize();
  expect(viewport).not.toBeNull();
  expect([360, 768, 1440]).toContain(viewport!.width);
  const dimensions = await page.evaluate(() => ({
    body: document.body.scrollWidth,
    document: document.documentElement.scrollWidth,
  }));
  expect(dimensions.body).toBeLessThanOrEqual(viewport!.width);
  expect(dimensions.document).toBeLessThanOrEqual(viewport!.width);

  const result = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(result.violations.filter(({ impact }) => impact === 'serious' || impact === 'critical')).toEqual([]);
});
