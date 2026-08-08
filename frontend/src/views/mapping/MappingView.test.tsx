// @vitest-environment jsdom

import { cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiRequestError, createApiClient } from '../../api/client';
import { MappingView } from './MappingView';

afterEach(cleanup);

function createMappingApi() {
  return {
    listCourses: vi.fn().mockResolvedValue([
      { courseId: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' },
    ]),
    listMaterials: vi.fn().mockResolvedValue([
      { materialId: 'material-1', filename: '并发讲义.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:00:00Z' },
    ]),
    listSources: vi.fn().mockResolvedValue([
      { locatorId: 'locator-1', materialVersionId: 'version-1', contentHash: 'a'.repeat(64), kind: 'text_lines', lineStart: 1, lineEnd: 1, text: '互斥保证临界区同一时刻只有一个执行者。' },
      { locatorId: 'locator-2', materialVersionId: 'version-1', contentHash: 'a'.repeat(64), kind: 'text_lines', lineStart: 2, lineEnd: 2, text: '竞态取决于不可控的执行顺序。' },
    ]),
    listConcepts: vi.fn().mockResolvedValue([
      { conceptId: 'concept-1', name: '互斥', evaluatorId: 'os.mutex.v1', state: 'active', version: 1, coverage: { decision: 'confirmed', locatorIds: ['locator-1'], sourceStatus: 'current', version: 1 } },
      { conceptId: 'concept-2', name: '竞态', evaluatorId: 'os.race.v1', state: 'active', version: 1 },
    ]),
    createConcept: vi.fn(),
    mapConcept: vi.fn().mockResolvedValue({ decision: 'confirmed', version: 1 }),
    deleteMaterial: vi.fn().mockResolvedValue({ status: 'deleted', retryable: false }),
  };
}

describe('MappingView', () => {
  it('shows inspectable locators and records explicit confirm or reject decisions', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    render(<MappingView api={api} />);

    expect(await screen.findByText('互斥保证临界区同一时刻只有一个执行者。')).toBeTruthy();
    expect(screen.getByText('第 1 行')).toBeTruthy();
    expect(screen.getAllByText('已确认').length).toBeGreaterThan(0);

    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-2');
    await user.click(screen.getByRole('checkbox', { name: /第 2 行/ }));
    await user.click(screen.getByRole('button', { name: '确认来源' }));
    expect(api.mapConcept).toHaveBeenCalledWith('concept-2', ['locator-2'], 'confirmed');

    await user.click(screen.getByRole('button', { name: '拒绝映射' }));
    expect(api.mapConcept).toHaveBeenLastCalledWith('concept-2', ['locator-2'], 'rejected');
  });

  it('marks stale coverage and requires confirmation before deleting a material', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    api.listConcepts.mockResolvedValueOnce([
      { conceptId: 'concept-1', name: '互斥', evaluatorId: 'os.mutex.v1', state: 'active', version: 1, coverage: { decision: 'confirmed', locatorIds: ['missing-locator'], sourceStatus: 'stale', version: 1 } },
    ]);
    render(<MappingView api={api} />);

    expect((await screen.findAllByText('来源已失效')).length).toBeGreaterThan(0);
    await user.click(screen.getByRole('button', { name: '删除 并发讲义.txt' }));
    const dialog = screen.getByRole('dialog', { name: '确认删除材料' });
    expect(dialog.textContent).toContain('并发讲义.txt');
    await user.click(screen.getByRole('button', { name: '确认删除' }));
    expect(api.deleteMaterial).toHaveBeenCalledWith('material-1');
  });

  it('clears hidden locator selections when the visible material changes', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    api.listMaterials.mockResolvedValue([
      { materialId: 'material-1', filename: 'first.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:00:00Z' },
      { materialId: 'material-2', filename: 'second.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:01:00Z' },
    ]);
    api.listConcepts.mockResolvedValue([
      { conceptId: 'concept-1', name: 'Mutex', evaluatorId: 'os.mutex.v1', state: 'active', version: 1 },
    ]);
    api.listSources.mockImplementation((materialId: string) => Promise.resolve([
      { locatorId: `${materialId}-locator`, materialVersionId: `${materialId}-version`, contentHash: 'a'.repeat(64), kind: 'text_lines', lineStart: 1, lineEnd: 1, text: `${materialId} source` },
    ]));
    render(<MappingView api={api} />);

    await user.click(await screen.findByRole('checkbox'));
    const confirm = screen.getByRole('button', { name: '确认来源' }) as HTMLButtonElement;
    expect(confirm.disabled).toBe(false);

    await user.selectOptions(screen.getByLabelText('选择材料'), 'material-2');
    await waitFor(() => expect(api.listSources).toHaveBeenLastCalledWith('material-2'));
    expect(confirm.disabled).toBe(true);
  });

  it('restores concept coverage only when its locators are visible for the selected material', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    api.listMaterials.mockResolvedValue([
      { materialId: 'material-1', filename: 'first.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:00:00Z' },
      { materialId: 'material-2', filename: 'second.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:01:00Z' },
    ]);
    api.listConcepts.mockResolvedValue([
      { conceptId: 'concept-1', name: 'Mutex', evaluatorId: 'os.mutex.v1', state: 'active', version: 1 },
      { conceptId: 'concept-2', name: 'Race', evaluatorId: 'os.race.v1', state: 'active', version: 1, coverage: { decision: 'confirmed', locatorIds: ['material-2-locator'], sourceStatus: 'current', version: 1 } },
    ]);
    api.listSources.mockImplementation((materialId: string) => Promise.resolve([
      { locatorId: `${materialId}-locator`, materialVersionId: `${materialId}-version`, contentHash: 'a'.repeat(64), kind: 'text_lines', lineStart: 1, lineEnd: 1, text: `${materialId} source` },
    ]));
    render(<MappingView api={api} />);

    await screen.findByText('material-1 source');
    await user.selectOptions(screen.getByLabelText('选择知识点'), 'concept-2');
    const confirm = screen.getByRole('button', { name: '确认来源' }) as HTMLButtonElement;
    expect(confirm.disabled).toBe(true);

    await user.selectOptions(screen.getByLabelText('选择材料'), 'material-2');
    await screen.findByText('material-2 source');
    expect((screen.getByRole('checkbox') as HTMLInputElement).checked).toBe(true);
    expect(confirm.disabled).toBe(false);
  });

  it('traps delete-dialog focus, closes on Escape, and restores the trigger', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    render(<MappingView api={api} />);

    const trigger = await screen.findByRole('button', { name: '删除 并发讲义.txt' });
    await user.click(trigger);
    const cancel = screen.getByRole('button', { name: '取消' });
    const confirm = screen.getByRole('button', { name: '确认删除' });
    expect(document.activeElement).toBe(cancel);
    await user.tab();
    expect(document.activeElement).toBe(confirm);
    await user.tab();
    expect(document.activeElement).toBe(cancel);
    await user.keyboard('{Escape}');
    expect(screen.queryByRole('dialog')).toBeNull();
    expect(document.activeElement).toBe(trigger);
  });

  it('moves focus to the material selector when confirmed deletion removes its trigger', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    api.listMaterials
      .mockResolvedValueOnce([
        { materialId: 'material-1', filename: '并发讲义.txt', mediaType: 'text/plain', status: 'ready', createdAt: '2026-08-07T09:00:00Z' },
      ])
      .mockResolvedValue([]);
    render(<MappingView api={api} />);

    await user.click(await screen.findByRole('button', { name: '删除 并发讲义.txt' }));
    await user.click(screen.getByRole('button', { name: '确认删除' }));

    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull());
    expect(screen.queryByRole('button', { name: '删除 并发讲义.txt' })).toBeNull();
    expect(document.activeElement).toBe(screen.getByLabelText('选择材料'));
  });

  it('fails closed on malformed source identifiers, hashes, and line ranges', async () => {
    const fetchImpl = vi.fn().mockResolvedValue(new Response(JSON.stringify({
      sources: [{
        locator_id: '', material_version_id: 'version-1', content_hash: 'not-a-hash',
        kind: 'text_lines', line_start: 2, line_end: 1, text: 'source',
      }],
    }), { status: 200, headers: { 'content-type': 'application/json' } }));
    const client = createApiClient({ fetchImpl });

    await expect(client.listSources('material-1')).rejects.toMatchObject({
      code: 'invalid_sources_response',
    });
  });

  it('clears a stale action error after the same delete action succeeds', async () => {
    const user = userEvent.setup();
    const api = createMappingApi();
    api.deleteMaterial
      .mockRejectedValueOnce(new ApiRequestError('delete_failed'))
      .mockResolvedValueOnce({ status: 'deleted', retryable: false });
    render(<MappingView api={api} />);

    await user.click(await screen.findByRole('button', { name: '删除 并发讲义.txt' }));
    await user.click(screen.getByRole('button', { name: '确认删除' }));
    expect((await screen.findByRole('alert')).textContent).toContain('delete_failed');
    await user.click(screen.getByRole('button', { name: '确认删除' }));
    await waitFor(() => expect(screen.queryByRole('alert')).toBeNull());
  });
});
