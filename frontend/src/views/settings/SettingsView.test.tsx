// @vitest-environment jsdom
import { cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { SettingsView } from './SettingsView';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('SettingsView', () => {
  it('shows first-run guidance, password semantics, profile caps, privacy, and deletion boundaries', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      if (String(input).includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      return new Response(JSON.stringify({ profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200, headers: { 'content-type': 'application/json' } });
    });
    render(<SettingsView />);
    expect(screen.getByRole('heading', { name: /settings/i })).toBeTruthy();
    expect((await screen.findByLabelText(/provider api key/i)).getAttribute('type')).toBe('password');
    expect(screen.getByRole('heading', { name: /privacy/i })).toBeTruthy();
    expect(screen.getByRole('heading', { name: /local profile/i })).toBeTruthy();
    expect(screen.getByRole('heading', { name: /provider caps/i })).toBeTruthy();
    expect(screen.getByRole('heading', { name: /delete local data/i })).toBeTruthy();
    expect(screen.getByRole('link', { name: /manage material deletion/i }).getAttribute('href')).toBe('/mapping');
    expect(screen.getByRole('heading', { name: /demo restrictions/i })).toBeTruthy();
    expect(screen.queryByText('sk-live-secret')).toBeNull();
    await userEvent.setup().click(screen.getByRole('button', { name: /save provider credential/i }));
    expect(screen.queryByText('sk-live-secret')).toBeNull();
  });

  it('updates and clears without rendering the credential value', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      if (String(input).includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      if (String(input).includes('/api/settings')) return new Response(JSON.stringify({ profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200 });
      if (String(input).includes('/api/credentials/provider')) return new Response(JSON.stringify({ configured: true, updated_at: '2026-08-08T00:00:00Z' }), { status: 200 });
      return new Response('{}', { status: 200 });
    });
    const user = userEvent.setup();
    render(<SettingsView />);
    const input = await screen.findByLabelText(/provider api key/i);
    await user.type(input, 'sk-live-secret');
    await user.click(screen.getByRole('button', { name: /save provider credential/i }));
    expect(fetchMock.mock.calls.some(([, options]) => String((options as RequestInit | undefined)?.body).includes('sk-live-secret'))).toBe(true);
    expect(fetchMock.mock.calls.some(([, options]) => new Headers((options as RequestInit | undefined)?.headers).get('x-csrf-token') === 'test-token')).toBe(true);
    expect(screen.queryByText('sk-live-secret')).toBeNull();
    await user.click(screen.getByRole('button', { name: /clear stored credential/i }));
    const deleteCall = fetchMock.mock.calls.find(([, options]) => (options as RequestInit | undefined)?.method === 'DELETE');
    expect(new Headers((deleteCall?.[1] as RequestInit | undefined)?.headers).get('x-csrf-token')).toBe('test-token');
    expect(screen.queryByText('sk-live-secret')).toBeNull();
  });

  it('fails closed when a credential mutation returns malformed status metadata', async () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, options) => {
      const path = String(input);
      if (path.includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      if (path.includes('/api/settings')) return new Response(JSON.stringify({ profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200 });
      if ((options as RequestInit | undefined)?.method === 'PUT') return new Response(JSON.stringify({ configured: 'yes', updated_at: null }), { status: 200 });
      return new Response(JSON.stringify({ configured: false, updated_at: null }), { status: 200 });
    });
    const user = userEvent.setup();
    render(<SettingsView />);

    await user.type(await screen.findByLabelText(/provider api key/i), 'sk-live-secret');
    await user.click(screen.getByRole('button', { name: /save provider credential/i }));

    expect(await screen.findByText(/credential could not be updated/i)).toBeTruthy();
    expect(screen.getByText(/status: not configured/i)).toBeTruthy();
    expect(screen.queryByText('sk-live-secret')).toBeNull();
  });

  it('keeps credentials unavailable in demo mode without requesting status', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      if (String(input).includes('/api/settings')) return new Response(JSON.stringify({ profile: 'demo', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200 });
      throw new Error('credential endpoint must not be requested in demo mode');
    });
    render(<SettingsView />);

    expect(await screen.findByText(/demo restrictions: credentials/i)).toBeTruthy();
    expect(screen.queryByLabelText(/provider api key/i)).toBeNull();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes('/api/credentials/provider'))).toBe(false);
  });
});
