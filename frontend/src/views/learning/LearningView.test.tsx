// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { LearningView } from './LearningView';

const sourceHash = 'a'.repeat(64);
const api = {
  listCourses: vi.fn().mockResolvedValue([{ courseId: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' }]),
  listMaterials: vi.fn().mockResolvedValue([{ materialId: 'material-1', filename: '并发讲义.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:00:00Z' }]),
  listSources: vi.fn().mockResolvedValue([{ locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: sourceHash, kind: 'text_lines', lineStart: 1, lineEnd: 1, text: '互斥保证临界区同一时刻只有一个执行者。' }]),
  listConcepts: vi.fn().mockResolvedValue([
    { conceptId: 'concept-1', name: '互斥', evaluatorId: 'os.mutex.v1', state: 'active', version: 1, coverage: { decision: 'confirmed', locatorIds: ['locator-1'], sourceStatus: 'current', version: 1 } },
    { conceptId: 'concept-explanation', name: '临界区背景', evaluatorId: null, state: 'explanation_only', version: 1, coverage: { decision: 'confirmed', locatorIds: ['locator-1'], sourceStatus: 'current', version: 1 } },
  ]),
};

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe('LearningView', () => {
  it('renders deterministic demo learning without provider preview or consent controls', async () => {
    render(<LearningView api={api} providerEnabled={false} />);

    expect(await screen.findByText('version-1')).toBeTruthy();
    expect(document.getElementById('provider-heading')).toBeNull();
    expect(document.querySelector('input[type="checkbox"]')).toBeNull();
  });

  it('loads current confirmed source identity and keeps evidence absent before submit', async () => {
    render(<LearningView api={api} />);

    expect(await screen.findByRole('heading', { name: '学习与练习' })).toBeTruthy();
    expect(screen.getByText('并发讲义.txt', { exact: false })).toBeTruthy();
    expect(screen.getByText('version-1')).toBeTruthy();
    expect(screen.getByText(sourceHash)).toBeTruthy();
    expect(screen.getByText('确定性规则')).toBeTruthy();
    expect(screen.queryByText('evidence-mutex-001')).toBeNull();
  });

  it('keeps explanation-only concepts out of deterministic grading', async () => {
    const user = userEvent.setup();
    render(<LearningView api={api} />);

    await user.selectOptions(await screen.findByLabelText('选择知识点'), 'concept-explanation');
    expect(screen.getAllByText('仅解释').length).toBeGreaterThan(0);
    expect(screen.queryByRole('button', { name: '提交确定性检查' })).toBeNull();
    expect(screen.getByText('该知识点不产生确定性证据。')).toBeTruthy();
    expect(screen.queryByText('evidence-mutex-001')).toBeNull();
  });

  it('fails closed for stale source coverage', async () => {
    const staleApi = {
      ...api,
      listConcepts: vi.fn().mockResolvedValue([
        { conceptId: 'concept-stale', name: '过期互斥', evaluatorId: 'os.mutex.v1', state: 'active', version: 2, coverage: { decision: 'confirmed', locatorIds: ['locator-1'], sourceStatus: 'stale', version: 2 } },
      ]),
    };
    render(<LearningView api={staleApi} />);

    expect(await screen.findByText('来源未确认、已过期或缺少不可变身份，学习与 P 预览均已禁用。')).toBeTruthy();
    expect((screen.getByRole('button', { name: '查看 P 提供方预览' }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole('group', { name: /执行轨迹/ }) as HTMLFieldSetElement).disabled).toBe(true);
  });

  it('creates local evidence only after submit and supports keyboard submission', async () => {
    const user = userEvent.setup();
    render(<LearningView api={api} />);

    const answer = await screen.findByLabelText('我的答案');
    await user.type(answer, '本地原始答案');
    const submit = screen.getByRole('button', { name: '提交确定性检查' });
    submit.focus();
    await user.keyboard('{Enter}');
    expect(await screen.findByText('evidence-concept-1-locator-1')).toBeTruthy();
    expect(screen.getByText('已通过')).toBeTruthy();
    expect(screen.getByText('本地原始答案')).toBeTruthy();

    await user.selectOptions(screen.getByLabelText('互斥是否成立'), 'false');
    await user.click(submit);
    expect(screen.getByText('需复核')).toBeTruthy();
  });

  it('requires consent and binds the preview to source identity without exposing the answer', async () => {
    const user = userEvent.setup();
    render(<LearningView api={api} />);

    const originalAnswer = await screen.findByLabelText('我的答案');
    await user.type(originalAnswer, '原始答案不应发送');
    await user.click(screen.getByRole('button', { name: '查看 P 提供方预览' }));

    const preview = screen.getByRole('region', { name: 'P 提供方预览' });
    expect(preview.textContent).toContain('version-1');
    expect(preview.textContent).toContain(sourceHash);
    expect(preview.textContent).toContain('最多 320 tokens');
    expect(preview.textContent).toContain('不包含原始答案');
    expect(preview.textContent).not.toContain('原始答案不应发送');
    const confirm = screen.getByRole('button', { name: '确认预览' });
    expect((confirm as HTMLButtonElement).disabled).toBe(true);
    await user.click(screen.getByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    expect((confirm as HTMLButtonElement).disabled).toBe(false);
  });
});
