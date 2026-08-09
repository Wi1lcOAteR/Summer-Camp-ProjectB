import { expect, test } from '@playwright/test';

const demoBaseUrl = 'http://127.0.0.1:7860';

test('boots the real demo assembly', async () => {
  const response = await fetch(`${demoBaseUrl}/api/settings`);
  expect(response.status).toBe(200);
  expect(await response.json()).toEqual({
    profile: 'demo',
    bind_host: '0.0.0.0',
    provider_mode: 'L',
    provider_configured: false,
  });
});

test('real demo UI exposes only isolated mock capabilities', async ({ browser }) => {
  const firstContext = await browser.newContext();
  const secondContext = await browser.newContext();
  const first = await firstContext.newPage();
  const second = await secondContext.newPage();
  try {
    await first.goto(`${demoBaseUrl}/import`);
    await expect(first.getByText('Public demo materials are synthetic and isolated to this browser session.')).toBeVisible();
    await expect(first.locator('.course strong')).toHaveText('Concurrent Systems Demo');
    await expect(first.getByText('materials.md')).toBeVisible();
    await expect(first.locator('input[type="file"]')).toHaveCount(0);

    const apiContract = await first.evaluate(async () => {
      const session = await fetch('/api/session', { credentials: 'same-origin' });
      const csrf = session.headers.get('x-csrf-token') ?? '';
      const courses = await fetch('/api/courses', { credentials: 'same-origin' }).then((value) => value.json());
      const courseId = courses.courses[0].course_id;
      const mutation: RequestInit = {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'x-csrf-token': csrf },
      };
      const explanation = await fetch('/api/demo/fixture-explanation', { credentials: 'same-origin' });
      return {
        upload: (await fetch(`/api/courses/${courseId}/materials/import`, mutation)).status,
        credentials: (await fetch('/api/credentials/provider', { credentials: 'same-origin' })).status,
        providers: (await fetch('/api/providers/execute', mutation)).status,
        explanation: await explanation.json(),
      };
    });
    expect(apiContract.upload).toBe(404);
    expect(apiContract.credentials).toBe(404);
    expect(apiContract.providers).toBe(404);
    expect(apiContract.explanation).toMatchObject({
      text: 'Mock explanation: Explain the confirmed synthetic source.',
      authoritative: false,
    });

    await first.goto(`${demoBaseUrl}/learning`);
    await expect(first.locator('#provider-heading')).toHaveCount(0);
    await expect(first.locator('input[type="checkbox"]')).toHaveCount(0);

    await first.goto(`${demoBaseUrl}/settings`);
    await expect(first.getByText('Demo / 0.0.0.0')).toBeVisible();
    await expect(first.getByRole('heading', { name: 'Demo profile' })).toBeVisible();
    await expect(first.getByLabel(/provider api key/i)).toHaveCount(0);
    await expect(first.getByText(/network calls require explicit consent/i)).toHaveCount(0);

    await second.goto(`${demoBaseUrl}/import`);
    const createStatus = await first.evaluate(async () => {
      const session = await fetch('/api/session', { credentials: 'same-origin' });
      const csrf = session.headers.get('x-csrf-token') ?? '';
      return (await fetch('/api/courses', {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'content-type': 'application/json', 'x-csrf-token': csrf },
        body: JSON.stringify({ name: 'First session only', timezone: 'UTC' }),
      })).status;
    });
    expect(createStatus).toBe(201);
    const secondCourses = await second.evaluate(async () => (
      fetch('/api/courses', { credentials: 'same-origin' }).then((response) => response.json())
    ));
    expect(secondCourses.courses.map((course: { name: string }) => course.name)).toEqual([
      'Concurrent Systems Demo',
    ]);
  } finally {
    await firstContext.close();
    await secondContext.close();
  }
});
