// @vitest-environment jsdom

import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { App } from './App';
import { createApiClient } from '../api/client';

const initialPath = window.location.pathname;

afterEach(() => {
  cleanup();
  window.history.replaceState({}, '', initialPath);
});

describe('ProjectB workbench shell', () => {
  it('keeps the shell truthful and capability controls closed while profile discovery is pending', () => {
    const api = {
      getCapabilities: vi.fn(() => new Promise<never>(() => undefined)),
    };
    window.history.replaceState({}, '', '/unknown');
    render(<App api={api} />);

    expect(screen.getByText('Checking profile')).toBeTruthy();
    expect(document.querySelector('.course strong')?.textContent).toBe('Course pending');
    expect(screen.queryByText('\u4ec5\u672c\u673a')).toBeNull();
    expect(screen.queryByText('Public demo')).toBeNull();
    expect(document.querySelector('input[type="file"]')).toBeNull();
  });

  it('publishes a truthful public demo shell and removes upload controls from the routed view', async () => {
    const api = {
      getCapabilities: vi.fn().mockResolvedValue({
        profile: 'demo',
        providerMode: 'L',
        providerConfigured: false,
        importEnabled: false,
        credentialManagementEnabled: false,
      }),
    };
    window.history.replaceState({}, '', '/import');
    render(<App api={api} />);

    expect(await screen.findByText('Public demo')).toBeTruthy();
    expect(document.querySelector('.course strong')?.textContent).toBe('Concurrent Systems Demo');
    expect(screen.getByText('Session-isolated synthetic data')).toBeTruthy();
    expect(screen.queryByText('仅本机')).toBeNull();
    expect(document.querySelector('input[type="file"]')).toBeNull();
    expect(api.getCapabilities).toHaveBeenCalledTimes(1);
  });

  it('retains the local-only shell status for the local profile', async () => {
    const api = {
      getCapabilities: vi.fn().mockResolvedValue({
        profile: 'local',
        providerMode: 'L',
        providerConfigured: false,
        importEnabled: true,
        credentialManagementEnabled: true,
      }),
    };
    render(<App api={api} />);

    expect(await screen.findByText('仅本机')).toBeTruthy();
    expect(document.querySelector('.course strong')?.textContent).toBe('操作系统');
    expect(screen.queryByText('Public demo')).toBeNull();
  });

  it('publishes the four learning stages and settings through semantic landmarks', () => {
    render(<App />);

    expect(screen.getByRole('banner')).toBeTruthy();
    expect(screen.getByRole('navigation', { name: '学习流程' })).toBeTruthy();
    expect(screen.getByRole('main')).toBeTruthy();

    const stages = ['导入', '映射', '学习', '复习'];
    expect(
      stages.map((name) => screen.getByRole('link', { name }).getAttribute('href')),
    ).toEqual(['/import', '/mapping', '/learning', '/review']);
    expect(screen.getByRole('link', { name: '设置' }).getAttribute('href')).toBe('/settings');
  });

  it('starts keyboard navigation at the first workflow stage', async () => {
    const user = userEvent.setup();
    render(<App />);

    await user.tab();

    expect(document.activeElement).toBe(screen.getByRole('link', { name: '导入' }));
  });

  it('loads capabilities through the same-origin API boundary without storing state in the browser', async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          profile: 'local',
          bind_host: '127.0.0.1',
          provider_mode: 'L',
          provider_configured: false,
        }),
        { status: 200, headers: { 'content-type': 'application/json' } },
      ),
    );
    const client = createApiClient({ fetchImpl });

    await expect(client.getCapabilities()).resolves.toEqual({
      profile: 'local',
      providerMode: 'L',
      providerConfigured: false,
      importEnabled: true,
      credentialManagementEnabled: true,
    });
    expect(fetchImpl).toHaveBeenCalledWith(
      '/api/settings',
      expect.objectContaining({ credentials: 'same-origin' }),
    );
    expect(window.localStorage.length).toBe(0);
    expect(window.sessionStorage.length).toBe(0);
  });

  it('fails closed when the capability response has an unknown profile', async () => {
    const fetchImpl = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          profile: 'remote',
          bind_host: '0.0.0.0',
          provider_mode: 'L',
          provider_configured: false,
        }),
        { status: 200, headers: { 'content-type': 'application/json' } },
      ),
    );

    await expect(createApiClient({ fetchImpl }).getCapabilities()).rejects.toThrow(
      'invalid_capabilities_response',
    );
  });
});

describe('explicit route states', () => {
  it('renders settings instead of falling through to an unavailable state', () => {
    const pathname = '/settings';
    window.history.pushState({}, '', pathname);
    render(<App />);

    expect(screen.getByRole('heading', { name: /settings/i })).toBeTruthy();
  });

  it('renders not found instead of falling through for an unknown path', () => {
    window.history.pushState({}, '', '/mappingfoo');
    render(<App />);

    expect(screen.getByRole('heading', { name: '\u9875\u9762\u4e0d\u5b58\u5728' })).toBeTruthy();
  });
});
