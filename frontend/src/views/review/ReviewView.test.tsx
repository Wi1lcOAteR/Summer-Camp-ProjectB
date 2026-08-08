// @vitest-environment jsdom
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it } from 'vitest';
import { ReviewView } from './ReviewView';

afterEach(cleanup);

describe('ReviewView', () => {
  it('renders deterministic review budget, source identity, mastery, and controls', () => {
    render(<ReviewView />);

    expect(screen.getByRole('heading', { name: '复习计划' })).toBeTruthy();
    expect(screen.getByText('今日预算')).toBeTruthy();
    expect(screen.getAllByText('30 分钟').length).toBeGreaterThan(0);
    expect(screen.getByText('3 个来源')).toBeTruthy();
    expect(screen.getByText('操作系统讲义.txt')).toBeTruthy();
    expect(screen.getByText('掌握度')).toBeTruthy();
    expect(screen.getByRole('radiogroup', { name: '复习模式' })).toBeTruthy();
    expect(screen.getByLabelText('压缩重复项')).toBeTruthy();
    expect(screen.getByLabelText('截止时间')).toBeTruthy();
    expect(screen.getByLabelText('每日预算（分钟）')).toBeTruthy();
    expect(screen.getByRole('region', { name: '计划修订差异' })).toBeTruthy();
  });

  it('updates the local plan and preserves completed work when recovery is used', async () => {
    const user = userEvent.setup();
    render(<ReviewView />);

    await user.click(screen.getByRole('radio', { name: '最终复习' }));
    expect(screen.getByText('最终复习已选择')).toBeTruthy();
    await user.click(screen.getByRole('button', { name: '恢复未完成项' }));
    expect(screen.getByText('已恢复 2 个未完成项；已完成任务保持不变')).toBeTruthy();
    expect(screen.getByText('已完成 · 互斥')).toBeTruthy();
    expect(screen.getByRole('button', { name: '开始复习' })).toBeTruthy();
  });

  it('uses the finals policy value, exposes an exam date, and fails closed for past exams', async () => {
    const user = userEvent.setup();
    render(<ReviewView />);

    const finals = screen.getByRole('radio', { name: '最终复习' });
    expect(finals.getAttribute('value')).toBe('finals');
    await user.click(finals);
    const examDate = screen.getByLabelText('考试日期');
    expect(examDate.getAttribute('type')).toBe('date');
    await user.clear(examDate);
    await user.type(examDate, '2026-08-01');
    expect(screen.getByRole('alert').textContent).toContain('考试日期已过去');
    expect(screen.getByText('可安排任务').parentElement?.textContent).toContain('0');
  });

  it('updates revision contents and marks recovered work without changing completed state', async () => {
    const user = userEvent.setup();
    render(<ReviewView />);

    await user.click(screen.getByLabelText('压缩重复项'));
    expect(screen.getByText('未压缩重复项，保留完整练习轨迹。')).toBeTruthy();
    await user.click(screen.getByRole('button', { name: '恢复未完成项' }));
    expect(screen.getByText('恢复中 · 竞态条件')).toBeTruthy();
    expect(screen.getByText('已完成 · 互斥')).toBeTruthy();
  });
});
