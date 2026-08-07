// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { createApiClient } from '../../api/client';
import { ImportView } from './ImportView';

afterEach(cleanup);

function createImportApi(overrides: Record<string, unknown> = {}) {
  return {
    listCourses: vi.fn().mockResolvedValue([
      { courseId: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' },
    ]),
    createCourse: vi.fn().mockResolvedValue(
      { courseId: 'course-1', name: '操作系统', timezone: 'Asia/Shanghai' },
    ),
    listMaterials: vi.fn().mockResolvedValue([
      {
        materialId: 'material-1',
        filename: '并发讲义.pdf',
        mediaType: 'application/pdf',
        status: 'ready',
        createdAt: '2026-08-07T09:00:00Z',
      },
    ]),
    importMaterials: vi.fn().mockResolvedValue({
      results: [
        {
          filename: '互斥笔记.md',
          status: 'imported',
          materialId: 'material-2',
          retryable: false,
        },
      ],
    }),
    ...overrides,
  };
}

describe('ImportView', () => {
  it('loads the current course materials and imports selected v1 files', async () => {
    const user = userEvent.setup();
    const api = createImportApi();
    render(<ImportView api={api} />);

    expect(await screen.findByText('并发讲义.pdf')).toBeTruthy();
    expect(screen.getByText(/最多 5 个文件/)).toBeTruthy();
    expect(screen.getByText(/仅支持含可提取文字的数字 PDF、TXT 或 Markdown/)).toBeTruthy();

    const file = new File(['# 互斥'], '互斥笔记.md', { type: 'text/markdown' });
    await user.upload(screen.getByLabelText('选择材料文件'), file);

    expect(screen.getByText('互斥笔记.md')).toBeTruthy();
    await user.click(screen.getByRole('button', { name: '开始导入' }));

    expect(await screen.findByText('已成功导入 1 个文件')).toBeTruthy();
    expect(api.importMaterials).toHaveBeenCalledWith('course-1', [file]);
    expect(api.listMaterials).toHaveBeenCalledTimes(2);
  });

  it('keeps a failed file selected and exposes a retryable import error', async () => {
    const user = userEvent.setup();
    const api = createImportApi({
      importMaterials: vi.fn().mockRejectedValue(
        Object.assign(new Error('file_too_large'), {
          code: 'file_too_large',
          retryable: true,
        }),
      ),
    });
    render(<ImportView api={api} />);

    await screen.findByText('并发讲义.pdf');
    const file = new File(['too large'], '超限.txt', { type: 'text/plain' });
    await user.upload(screen.getByLabelText('选择材料文件'), file);
    await user.click(screen.getByRole('button', { name: '开始导入' }));

    const error = await screen.findByRole('alert');
    expect(error.textContent).toContain('导入失败');
    expect(error.textContent).toContain('文件超过 20 MiB 限制');
    expect(error.textContent).toContain('可以重试');
    expect(screen.getByText('超限.txt')).toBeTruthy();
    expect(screen.getByRole('button', { name: '开始导入' })).toBeTruthy();
  });

  it('rejects an unknown per-file status instead of displaying it as success', async () => {
    const fetchImpl = vi.fn<typeof fetch>()
      .mockResolvedValueOnce(new Response('{"status":"ready"}', {
        status: 200,
        headers: { 'x-csrf-token': 'test-token' },
      }))
      .mockResolvedValueOnce(new Response('{"results":[{"status":"mystery","retryable":false}]}', {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }));
    const client = createApiClient({ fetchImpl });

    await expect(client.importMaterials('course-1', [new File(['x'], 'notes.txt')]))
      .rejects.toThrow('invalid_import_response');
  });
});
