import { toCapabilities, type ApiCapabilities } from './capabilities';

export interface ApiClientOptions {
  fetchImpl?: typeof fetch;
}

export function createApiClient(options: ApiClientOptions = {}) {
  const fetchImpl = options.fetchImpl ?? fetch;
  return {
    async getCapabilities(): Promise<ApiCapabilities> {
      const response = await fetchImpl('/api/settings', {
        credentials: 'same-origin',
        headers: { accept: 'application/json' },
      });
      if (!response.ok) throw new Error('capabilities_unavailable');
      return toCapabilities(await response.json());
    },
  };
}
