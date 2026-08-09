import { Check, KeyRound, ShieldCheck, Trash2 } from 'lucide-react';
import { useEffect, useState } from 'react';
import styles from './SettingsView.module.css';

type Profile = 'local' | 'demo' | 'unavailable';

interface SettingsState {
  profile: Profile;
  bind_host: string;
  provider_mode: 'L' | 'L+P';
  provider_configured: boolean;
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
  ) {
    throw new Error('invalid_settings_response');
  }
  return {
    profile: value.profile,
    bind_host: bindHost,
    provider_mode: value.provider_mode,
    provider_configured: value.provider_configured,
  };
}

export function SettingsView() {
  const [settings, setSettings] = useState<SettingsState | null>(null);
  const [credential, setCredential] = useState<CredentialState>({ configured: false, updated_at: null });
  const [secret, setSecret] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    let active = true;

    async function load() {
      let profile: SettingsState;
      try {
        profile = await settingsState(await fetch('/api/settings', {
          credentials: 'same-origin',
          headers: { accept: 'application/json' },
        }));
        if (!active) return;
        setSettings(profile);
      } catch {
        if (active) setSettings(unavailable);
        return;
      }

      if (!active || profile.profile !== 'local') return;
      try {
        const status = await credentialState(await fetch('/api/credentials/provider', {
          credentials: 'same-origin',
          headers: { accept: 'application/json' },
        }));
        if (active) setCredential(status);
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
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/credentials/provider', {
        method: 'PUT',
        credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ value: secret }),
      });
      setCredential(await credentialState(response, true));
      setMessage('Credential status updated. The value was not displayed.');
    } catch {
      setMessage('Credential could not be updated.');
    }
    setSecret('');
  }

  async function clearCredential() {
    try {
      const csrfHeader = await csrfToken();
      const response = await fetch('/api/credentials/provider', {
        method: 'DELETE',
        credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      setCredential(await credentialState(response, false));
      setMessage('Stored credential cleared.');
    } catch {
      setMessage('Credential could not be cleared.');
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
                      <button type="button" className={styles.primaryButton} onClick={saveCredential}>Save provider credential</button>
                      <button type="button" className={styles.secondaryButton} onClick={clearCredential} disabled={!credential.configured}>Clear stored credential</button>
                    </div>
                    <p className={styles.muted} role="status">Status: {credential.configured ? 'configured' : 'not configured'}{credential.updated_at ? ' / updated recently' : ''}. Secret values are never shown.</p>
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
          {isLocal && <section className={styles.section} aria-labelledby="caps-title"><div className={styles.heading}><h2 id="caps-title">Provider caps</h2></div><ul className={styles.list}><li>Local deterministic explanations</li><li>Maximum context is source-bound</li><li>No background network requests</li></ul></section>}
          <section className={styles.section} aria-labelledby="security-title"><div className={styles.heading}><h2 id="security-title">Data &amp; security</h2></div><p className={styles.muted}>{isDemo ? 'Requests are bound to an isolated session and protected by same-origin checks.' : isLocal ? 'Passwords use a hidden input. API responses contain status metadata only, never secret material.' : 'Security metadata is unavailable without a confirmed profile.'}</p></section>
          {isLocal && <section className={styles.section} aria-labelledby="demo-title"><div className={styles.heading}><h2 id="demo-title">Demo restrictions</h2></div><p className={styles.muted}>Demo mode uses synthetic data and disables uploads, credentials, external providers, and cross-session state.</p></section>}
        </aside>
      </div>
    </div>
  );
}
