import { expect, test } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('review planner', () => {
  test('supports keyboard controls, recovery, and accessible responsive layout', async ({ page }) => {
    await page.goto('/review');
    await expect(page.getByRole('heading', { name: '复习计划' })).toBeVisible();
    await expect(page.getByText('今日预算')).toBeVisible();
    await expect(page.getByText('操作系统讲义.txt')).toBeVisible();

    await page.getByRole('radio', { name: '最终复习' }).press('Space');
    await expect(page.getByText('最终复习已选择')).toBeVisible();
    await expect(page.getByLabel('考试日期')).toBeVisible();
    await page.getByLabel('压缩重复项').press('Space');
    await expect(page.getByText('未压缩重复项，保留完整练习轨迹。')).toBeVisible();
    await page.getByLabel('考试日期').fill('2026-08-01');
    await expect(page.getByRole('alert')).toContainText('考试日期已过去');
    await page.getByRole('button', { name: '恢复未完成项' }).press('Enter');
    await expect(page.getByText('已恢复 2 个未完成项；已完成任务保持不变')).toBeVisible();
    await expect(page.getByText('恢复中 · 竞态条件')).toBeVisible();

    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth);
    expect(overflow).toBe(false);
    const results = await new AxeBuilder({ page }).analyze();
    expect(results.violations).toEqual([]);
  });
});
