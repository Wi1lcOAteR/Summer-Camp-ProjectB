// @vitest-environment jsdom
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ReviewView } from './ReviewView';

const revision = {
  revisionId: 'revision-1',
  courseId: 'course-1',
  inputHash: 'b'.repeat(64),
  parentRevisionId: null,
  createdAt: '2026-08-12T12:00:00Z',
  tasks: [
    {
      taskId: 'task-1', revisionId: 'revision-1', conceptId: 'concept-1', dueLocalDate: '2026-08-13',
      durationMinutes: 10, status: 'pending' as const, sourceRefs: ['locator-1'], evidenceRefs: ['evidence-1'],
      completedAt: null, createdAt: '2026-08-12T12:00:00Z',
    },
    {
      taskId: 'task-2', revisionId: 'revision-1', conceptId: 'concept-1', dueLocalDate: '2026-08-15',
      durationMinutes: 10, status: 'skipped' as const, sourceRefs: ['locator-1'], evidenceRefs: ['evidence-1'],
      completedAt: null, createdAt: '2026-08-12T12:00:00Z',
    },
  ],
  diff: { added: ['concept-1@2026-08-13'], removed: [], changed: [], retained: [] },
};

function api() {
  return {
    listCourses: vi.fn().mockResolvedValue([{ courseId: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' }]),
    listConcepts: vi.fn().mockResolvedValue([
      { conceptId: 'concept-1', name: '互斥', evaluatorId: 'os.mutex.v1', state: 'active', version: 1 },
    ]),
    generateReviewRevision: vi.fn().mockResolvedValue(revision),
    completeReviewTask: vi.fn().mockResolvedValue({ ...revision.tasks[0], status: 'completed', completedAt: '2026-08-12T12:30:00Z' }),
    skipReviewTask: vi.fn().mockResolvedValue({ ...revision.tasks[0], status: 'skipped' }),
    recoverReviewTask: vi.fn().mockResolvedValue({ ...revision.tasks[1], status: 'pending' }),
  };
}

afterEach(cleanup);

describe('ReviewView', () => {
  it('renders the real backend revision without fixture sources or hashes', async () => {
    const client = api();
    render(<ReviewView api={client} now={() => new Date('2026-08-12T12:00:00Z')} />);

    expect(await screen.findByText('待复习 · 互斥')).toBeTruthy();
    expect(screen.getByText('2026-08-13 · 10 分钟')).toBeTruthy();
    expect(screen.getByText('1 个已确认来源')).toBeTruthy();
    expect(screen.queryByText('操作系统讲义.txt')).toBeNull();
    expect(screen.queryByText(/aaaaaaaa/)).toBeNull();
    expect(client.generateReviewRevision).toHaveBeenCalledWith(expect.objectContaining({
      courseId: 'course-1', mode: 'continuous', timezone: 'Asia/Shanghai', dailyBudgetMinutes: 30,
    }));
  });

  it('starts the first pending task and persists completion', async () => {
    const client = api();
    const user = userEvent.setup();
    render(<ReviewView api={client} now={() => new Date('2026-08-12T12:30:00Z')} />);

    await screen.findByText('待复习 · 互斥');
    await user.click(screen.getByRole('button', { name: '开始复习' }));
    expect(screen.getByRole('status').textContent).toContain('正在复习：互斥');
    await user.click(screen.getByRole('button', { name: '完成当前任务' }));

    expect(client.completeReviewTask).toHaveBeenCalledWith('task-1', '2026-08-12T12:30:00.000Z');
    expect(await screen.findByText('已完成 · 互斥')).toBeTruthy();
  });

  it('persists skip and recovery instead of changing only local copy', async () => {
    const client = api();
    const user = userEvent.setup();
    render(<ReviewView api={client} now={() => new Date('2026-08-12T12:00:00Z')} />);

    await screen.findByText('待复习 · 互斥');
    await user.click(screen.getByRole('button', { name: '跳过当前任务' }));
    expect(client.skipReviewTask).toHaveBeenCalledWith('task-1');
    await user.click(screen.getByRole('button', { name: '恢复已跳过任务' }));
    expect(client.recoverReviewTask).toHaveBeenCalledWith('task-1');
  });
});
