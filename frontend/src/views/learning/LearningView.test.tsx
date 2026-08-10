// @vitest-environment jsdom

import { act, cleanup, render, screen } from '@testing-library/react';
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
  getProviderSettings: vi.fn().mockResolvedValue({
    providerMode: 'L+P',
    providerProfile: {
      profileId: 'openai-profile', adapterId: 'openai', modelId: 'gpt-5.6-terra',
      inputTokenCap: 20000, outputTokenCap: 3000, maxCostMicrousd: 118250,
      configFingerprint: 'b'.repeat(64), policyFingerprint: 'c'.repeat(64),
    },
  }),
  previewExplanation: vi.fn().mockResolvedValue({
    previewId: 'preview-1', operation: 'generate_explanation', profileId: 'openai-profile',
    adapterId: 'openai', modelId: 'gpt-5.6-terra', inputTokenCap: 20000,
    outputTokenCap: 3000, maxCostMicrousd: 118250, policyFingerprint: 'c'.repeat(64),
    configFingerprint: 'b'.repeat(64),
    sources: [{ locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: sourceHash, text: '服务器确认片段。' }],
  }),
  grantProviderConsent: vi.fn().mockResolvedValue({ consentId: 'consent-1' }),
  executeProvider: vi.fn().mockResolvedValue({ text: '模型候选解释', authoritative: false }),
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

  it('keeps deterministic learning available when optional provider settings fail', async () => {
    const localOnlyApi = {
      ...api,
      getProviderSettings: vi.fn().mockRejectedValue(new Error('provider settings unavailable')),
    };
    render(<LearningView api={localOnlyApi} />);

    expect(await screen.findByText('version-1')).toBeTruthy();
    expect(screen.getByRole('button', { name: '提交确定性检查' })).toBeTruthy();
    expect(document.getElementById('provider-heading')).toBeNull();
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

    const preview = await screen.findByRole('region', { name: 'P 提供方预览' });
    expect(preview.textContent).toContain('version-1');
    expect(preview.textContent).toContain(sourceHash);
    expect(preview.textContent).toContain('服务器确认片段。');
    expect(preview.textContent).not.toContain('互斥保证临界区同一时刻只有一个执行者。');
    expect(preview.textContent).toContain('20,000 input tokens');
    expect(preview.textContent).toContain('3,000 output tokens');
    expect(preview.textContent).toContain('USD 0.11825');
    expect(preview.textContent).toContain('最长 30 天');
    expect(preview.textContent).toContain('最长 24 小时');
    expect(preview.textContent).toContain('不代表 ZDR');
    expect(preview.textContent).toContain('不包含原始答案');
    expect(preview.textContent).not.toContain('原始答案不应发送');
    const confirm = screen.getByRole('button', { name: '确认预览' });
    expect((confirm as HTMLButtonElement).disabled).toBe(true);
    await user.click(screen.getByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    expect((confirm as HTMLButtonElement).disabled).toBe(false);
    await user.click(confirm);
    expect(await screen.findByText(/模型候选解释/)).toBeTruthy();
    expect(api.grantProviderConsent).toHaveBeenCalledWith('preview-1');
    expect(api.executeProvider).toHaveBeenCalledWith('preview-1', 'consent-1');
    const outbound = api.previewExplanation.mock.calls.at(-1)?.[0];
    expect(JSON.stringify(outbound)).not.toContain('原始答案不应发送');
  });

  it('discards a preview that resolves after the selected concept changes', async () => {
    const user = userEvent.setup();
    let resolvePreview: ((value: Awaited<ReturnType<typeof api.previewExplanation>>) => void) | undefined;
    const delayedApi = {
      ...api,
      previewExplanation: vi.fn(() => new Promise<Awaited<ReturnType<typeof api.previewExplanation>>>((resolve) => {
        resolvePreview = resolve;
      })),
    };
    render(<LearningView api={delayedApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-explanation');
    await act(async () => {
      resolvePreview?.({
        previewId: 'preview-stale', operation: 'generate_explanation', profileId: 'openai-profile',
        adapterId: 'openai', modelId: 'gpt-5.6-terra', inputTokenCap: 20000,
        outputTokenCap: 3000, maxCostMicrousd: 118250, policyFingerprint: 'c'.repeat(64),
        configFingerprint: 'b'.repeat(64),
        sources: [{ locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: sourceHash, kind: 'text_lines', lineStart: 1, lineEnd: 1, text: '互斥保证临界区同一时刻只有一个执行者。' }],
      });
      await Promise.resolve();
    });
    expect(screen.queryByRole('region', { name: 'P 提供方预览' })).toBeNull();
    expect(delayedApi.grantProviderConsent).not.toHaveBeenCalled();
    expect(delayedApi.executeProvider).not.toHaveBeenCalled();
  });

  it('does not execute when consent resolves after the selected concept changes', async () => {
    const user = userEvent.setup();
    let resolveConsent: ((value: { consentId: string }) => void) | undefined;
    const delayedApi = {
      ...api,
      grantProviderConsent: vi.fn(() => new Promise<{ consentId: string }>((resolve) => {
        resolveConsent = resolve;
      })),
      executeProvider: vi.fn(),
    };
    render(<LearningView api={delayedApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-explanation');
    await act(async () => {
      resolveConsent?.({ consentId: 'consent-stale' });
      await Promise.resolve();
    });

    expect(delayedApi.executeProvider).not.toHaveBeenCalled();
    expect(screen.queryByText(/外部候选/)).toBeNull();
  });

  it('discards a provider candidate that resolves after the selected concept changes', async () => {
    const user = userEvent.setup();
    let resolveCandidate: ((value: { text: string; authoritative: false }) => void) | undefined;
    const delayedApi = {
      ...api,
      grantProviderConsent: vi.fn().mockResolvedValue({ consentId: 'consent-1' }),
      executeProvider: vi.fn(() => new Promise<{ text: string; authoritative: false }>((resolve) => {
        resolveCandidate = resolve;
      })),
    };
    render(<LearningView api={delayedApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-explanation');
    await act(async () => {
      resolveCandidate?.({ text: 'stale candidate', authoritative: false });
      await Promise.resolve();
    });

    expect(screen.queryByText('stale candidate')).toBeNull();
    expect(screen.queryByText(/外部候选/)).toBeNull();
  });

  it('discards a consent error that arrives after the selected concept changes', async () => {
    const user = userEvent.setup();
    let rejectConsent: ((reason: Error) => void) | undefined;
    const delayedApi = {
      ...api,
      grantProviderConsent: vi.fn(() => new Promise<{ consentId: string }>((_resolve, reject) => {
        rejectConsent = reject;
      })),
    };
    render(<LearningView api={delayedApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-explanation');
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-1');
    await user.click(screen.getByRole('button', { name: '查看 P 提供方预览' }));
    expect(await screen.findByRole('region', { name: 'P 提供方预览' })).toBeTruthy();
    await act(async () => {
      rejectConsent?.(new Error('stale consent failure'));
      await Promise.resolve();
    });

    expect(screen.queryByText(/stale consent failure/)).toBeNull();
    expect(screen.queryByText(/提供方请求失败/)).toBeNull();
  });

  it('discards an execute error that arrives after the selected concept changes', async () => {
    const user = userEvent.setup();
    let rejectCandidate: ((reason: Error) => void) | undefined;
    const delayedApi = {
      ...api,
      grantProviderConsent: vi.fn().mockResolvedValue({ consentId: 'consent-1' }),
      executeProvider: vi.fn(() => new Promise<{ text: string; authoritative: false }>((_resolve, reject) => {
        rejectCandidate = reject;
      })),
    };
    render(<LearningView api={delayedApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-explanation');
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-1');
    await user.click(screen.getByRole('button', { name: '查看 P 提供方预览' }));
    expect(await screen.findByRole('region', { name: 'P 提供方预览' })).toBeTruthy();
    await act(async () => {
      rejectCandidate?.(new Error('stale execute failure'));
      await Promise.resolve();
    });

    expect(screen.queryByText(/stale execute failure/)).toBeNull();
    expect(screen.queryByText(/提供方请求失败/)).toBeNull();
  });

  it('revokes the old preview while a replacement preview overlaps its pending consent', async () => {
    const user = userEvent.setup();
    const firstPreview = {
      previewId: 'preview-first', operation: 'generate_explanation' as const, profileId: 'openai-profile',
      adapterId: 'openai' as const, modelId: 'gpt-5.6-terra', inputTokenCap: 20000,
      outputTokenCap: 3000, maxCostMicrousd: 118250, policyFingerprint: 'c'.repeat(64),
      configFingerprint: 'b'.repeat(64),
      sources: [{ locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: sourceHash, text: 'first source' }],
    };
    const secondPreview = { ...firstPreview, previewId: 'preview-second', sources: [{ ...firstPreview.sources[0], text: 'second source' }] };
    let resolveSecondPreview: ((value: typeof secondPreview) => void) | undefined;
    let resolveConsent: ((value: { consentId: string }) => void) | undefined;
    const overlappingApi = {
      ...api,
      previewExplanation: vi.fn()
        .mockResolvedValueOnce(firstPreview)
        .mockImplementationOnce(() => new Promise<typeof secondPreview>((resolve) => { resolveSecondPreview = resolve; })),
      grantProviderConsent: vi.fn(() => new Promise<{ consentId: string }>((resolve) => { resolveConsent = resolve; })),
      executeProvider: vi.fn(),
    };
    render(<LearningView api={overlappingApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.click(screen.getByRole('button', { name: '查看 P 提供方预览' }));

    expect(screen.queryByRole('button', { name: '确认预览' })).toBeNull();
    await act(async () => {
      resolveSecondPreview?.(secondPreview);
      resolveConsent?.({ consentId: 'consent-first' });
      await Promise.resolve();
    });
    expect(await screen.findByText(/second source/)).toBeTruthy();
    expect(overlappingApi.executeProvider).not.toHaveBeenCalled();
  });

  it('does not attach an old consent rejection to a replacement preview', async () => {
    const user = userEvent.setup();
    const firstPreview = {
      previewId: 'preview-first', operation: 'generate_explanation' as const, profileId: 'openai-profile',
      adapterId: 'openai' as const, modelId: 'gpt-5.6-terra', inputTokenCap: 20000,
      outputTokenCap: 3000, maxCostMicrousd: 118250, policyFingerprint: 'c'.repeat(64),
      configFingerprint: 'b'.repeat(64),
      sources: [{ locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: sourceHash, text: 'first source' }],
    };
    const secondPreview = { ...firstPreview, previewId: 'preview-second', sources: [{ ...firstPreview.sources[0], text: 'second source' }] };
    let resolveSecondPreview: ((value: typeof secondPreview) => void) | undefined;
    let rejectConsent: ((reason: Error) => void) | undefined;
    const overlappingApi = {
      ...api,
      previewExplanation: vi.fn()
        .mockResolvedValueOnce(firstPreview)
        .mockImplementationOnce(() => new Promise<typeof secondPreview>((resolve) => { resolveSecondPreview = resolve; })),
      grantProviderConsent: vi.fn(() => new Promise<{ consentId: string }>((_resolve, reject) => { rejectConsent = reject; })),
    };
    render(<LearningView api={overlappingApi} />);

    await user.click(await screen.findByRole('button', { name: '查看 P 提供方预览' }));
    await user.click(await screen.findByRole('checkbox', { name: '我确认以上预览内容可以发送' }));
    await user.click(screen.getByRole('button', { name: '确认预览' }));
    await user.click(screen.getByRole('button', { name: '查看 P 提供方预览' }));
    await act(async () => {
      resolveSecondPreview?.(secondPreview);
      rejectConsent?.(new Error('old consent rejected'));
      await Promise.resolve();
    });

    expect(await screen.findByText(/second source/)).toBeTruthy();
    expect(screen.queryByText(/提供方请求失败/)).toBeNull();
  });
});
