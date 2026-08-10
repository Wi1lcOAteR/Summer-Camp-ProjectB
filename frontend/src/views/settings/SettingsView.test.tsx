// @vitest-environment jsdom
import { act, cleanup, render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { SettingsView } from './SettingsView';

afterEach(() => { cleanup(); vi.restoreAllMocks(); });

describe('SettingsView', () => {
  it('does not claim local or provider capabilities while settings are pending', () => {
    vi.spyOn(globalThis, 'fetch').mockImplementation(() => new Promise<Response>(() => undefined));
    render(<SettingsView />);

    expect(screen.getByText('Checking profile capabilities')).toBeTruthy();
    expect(screen.queryByRole('heading', { name: /provider credential/i })).toBeNull();
    expect(screen.queryByRole('heading', { name: /provider caps/i })).toBeNull();
    expect(screen.queryByRole('heading', { name: /local profile/i })).toBeNull();
    expect(screen.queryByText(/course files, profile data, and credentials remain on this device/i)).toBeNull();
  });

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

  it('fails closed for malformed active provider identity and caps', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      if (String(input).includes('/api/settings')) return new Response(JSON.stringify({
        profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L+P', provider_configured: true,
        provider_profile: {
          profile_id: '', adapter_id: 'openai', model_id: 'gpt-5.6-terra',
          input_token_cap: -1, output_token_cap: 3000, max_cost_microusd: 118250,
          config_fingerprint: '', policy_fingerprint: 'not-a-hash',
        },
      }), { status: 200 });
      throw new Error('credential status must not load for malformed settings');
    });
    render(<SettingsView />);

    expect(await screen.findByText('Unavailable / unavailable')).toBeTruthy();
    expect(screen.queryByLabelText(/provider api key/i)).toBeNull();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes('/api/credentials/provider'))).toBe(false);
  });

  it('keeps credentials unavailable in demo mode without requesting status', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input) => {
      if (String(input).includes('/api/settings')) return new Response(JSON.stringify({ profile: 'demo', bind_host: '0.0.0.0', provider_mode: 'L', provider_configured: false }), { status: 200 });
      throw new Error('credential endpoint must not be requested in demo mode');
    });
    render(<SettingsView />);

    expect(await screen.findByText(/demo restrictions: credentials/i)).toBeTruthy();
    expect(screen.getByText('Demo / 0.0.0.0')).toBeTruthy();
    expect(screen.getByRole('heading', { name: /demo profile/i })).toBeTruthy();
    expect(screen.getByText(/synthetic fixtures and changes are isolated to this browser session/i)).toBeTruthy();
    expect(screen.queryByRole('heading', { name: /local profile/i })).toBeNull();
    expect(screen.queryByText(/network calls require explicit consent/i)).toBeNull();
    expect(screen.queryByText(/course files, profile data, and credentials remain on this device/i)).toBeNull();
    expect(screen.queryByLabelText(/provider api key/i)).toBeNull();
    expect(fetchMock.mock.calls.some(([input]) => String(input).includes('/api/credentials/provider'))).toBe(false);
  });

  it('explicitly enables a reviewed model and disables the active provider profile', async () => {
    let enabled = false;
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, options) => {
      const path = String(input);
      const method = (options as RequestInit | undefined)?.method ?? 'GET';
      if (path.includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      if (path.includes('/api/credentials/provider')) return new Response(JSON.stringify({ configured: true, updated_at: null }), { status: 200 });
      if (path.includes('/api/settings/provider') && method === 'POST') {
        enabled = true;
      } else if (path.includes('/api/settings/provider') && method === 'DELETE') {
        enabled = false;
      }
      if (path.includes('/api/settings')) return new Response(JSON.stringify({
        profile: 'local', bind_host: '127.0.0.1', provider_mode: enabled ? 'L+P' : 'L', provider_configured: true,
        provider_profile: enabled ? {
          profile_id: 'openai-profile', adapter_id: 'openai', model_id: 'gpt-5.6-terra',
          input_token_cap: 20000, output_token_cap: 3000, max_cost_microusd: 118250,
          config_fingerprint: 'b'.repeat(64), policy_fingerprint: 'c'.repeat(64),
        } : null,
      }), { status: 200 });
      return new Response('{}', { status: 404 });
    });
    const user = userEvent.setup();
    render(<SettingsView />);

    await screen.findByText(/status: configured/i);
    await user.selectOptions(screen.getByLabelText(/openai model/i), 'gpt-5.6-terra');
    await user.click(screen.getByRole('button', { name: /enable p provider/i }));
    expect(await screen.findByText(/USD 0.11825/)).toBeTruthy();
    expect(screen.getByText(/20,000 input/)).toBeTruthy();
    expect(screen.getByText(/3,000 output/)).toBeTruthy();
    const enableCall = fetchMock.mock.calls.find(([input, options]) => String(input).includes('/api/settings/provider') && (options as RequestInit | undefined)?.method === 'POST');
    expect(JSON.parse(String((enableCall?.[1] as RequestInit).body))).toEqual({ model_id: 'gpt-5.6-terra' });

    await user.click(screen.getByRole('button', { name: /disable p provider/i }));
    expect(await screen.findByText(/provider mode is L;/i)).toBeTruthy();
  });

  it('does not let the initial credential read overwrite a later successful save', async () => {
    let resolveInitialStatus: ((response: Response) => void) | undefined;
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, options) => {
      const path = String(input);
      const method = (options as RequestInit | undefined)?.method ?? 'GET';
      if (path.includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      if (path.includes('/api/settings')) return new Response(JSON.stringify({ profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200 });
      if (path.includes('/api/credentials/provider') && method === 'GET') {
        return new Promise<Response>((resolve) => { resolveInitialStatus = resolve; });
      }
      if (path.includes('/api/credentials/provider') && method === 'PUT') {
        return new Response(JSON.stringify({ configured: true, updated_at: '2026-08-09T00:00:00Z' }), { status: 200 });
      }
      return new Response('{}', { status: 404 });
    });
    const user = userEvent.setup();
    render(<SettingsView />);

    await user.type(await screen.findByLabelText(/provider api key/i), 'unit-test-secret');
    await user.click(screen.getByRole('button', { name: /save provider credential/i }));
    expect(await screen.findByText(/status: configured/i)).toBeTruthy();
    await act(async () => {
      resolveInitialStatus?.(new Response(JSON.stringify({ configured: false, updated_at: null }), { status: 200 }));
      await Promise.resolve();
    });

    expect(screen.getByText(/status: configured/i)).toBeTruthy();
    expect((screen.getByRole('button', { name: /enable p provider/i }) as HTMLButtonElement).disabled).toBe(false);
  });

  it('serializes credential and provider mutations while a save is pending', async () => {
    let resolveSave: ((response: Response) => void) | undefined;
    vi.spyOn(globalThis, 'fetch').mockImplementation(async (input, options) => {
      const path = String(input);
      const method = (options as RequestInit | undefined)?.method ?? 'GET';
      if (path.includes('/api/session')) return new Response('{}', { status: 200, headers: { 'x-csrf-token': 'test-token' } });
      if (path.includes('/api/settings')) return new Response(JSON.stringify({ profile: 'local', bind_host: '127.0.0.1', provider_mode: 'L', provider_configured: false }), { status: 200 });
      if (path.includes('/api/credentials/provider') && method === 'GET') return new Response(JSON.stringify({ configured: false, updated_at: null }), { status: 200 });
      if (path.includes('/api/credentials/provider') && method === 'PUT') {
        return new Promise<Response>((resolve) => { resolveSave = resolve; });
      }
      return new Response('{}', { status: 404 });
    });
    const user = userEvent.setup();
    render(<SettingsView />);

    await user.type(await screen.findByLabelText(/provider api key/i), 'unit-test-secret');
    await user.click(screen.getByRole('button', { name: /save provider credential/i }));

    expect((screen.getByRole('button', { name: /save provider credential/i }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole('button', { name: /enable p provider/i }) as HTMLButtonElement).disabled).toBe(true);
    await act(async () => {
      resolveSave?.(new Response(JSON.stringify({ configured: true, updated_at: null }), { status: 200 }));
      await Promise.resolve();
    });
    expect((screen.getByRole('button', { name: /save provider credential/i }) as HTMLButtonElement).disabled).toBe(false);
  });
});
