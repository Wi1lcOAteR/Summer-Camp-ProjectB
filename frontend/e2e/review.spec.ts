import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('uses persisted review revisions and task actions', async ({ page }) => {
  const inputHash = 'b'.repeat(64);
  const calls: string[] = [];
  const tasks = [
    {
      task_id: 'task-1', revision_id: 'revision-1', concept_id: 'concept-1',
      due_local_date: '2026-08-13', duration_minutes: 10, status: 'pending',
      source_refs: ['locator-1'], evidence_refs: ['evidence-1'], completed_at: null,
      created_at: '2026-08-12T12:00:00Z',
    },
    {
      task_id: 'task-2', revision_id: 'revision-1', concept_id: 'concept-1',
      due_local_date: '2026-08-15', duration_minutes: 10, status: 'pending',
      source_refs: ['locator-1'], evidence_refs: ['evidence-1'], completed_at: null,
      created_at: '2026-08-12T12:00:00Z',
    },
  ];

  await page.route('**/*', async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (!path.startsWith('/api/')) {
      await route.continue();
      return;
    }
    if (path === '/api/settings') {
      await route.fulfill({ json: {
        profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false,
      } });
      return;
    }
    if (path === '/api/session') {
      await route.fulfill({ headers: { 'x-csrf-token': 'test-csrf-token' }, json: { ok: true } });
      return;
    }
    if (path === '/api/courses') {
      await route.fulfill({ json: { courses: [{ course_id: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' }] } });
      return;
    }
    if (path === '/api/courses/course-1/concepts') {
      await route.fulfill({ json: { concepts: [
        { concept_id: 'concept-1', name: '互斥', evaluator_id: 'os.mutex.v1', state: 'active', version: 1 },
      ] } });
      return;
    }
    if (path === '/api/review/revisions') {
      calls.push('revision');
      await route.fulfill({ json: {
        revision_id: 'revision-1', course_id: 'course-1', input_hash: inputHash,
        parent_revision_id: null, created_at: '2026-08-12T12:00:00Z', tasks,
        diff: { added: ['concept-1@2026-08-13'], removed: [], changed: [], retained: [] },
      } });
      return;
    }
    const action = path.match(/^\/api\/review\/tasks\/(task-[12])\/(complete|skip|recover)$/);
    if (action) {
      const task = tasks.find((item) => item.task_id === action[1])!;
      calls.push(`${action[2]}:${task.task_id}`);
      task.status = action[2] === 'complete' ? 'completed' : action[2] === 'skip' ? 'skipped' : 'pending';
      task.completed_at = action[2] === 'complete' ? '2026-08-12T12:30:00Z' : null;
      await route.fulfill({ json: task });
      return;
    }
    await route.abort();
  });

  await page.goto('/review');
  await expect(page.getByRole('heading', { name: '复习计划' })).toBeVisible();
  await expect(page.getByText('待复习 · 互斥')).toHaveCount(2);
  await expect(page.getByText(inputHash)).toBeVisible();
  await expect(page.getByText('操作系统讲义.txt')).toHaveCount(0);

  await page.getByRole('button', { name: '开始复习' }).focus();
  await page.keyboard.press('Enter');
  await expect(page.getByRole('status')).toContainText('正在复习：互斥');
  await page.getByRole('button', { name: '完成当前任务' }).click();
  await expect(page.getByText('已完成 · 互斥')).toBeVisible();

  await page.getByRole('button', { name: '跳过当前任务' }).click();
  await expect(page.getByText('已跳过 · 互斥')).toBeVisible();
  await page.getByRole('button', { name: '恢复已跳过任务' }).click();
  await expect(page.getByText('待复习 · 互斥')).toBeVisible();
  expect(calls).toEqual(['revision', 'complete:task-1', 'skip:task-2', 'recover:task-2']);

  const result = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(result.violations.filter(({ impact }) => impact === 'serious' || impact === 'critical')).toEqual([]);
  const viewport = page.viewportSize()!;
  const width = await page.evaluate(() => Math.max(document.body.scrollWidth, document.documentElement.scrollWidth));
  expect(width).toBeLessThanOrEqual(viewport.width);
});
