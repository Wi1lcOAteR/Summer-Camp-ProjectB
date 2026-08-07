import { toCapabilities, type ApiCapabilities } from './capabilities';

export interface ApiClientOptions {
  fetchImpl?: typeof fetch;
}

export interface CourseSummary {
  courseId: string;
  name: string;
  timezone: string;
}

export interface MaterialSummary {
  materialId: string;
  filename: string;
  mediaType: string;
  status: string;
  createdAt: string;
}

export interface MaterialImportResult {
  status: 'imported' | 'idempotent' | 'failed';
  materialId?: string;
  versionId?: string;
  errorCode?: string;
  retryable: boolean;
  contentHash?: string;
}

export interface MaterialImportResponse {
  results: MaterialImportResult[];
}

export class ApiRequestError extends Error {
  constructor(
    public readonly code: string,
    public readonly retryable = false,
  ) {
    super(code);
    this.name = 'ApiRequestError';
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null;
}

async function requestError(response: Response, fallback: string): Promise<ApiRequestError> {
  let payload: unknown;
  try {
    payload = await response.json();
  } catch {
    return new ApiRequestError(fallback);
  }
  const root = isRecord(payload) ? payload : {};
  const nested = isRecord(root.error) ? root.error : isRecord(root.detail) ? root.detail : root;
  const code = typeof nested.code === 'string' ? nested.code : fallback;
  return new ApiRequestError(code, nested.retryable === true);
}

function requireRecord(value: unknown, errorCode: string): Record<string, unknown> {
  if (!isRecord(value)) throw new ApiRequestError(errorCode);
  return value;
}

function requireString(record: Record<string, unknown>, key: string, errorCode: string): string {
  const value = record[key];
  if (typeof value !== 'string') throw new ApiRequestError(errorCode);
  return value;
}

function toCourse(value: unknown): CourseSummary {
  const course = requireRecord(value, 'invalid_courses_response');
  return {
    courseId: requireString(course, 'course_id', 'invalid_courses_response'),
    name: requireString(course, 'name', 'invalid_courses_response'),
    timezone: requireString(course, 'timezone', 'invalid_courses_response'),
  };
}

function toMaterial(value: unknown): MaterialSummary {
  const material = requireRecord(value, 'invalid_materials_response');
  return {
    materialId: requireString(material, 'material_id', 'invalid_materials_response'),
    filename: requireString(material, 'filename', 'invalid_materials_response'),
    mediaType: requireString(material, 'media_type', 'invalid_materials_response'),
    status: requireString(material, 'status', 'invalid_materials_response'),
    createdAt: requireString(material, 'created_at', 'invalid_materials_response'),
  };
}

function toImportResult(value: unknown): MaterialImportResult {
  const result = requireRecord(value, 'invalid_import_response');
  const status = requireString(result, 'status', 'invalid_import_response');
  if (status !== 'imported' && status !== 'idempotent' && status !== 'failed') {
    throw new ApiRequestError('invalid_import_response');
  }
  const errorCode = typeof result.error_code === 'string' ? result.error_code : undefined;
  if ((status === 'failed') !== Boolean(errorCode)) {
    throw new ApiRequestError('invalid_import_response');
  }
  return {
    status,
    materialId: typeof result.material_id === 'string' ? result.material_id : undefined,
    versionId: typeof result.version_id === 'string' ? result.version_id : undefined,
    errorCode,
    retryable: result.retryable === true,
    contentHash: typeof result.content_hash === 'string' ? result.content_hash : undefined,
  };
}

export function createApiClient(options: ApiClientOptions = {}) {
  const fetchImpl = options.fetchImpl ?? fetch;
  async function csrfToken(): Promise<string> {
    const response = await fetchImpl('/api/session', {
      credentials: 'same-origin',
      headers: { accept: 'application/json' },
    });
    if (!response.ok) throw await requestError(response, 'session_unavailable');
    const csrfHeader = response.headers.get('x-csrf-token');
    if (!csrfHeader) throw new ApiRequestError('session_unavailable');
    return csrfHeader;
  }

  return {
    async getCapabilities(): Promise<ApiCapabilities> {
      const response = await fetchImpl('/api/settings', {
        credentials: 'same-origin',
        headers: { accept: 'application/json' },
      });
      if (!response.ok) throw new Error('capabilities_unavailable');
      return toCapabilities(await response.json());
    },
    async listCourses(): Promise<CourseSummary[]> {
      const response = await fetchImpl('/api/courses', {
        credentials: 'same-origin',
        headers: { accept: 'application/json' },
      });
      if (!response.ok) throw await requestError(response, 'courses_unavailable');
      const payload = requireRecord(await response.json(), 'invalid_courses_response');
      if (!Array.isArray(payload.courses)) throw new ApiRequestError('invalid_courses_response');
      return payload.courses.map(toCourse);
    },
    async createCourse(name: string, timezone: string): Promise<CourseSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl('/api/courses', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
          accept: 'application/json',
          'content-type': 'application/json',
          'x-csrf-token': csrfHeader,
        },
        body: JSON.stringify({ name, timezone }),
      });
      if (!response.ok) throw await requestError(response, 'course_create_failed');
      return toCourse(await response.json());
    },
    async listMaterials(courseId: string): Promise<MaterialSummary[]> {
      const response = await fetchImpl(`/api/courses/${encodeURIComponent(courseId)}/materials`, {
        credentials: 'same-origin',
        headers: { accept: 'application/json' },
      });
      if (!response.ok) throw await requestError(response, 'materials_unavailable');
      const payload = requireRecord(await response.json(), 'invalid_materials_response');
      if (!Array.isArray(payload.materials)) throw new ApiRequestError('invalid_materials_response');
      return payload.materials.map(toMaterial);
    },
    async importMaterials(courseId: string, files: readonly File[]): Promise<MaterialImportResponse> {
      const csrfHeader = await csrfToken();
      const body = new FormData();
      for (const file of files) body.append('files', file, file.name);
      const response = await fetchImpl(`/api/courses/${encodeURIComponent(courseId)}/materials/import`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
        body,
      });
      if (!response.ok) throw await requestError(response, 'import_failed');
      const payload = requireRecord(await response.json(), 'invalid_import_response');
      if (!Array.isArray(payload.results)) throw new ApiRequestError('invalid_import_response');
      return { results: payload.results.map(toImportResult) };
    },
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
