import { Check, KeyRound, ShieldCheck, Trash2 } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import styles from './SettingsView.module.css';

type Profile = 'local' | 'demo' | 'unavailable';

interface SettingsState {
  profile: Profile;
  bind_host: string;
  provider_mode: 'L' | 'L+P';
  provider_configured: boolean;
  provider_profile: ProviderProfileState | null;
}

interface ProviderProfileState {
  profile_id: string;
  adapter_id: 'openai';
  model_id: 'gpt-5.6-terra' | 'gpt-5.6-luna';
  input_token_cap: number;
  output_token_cap: number;
  max_cost_microusd: number;
  config_fingerprint: string;
  policy_fingerprint: string;
}

interface CredentialState {
  configured: boolean;
  updated_at: string | null;
}

const unavailable: SettingsState = {
  profile: 'unavailable',
  bind_host: 'unavailable',
  provider_mode: 'L',
  provider_configured: false,
  provider_profile: null,
};

async function csrfToken(): Promise<string> {
  const response = await fetch('/api/session', {
    credentials: 'same-origin',
    headers: { accept: 'application/json' },
  });
  const csrfHeader = response.headers.get('x-csrf-token');
  if (!response.ok || !csrfHeader) throw new Error('session_unavailable');
  return csrfHeader;
}

async function credentialState(response: Response, expected?: boolean): Promise<CredentialState> {
  if (!response.ok) throw new Error('credential_request_failed');
  const value = await response.json() as Record<string, unknown>;
  if (typeof value.configured !== 'boolean' || (value.updated_at !== null && typeof value.updated_at !== 'string')) {
    throw new Error('invalid_credential_response');
  }
  if (expected !== undefined && value.configured !== expected) throw new Error('invalid_credential_response');
  return { configured: value.configured, updated_at: value.updated_at as string | null };
}

async function settingsState(response: Response): Promise<SettingsState> {
  if (!response.ok) throw new Error('settings_unavailable');
  const value = await response.json() as Record<string, unknown>;
  const bindHost = typeof value.bind_host === 'string' ? value.bind_host : '';
  const validBindHost = value.profile === 'local'
    ? bindHost === '127.0.0.1'
    : value.profile === 'demo' && bindHost === '0.0.0.0';
  if (
    (value.profile !== 'local' && value.profile !== 'demo')
    || !validBindHost
    || (value.provider_mode !== 'L' && value.provider_mode !== 'L+P')
    || typeof value.provider_configured !== 'boolean'
    || (value.provider_mode === 'L+P' && (value.profile !== 'local' || value.provider_configured !== true))
    || (value.provider_mode === 'L' && value.provider_profile != null)
  ) {
    throw new Error('invalid_settings_response');
  }
  let providerProfile: ProviderProfileState | null = null;
  if (value.provider_mode === 'L+P') {
    const profile = value.provider_profile as Record<string, unknown> | null;
    if (!profile || profile.adapter_id !== 'openai'
      || (profile.model_id !== 'gpt-5.6-terra' && profile.model_id !== 'gpt-5.6-luna')
      || typeof profile.profile_id !== 'string' || !profile.profile_id.trim()
      || !Number.isInteger(profile.input_token_cap) || Number(profile.input_token_cap) <= 0
      || !Number.isInteger(profile.output_token_cap) || Number(profile.output_token_cap) <= 0
      || !Number.isInteger(profile.max_cost_microusd) || Number(profile.max_cost_microusd) <= 0
      || typeof profile.config_fingerprint !== 'string' || !/^[0-9a-f]{64}$/.test(profile.config_fingerprint)
      || typeof profile.policy_fingerprint !== 'string' || !/^[0-9a-f]{64}$/.test(profile.policy_fingerprint)) {
      throw new Error('invalid_settings_response');
    }
    providerProfile = profile as unknown as ProviderProfileState;
  }
  return {
    profile: value.profile,
    bind_host: bindHost,
    provider_mode: value.provider_mode,
    provider_configured: value.provider_configured,
    provider_profile: providerProfile,
  };
}

export function SettingsView() {
  const [settings, setSettings] = useState<SettingsState | null>(null);
  const [credential, setCredential] = useState<CredentialState>({ configured: false, updated_at: null });
  const [secret, setSecret] = useState('');
  const [message, setMessage] = useState('');
  const [modelId, setModelId] = useState<'gpt-5.6-terra' | 'gpt-5.6-luna'>('gpt-5.6-terra');
  const [mutationPending, setMutationPending] = useState(false);
  const mutationPendingRef = useRef(false);
  const settingsRequestId = useRef(0);
  const credentialRequestId = useRef(0);

  function beginMutation(): boolean {
    if (mutationPendingRef.current) return false;
    mutationPendingRef.current = true;
    setMutationPending(true);
    return true;
  }

  function endMutation() {
    mutationPendingRef.current = false;
    setMutationPending(false);
  }

  useEffect(() => {
    let active = true;

    async function load() {
      const settingsId = ++settingsRequestId.current;
      let profile: SettingsState;
      try {
        profile = await settingsState(await fetch('/api/settings', {
          credentials: 'same-origin',
          headers: { accept: 'application/json' },
        }));
        if (!active || settingsId !== settingsRequestId.current) return;
        setSettings(profile);
      } catch {
        if (active && settingsId === settingsRequestId.current) setSettings(unavailable);
        return;
      }

      if (!active || profile.profile !== 'local') return;
      const credentialId = ++credentialRequestId.current;
      try {
        const status = await credentialState(await fetch('/api/credentials/provider', {
          credentials: 'same-origin',
          headers: { accept: 'application/json' },
        }));
        if (active && credentialId === credentialRequestId.current) setCredential(status);
      } catch {
        // The local profile remains usable; an unavailable status is unconfigured.
      }
    }

    void load();
    return () => { active = false; };
  }, []);

  async function saveCredential() {
    if (!secret.trim()) {
      setMessage('Enter a credential before saving.');
      return;
    }
    if (!beginMutation()) return;
    const credentialId = ++credentialRequestId.current;
    const submittedSecret = secret;
    setSecret('');
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/credentials/provider', {
        method: 'PUT',
        credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ value: submittedSecret }),
      });
      const nextCredential = await credentialState(response, true);
      if (credentialId === credentialRequestId.current) {
        setCredential(nextCredential);
        setMessage('Credential status updated. The value was not displayed.');
      }
    } catch {
      if (credentialId === credentialRequestId.current) setMessage('Credential could not be updated.');
    } finally {
      endMutation();
    }
  }

  async function clearCredential() {
    if (!beginMutation()) return;
    const credentialId = ++credentialRequestId.current;
    const settingsId = ++settingsRequestId.current;
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/credentials/provider', {
        method: 'DELETE',
        credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      const nextCredential = await credentialState(response, false);
      if (credentialId === credentialRequestId.current) setCredential(nextCredential);
      if (settingsId === settingsRequestId.current) {
        setSettings((current) => current ? { ...current, provider_mode: 'L', provider_profile: null, provider_configured: false } : current);
      }
      setMessage('Stored credential cleared.');
    } catch {
      setMessage('Credential could not be cleared.');
    } finally {
      endMutation();
    }
  }

  async function enableProvider() {
    if (!beginMutation()) return;
    const settingsId = ++settingsRequestId.current;
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/settings/provider', {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ model_id: modelId }),
      });
      const nextSettings = await settingsState(response);
      if (settingsId === settingsRequestId.current) {
        setSettings(nextSettings);
        setMessage('P provider enabled. Each request still requires exact consent.');
      }
    } catch {
      if (settingsId === settingsRequestId.current) setMessage('P provider could not be enabled.');
    } finally {
      endMutation();
    }
  }

  async function disableProvider() {
    if (!beginMutation()) return;
    const settingsId = ++settingsRequestId.current;
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/settings/provider', {
        method: 'DELETE', credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      const nextSettings = await settingsState(response);
      if (settingsId === settingsRequestId.current) {
        setSettings(nextSettings);
        setMessage('P provider disabled.');
      }
    } catch {
      if (settingsId === settingsRequestId.current) setMessage('P provider could not be disabled.');
    } finally {
      endMutation();
    }
  }

  const profileLabel = settings === null
    ? 'Checking profile capabilities'
    : settings.profile === 'demo'
      ? 'Demo'
      : settings.profile === 'local'
        ? 'Local'
        : 'Unavailable';
  const isDemo = settings?.profile === 'demo';
  const isLocal = settings?.profile === 'local';

  return (
    <div className={styles.view}>
      <section className="pageIntro" aria-labelledby="settings-title">
        <div>
          <p className="eyebrow">{isDemo ? 'Utility / Public demo' : isLocal ? 'Utility / Local configuration' : 'Utility / Profile'}</p>
          <h1 id="settings-title">Settings</h1>
          <p className="introCopy">{isDemo ? 'Review public demo isolation and session lifecycle.' : isLocal ? 'Control local access, provider credentials, privacy, and data lifecycle.' : 'Review profile capabilities and data lifecycle.'}</p>
        </div>
        <p className={styles.status}><span>Profile</span><strong>{profileLabel}{settings ? ` / ${settings.bind_host}` : ''}</strong></p>
      </section>
      {message && <p className={styles.message} role="status"><Check size={16} aria-hidden="true" />{message}</p>}
      <div className={styles.layout}>
        <div className={styles.primary}>
          <section className={styles.section} aria-labelledby="credential-title">
            <div className={styles.heading}>
              <div><h2 id="credential-title">{isDemo ? 'Demo restrictions' : isLocal ? 'Provider credential' : 'Profile capabilities'}</h2><p>{isDemo ? 'This profile has no credential or upload capability.' : isLocal ? 'First run keeps the value hidden and stores it locally.' : 'Capabilities remain unavailable until the profile is confirmed.'}</p></div>
              <KeyRound size={20} aria-hidden="true" />
            </div>
            {settings === null ? <p className={styles.notice} role="status">Checking profile capabilities.</p>
              : settings.profile === 'demo' ? <p className={styles.notice}>Demo restrictions: credentials, uploads, and outbound provider calls are unavailable.</p>
                : settings.profile === 'unavailable' ? <p className={styles.notice} role="alert">Settings are unavailable. Credentials remain disabled.</p>
                  : <>
                    <label className={styles.field}>Provider API key<input aria-label="Provider API key" type="password" autoComplete="new-password" value={secret} onChange={(event) => setSecret(event.target.value)} /></label>
                    <div className={styles.actions}>
                      <button type="button" className={styles.primaryButton} onClick={saveCredential} disabled={mutationPending}>Save provider credential</button>
                      <button type="button" className={styles.secondaryButton} onClick={clearCredential} disabled={!credential.configured || mutationPending}>Clear stored credential</button>
                    </div>
                    <p className={styles.muted} role="status">Status: {credential.configured ? 'configured' : 'not configured'}{credential.updated_at ? ' / updated recently' : ''}. Secret values are never shown.</p>
                    <label className={styles.field}>OpenAI model<select aria-label="OpenAI model" value={modelId} disabled={mutationPending} onChange={(event) => setModelId(event.target.value as typeof modelId)}><option value="gpt-5.6-terra">gpt-5.6-terra</option><option value="gpt-5.6-luna">gpt-5.6-luna</option></select></label>
                    <div className={styles.actions}><button type="button" className={styles.primaryButton} onClick={enableProvider} disabled={!credential.configured || mutationPending}>Enable P provider</button><button type="button" className={styles.secondaryButton} onClick={disableProvider} disabled={settings.provider_mode !== 'L+P' || mutationPending}>Disable P provider</button></div>
                  </>}
          </section>
          <section className={styles.section} aria-labelledby="privacy-title">
            <div className={styles.heading}><div><h2 id="privacy-title">Privacy</h2><p>{isDemo ? 'Ephemeral controls for public demo data.' : isLocal ? 'Local-first controls for your learning data.' : 'Privacy capabilities are not yet available.'}</p></div><ShieldCheck size={20} aria-hidden="true" /></div>
            {isDemo
              ? <ul className={styles.list}><li>Synthetic fixtures and changes are isolated to this browser session.</li><li>Idle sessions expire after 30 minutes and all sessions expire after 2 hours.</li><li>Uploads, credentials, and outbound calls are unavailable.</li></ul>
              : isLocal
                ? <ul className={styles.list}><li>Course files, profile data, and credentials remain on this device.</li><li>Provider mode is {settings.provider_mode}; network calls require explicit consent.</li><li>Only source-bound, minimum data may leave the local profile.</li></ul>
                : <p className={styles.notice}>No privacy capability is enabled without a confirmed profile.</p>}
          </section>
          <section className={styles.section} aria-labelledby="deletion-title">
            <div className={styles.heading}><div><h2 id="deletion-title">{isDemo ? 'Session data lifecycle' : isLocal ? 'Delete local data' : 'Data lifecycle'}</h2><p>{isDemo ? 'Session data is removed automatically at expiry.' : isLocal ? 'Materials are deleted individually so shared content remains protected.' : 'Data controls are unavailable without a confirmed profile.'}</p></div><Trash2 size={20} aria-hidden="true" /></div>
            {(isDemo || isLocal) && <a className={styles.dangerLink} href="/mapping">{isDemo ? 'Manage session materials' : 'Manage material deletion'}</a>}
          </section>
        </div>
        <aside className={styles.aside}>
          <section className={styles.section} aria-labelledby="profile-title"><div className={styles.heading}><h2 id="profile-title">{isDemo ? 'Demo profile' : isLocal ? 'Local profile' : 'Profile'}</h2></div><dl className={styles.settings}><div><dt>Bind host</dt><dd>{settings?.bind_host ?? 'checking'}</dd></div><div><dt>Provider mode</dt><dd>{settings?.provider_mode ?? 'checking'}</dd></div><div><dt>Credential</dt><dd>{isDemo || !isLocal ? 'Unavailable' : credential.configured ? 'Configured' : 'Not configured'}</dd></div></dl></section>
          {isLocal && <section className={styles.section} aria-labelledby="caps-title"><div className={styles.heading}><h2 id="caps-title">Provider caps</h2></div>{settings.provider_profile ? <ul className={styles.list}><li>{settings.provider_profile.model_id}</li><li>{settings.provider_profile.input_token_cap.toLocaleString('en-US')} input tokens</li><li>{settings.provider_profile.output_token_cap.toLocaleString('en-US')} output tokens</li><li>USD {(settings.provider_profile.max_cost_microusd / 1_000_000).toFixed(5)} maximum</li></ul> : <ul className={styles.list}><li>P provider disabled</li><li>Choose only a reviewed OpenAI model</li><li>No background network requests</li></ul>}</section>}
          <section className={styles.section} aria-labelledby="security-title"><div className={styles.heading}><h2 id="security-title">Data &amp; security</h2></div><p className={styles.muted}>{isDemo ? 'Requests are bound to an isolated session and protected by same-origin checks.' : isLocal ? 'Passwords use a hidden input. API responses contain status metadata only, never secret material.' : 'Security metadata is unavailable without a confirmed profile.'}</p></section>
          {isLocal && <section className={styles.section} aria-labelledby="demo-title"><div className={styles.heading}><h2 id="demo-title">Demo restrictions</h2></div><p className={styles.muted}>Demo mode uses synthetic data and disables uploads, credentials, external providers, and cross-session state.</p></section>}
        </aside>
      </div>
    </div>
  );
}
