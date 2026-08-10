import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

test('keeps learning source-bound and requires consent for the P preview', async ({ page }) => {
  const sourceHash = 'a'.repeat(64);
  const providerRequests: string[] = [];
  const providerBodies: Record<string, unknown>[] = [];
  page.on('request', (request) => {
    if (request.url().includes('/api/providers/')) providerRequests.push(request.url());
  });
  await page.route('**/*', async (route) => {
    const request = route.request();
    const path = new URL(request.url()).pathname;
    if (!path.startsWith('/api/')) {
      await route.continue();
      return;
    }
    if (path === '/api/settings') {
      await route.fulfill({ json: {
        profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L+P', provider_configured: true,
        provider_profile: {
          profile_id: 'openai-reviewed', adapter_id: 'openai', model_id: 'gpt-5.6-terra',
          input_token_cap: 20_000, output_token_cap: 3_000, max_cost_microusd: 118_250,
          config_fingerprint: 'b'.repeat(64), policy_fingerprint: 'c'.repeat(64),
        },
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
    if (path === '/api/courses/course-1/materials') {
      await route.fulfill({ json: { materials: [{ material_id: 'material-1', filename: '并发讲义.txt', media_type: 'text/plain', status: 'ready', created_at: '2026-08-07T09:00:00Z' }] } });
      return;
    }
    if (path === '/api/materials/material-1/sources') {
      await route.fulfill({ json: { sources: [{ locator_id: 'locator-1', material_version_id: 'version-1', content_hash: sourceHash, kind: 'text_lines', line_start: 1, line_end: 1, text: '互斥保证临界区同一时刻只有一个执行者。' }] } });
      return;
    }
    if (path === '/api/courses/course-1/concepts') {
      await route.fulfill({ json: { concepts: [
        { concept_id: 'concept-1', name: '互斥', evaluator_id: 'os.mutex.v1', state: 'active', version: 1, coverage: { decision: 'confirmed', locator_ids: ['locator-1'], source_status: 'current', version: 1 } },
        { concept_id: 'concept-explanation', name: '临界区背景', evaluator_id: null, state: 'explanation_only', version: 1, coverage: { decision: 'confirmed', locator_ids: ['locator-1'], source_status: 'current', version: 1 } },
      ] } });
      return;
    }
    if (path === '/api/providers/previews/explanation') {
      providerBodies.push(request.postDataJSON() as Record<string, unknown>);
      await route.fulfill({ json: {
        preview_id: 'preview-1', operation: 'generate_explanation', profile_id: 'openai-reviewed',
        adapter_id: 'openai', model_id: 'gpt-5.6-terra', input_token_cap: 20_000,
        max_tokens: 3_000, max_cost_microusd: 118_250, config_fingerprint: 'config-fingerprint',
        policy_fingerprint: 'policy-fingerprint',
        sources: [{
          locator_id: 'locator-1', material_version_id: 'version-1', content_hash: sourceHash,
          text: '互斥保证临界区同一时刻只有一个执行者。',
        }],
      } });
      return;
    }
    if (path === '/api/providers/consents') {
      providerBodies.push(request.postDataJSON() as Record<string, unknown>);
      await route.fulfill({ json: { consent_id: 'consent-1' } });
      return;
    }
    if (path === '/api/providers/execute') {
      providerBodies.push(request.postDataJSON() as Record<string, unknown>);
      await route.fulfill({ json: { text: 'Source-grounded candidate.', authoritative: false } });
      return;
    }
    await route.abort();
  });

  await page.goto('/learning');
  await expect(page.getByRole('heading', { name: '学习与练习' })).toBeVisible();
  await expect(page.getByText('version-1')).toBeVisible();
  await expect(page.getByText(sourceHash)).toBeVisible();
  await expect(page.getByText('确定性规则')).toBeVisible();
  await expect(page.getByText('evidence-concept-1-locator-1')).toHaveCount(0);

  await page.getByLabel('我的答案').fill('原始答案只留在本地');
  const submit = page.getByRole('button', { name: '提交确定性检查' });
  await submit.focus();
  await page.keyboard.press('Enter');
  await expect(page.getByText('evidence-concept-1-locator-1')).toBeVisible();
  await expect(page.getByText('已通过')).toBeVisible();

  await page.getByRole('button', { name: '查看 P 提供方预览' }).click();
  const preview = page.getByRole('region', { name: 'P 提供方预览' });
  await expect(preview).toContainText('version-1');
  await expect(preview).toContainText(sourceHash);
  await expect(preview).toContainText('20,000 input tokens');
  await expect(preview).toContainText('3,000 output tokens');
  await expect(preview).toContainText('USD 0.11825');
  await expect(preview).toContainText('不包含原始答案');
  await expect(preview).not.toContainText('原始答案只留在本地');
  const checkbox = page.getByRole('checkbox', { name: '我确认以上预览内容可以发送' });
  const confirm = page.getByRole('button', { name: '确认预览' });
  await expect(confirm).toBeDisabled();
  await checkbox.focus();
  await page.keyboard.press('Space');
  await expect(confirm).toBeEnabled();
  await confirm.focus();
  await page.keyboard.press('Enter');
  await expect(preview.getByRole('status')).toContainText('外部候选已返回');
  await expect(preview).toContainText('Source-grounded candidate.');
  expect(providerRequests).toHaveLength(3);
  expect(providerBodies[0]).toEqual(expect.objectContaining({
    locator_ids: ['locator-1'], profile_id: 'openai-reviewed',
  }));
  expect(providerBodies[0]).not.toHaveProperty('answer');
  expect(providerBodies[0]).not.toHaveProperty('max_tokens');
  expect(providerBodies[0]).not.toHaveProperty('max_cost_microusd');

  let result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(result.violations.filter(({ impact }) => impact === 'serious' || impact === 'critical')).toEqual([]);

  await page.getByLabel('选择知识点').selectOption('concept-explanation');
  await expect(page.getByRole('region', { name: '确定性练习' }).getByRole('status')).toContainText('仅解释');
  await expect(page.getByRole('button', { name: '提交确定性检查' })).toHaveCount(0);
  result = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(result.violations.filter(({ impact }) => impact === 'serious' || impact === 'critical')).toEqual([]);

  const viewport = page.viewportSize()!;
  const width = await page.evaluate(() => Math.max(document.body.scrollWidth, document.documentElement.scrollWidth));
  expect(width).toBeLessThanOrEqual(viewport.width);
});
