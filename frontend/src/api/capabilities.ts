export interface ApiCapabilities {
  profile: 'local' | 'demo';
  providerMode: 'L' | 'L+P';
  providerConfigured: boolean;
  importEnabled: boolean;
  credentialManagementEnabled: boolean;
}

export interface SettingsResponse {
  profile: 'local' | 'demo';
  bind_host: string;
  provider_mode: 'L' | 'L+P';
  provider_configured: boolean;
}

export function toCapabilities(value: unknown): ApiCapabilities {
  if (!isSettingsResponse(value)) throw new Error('invalid_capabilities_response');
  const profile = value.profile;
  return {
    profile,
    providerMode: value.provider_mode,
    providerConfigured: value.provider_configured,
    importEnabled: profile === 'local',
    credentialManagementEnabled: profile === 'local',
  };
}

function isSettingsResponse(value: unknown): value is SettingsResponse {
  if (typeof value !== 'object' || value === null) return false;
  const candidate = value as Record<string, unknown>;
  if (candidate.profile !== 'local' && candidate.profile !== 'demo') return false;
  if (candidate.provider_mode !== 'L' && candidate.provider_mode !== 'L+P') return false;
  if (typeof candidate.provider_configured !== 'boolean') return false;
  if (typeof candidate.bind_host !== 'string') return false;
  return candidate.profile !== 'local' || candidate.bind_host === '127.0.0.1';
}
