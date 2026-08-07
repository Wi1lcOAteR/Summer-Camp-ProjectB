import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
import { join, resolve } from 'node:path';
import { ensureShellTestServer, shellBaseUrl } from './support/testServer';

const screenshotDir = resolve(__dirname, '..', '..', 'docs', 'engineering', 'open-design');

const viewports = [
  { name: 'mobile-360', width: 360, height: 800 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'desktop-1440', width: 1440, height: 900 },
] as const;

let stopServer: (() => Promise<void>) | undefined;

test.beforeAll(async () => {
  stopServer = await ensureShellTestServer();
});

test.afterAll(async () => {
  await stopServer?.();
});

for (const viewport of viewports) {
  test.describe(viewport.name, () => {
    test.use({ viewport: { width: viewport.width, height: viewport.height } });

    test.beforeEach(async ({ page }) => {
      await page.goto(shellBaseUrl);
    });

    test('exposes the four-stage workbench through semantic landmarks', async ({ page }) => {
      await expect(page.getByRole('banner')).toBeVisible();
      const workflow = page.getByRole('navigation', { name: '学习流程' });
      await expect(workflow).toBeVisible();
      await expect(page.getByRole('main')).toBeVisible();

      for (const stage of ['导入', '映射', '学习', '复习']) {
        await expect(workflow.getByRole('link', { name: stage, exact: true })).toBeVisible();
      }
      await expect(page.getByRole('link', { name: '设置', exact: true })).toBeVisible();
      await mkdir(screenshotDir, { recursive: true });
      await page.screenshot({
        path: join(screenshotDir, `ui01-${viewport.width}.png`),
        fullPage: true,
      });
    });

    test('fits the viewport without page-level horizontal overflow', async ({ page }) => {
      const dimensions = await page.evaluate(() => ({
        body: document.body.scrollWidth,
        document: document.documentElement.scrollWidth,
      }));

      expect(dimensions.body).toBeLessThanOrEqual(viewport.width);
      expect(dimensions.document).toBeLessThanOrEqual(viewport.width);
    });

    test('provides visible keyboard focus in workflow order', async ({ page }) => {
      await page.keyboard.press('Tab');
      const firstStage = page.getByRole('link', { name: '导入', exact: true });
      await expect(firstStage).toBeFocused();

      const focusStyle = await firstStage.evaluate((element) => {
        const style = getComputedStyle(element);
        return { outlineStyle: style.outlineStyle, outlineWidth: style.outlineWidth };
      });
      expect(focusStyle.outlineStyle).not.toBe('none');
      expect(focusStyle.outlineWidth).not.toBe('0px');
    });

    test('has no serious or critical axe violations', async ({ page }) => {
      const result = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
        .analyze();
      const blocking = result.violations.filter(
        ({ impact }) => impact === 'serious' || impact === 'critical',
      );

      expect(blocking).toEqual([]);
    });
  });
}
