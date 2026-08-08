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

export interface SourceLocatorSummary {
  locatorId: string;
  materialVersionId: string;
  contentHash: string;
  kind: 'pdf_page' | 'text_lines';
  page?: number;
  lineStart?: number;
  lineEnd?: number;
  text: string;
}

export interface CoverageSummary {
  decision: 'confirmed' | 'rejected';
  locatorIds: string[];
  sourceStatus: 'current' | 'stale';
  version: number;
}

export interface ConceptSummary {
  conceptId: string;
  name: string;
  evaluatorId: string | null;
  state: 'active' | 'explanation_only';
  version: number;
  coverage?: CoverageSummary;
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

function requireNonEmptyString(record: Record<string, unknown>, key: string, errorCode: string): string {
  const value = requireString(record, key, errorCode);
  if (!value.trim()) throw new ApiRequestError(errorCode);
  return value;
}

function requirePositiveInteger(record: Record<string, unknown>, key: string, errorCode: string): number {
  const value = record[key];
  if (!Number.isInteger(value) || Number(value) < 1) throw new ApiRequestError(errorCode);
  return Number(value);
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

function toSource(value: unknown): SourceLocatorSummary {
  const source = requireRecord(value, 'invalid_sources_response');
  const kind = requireString(source, 'kind', 'invalid_sources_response');
  if (kind !== 'pdf_page' && kind !== 'text_lines') throw new ApiRequestError('invalid_sources_response');
  const base = {
    locatorId: requireNonEmptyString(source, 'locator_id', 'invalid_sources_response'),
    materialVersionId: requireNonEmptyString(source, 'material_version_id', 'invalid_sources_response'),
    contentHash: requireNonEmptyString(source, 'content_hash', 'invalid_sources_response'),
    text: requireNonEmptyString(source, 'text', 'invalid_sources_response'),
  };
  if (!/^[0-9a-f]{64}$/.test(base.contentHash)) throw new ApiRequestError('invalid_sources_response');
  if (kind === 'pdf_page') {
    return { ...base, kind: 'pdf_page', page: requirePositiveInteger(source, 'page', 'invalid_sources_response') };
  }
  const lineStart = requirePositiveInteger(source, 'line_start', 'invalid_sources_response');
  const lineEnd = requirePositiveInteger(source, 'line_end', 'invalid_sources_response');
  if (lineEnd < lineStart) throw new ApiRequestError('invalid_sources_response');
  return { ...base, kind: 'text_lines', lineStart, lineEnd };
}

function toConcept(value: unknown): ConceptSummary {
  const concept = requireRecord(value, 'invalid_concepts_response');
  const state = requireString(concept, 'state', 'invalid_concepts_response');
  if (state !== 'active' && state !== 'explanation_only') throw new ApiRequestError('invalid_concepts_response');
  let coverage: CoverageSummary | undefined;
  if (concept.coverage !== null && concept.coverage !== undefined) {
    const raw = requireRecord(concept.coverage, 'invalid_concepts_response');
    const decision = requireString(raw, 'decision', 'invalid_concepts_response');
    const sourceStatus = requireString(raw, 'source_status', 'invalid_concepts_response');
    if (decision !== 'confirmed' && decision !== 'rejected') throw new ApiRequestError('invalid_concepts_response');
    if (sourceStatus !== 'current' && sourceStatus !== 'stale') throw new ApiRequestError('invalid_concepts_response');
    if (!Array.isArray(raw.locator_ids) || raw.locator_ids.some((id) => typeof id !== 'string' || !id)) {
      throw new ApiRequestError('invalid_concepts_response');
    }
    coverage = {
      decision,
      locatorIds: [...raw.locator_ids] as string[],
      sourceStatus,
      version: requirePositiveInteger(raw, 'version', 'invalid_concepts_response'),
    };
  }
  const evaluator = concept.evaluator_id;
  if (evaluator !== null && typeof evaluator !== 'string') throw new ApiRequestError('invalid_concepts_response');
  return {
    conceptId: requireString(concept, 'concept_id', 'invalid_concepts_response'),
    name: requireString(concept, 'name', 'invalid_concepts_response'),
    evaluatorId: evaluator,
    state,
    version: requirePositiveInteger(concept, 'version', 'invalid_concepts_response'),
    coverage,
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
    async listSources(materialId: string): Promise<SourceLocatorSummary[]> {
      const response = await fetchImpl(`/api/materials/${encodeURIComponent(materialId)}/sources`, {
        credentials: 'same-origin', headers: { accept: 'application/json' },
      });
      if (!response.ok) throw await requestError(response, 'sources_unavailable');
      const payload = requireRecord(await response.json(), 'invalid_sources_response');
      if (!Array.isArray(payload.sources)) throw new ApiRequestError('invalid_sources_response');
      return payload.sources.map(toSource);
    },
    async listConcepts(courseId: string): Promise<ConceptSummary[]> {
      const response = await fetchImpl(`/api/courses/${encodeURIComponent(courseId)}/concepts`, {
        credentials: 'same-origin', headers: { accept: 'application/json' },
      });
      if (!response.ok) throw await requestError(response, 'concepts_unavailable');
      const payload = requireRecord(await response.json(), 'invalid_concepts_response');
      if (!Array.isArray(payload.concepts)) throw new ApiRequestError('invalid_concepts_response');
      return payload.concepts.map(toConcept);
    },
    async createConcept(courseId: string, name: string, evaluatorId: string | null): Promise<ConceptSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/courses/${encodeURIComponent(courseId)}/concepts`, {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ name, evaluator_id: evaluatorId }),
      });
      if (!response.ok) throw await requestError(response, 'concept_create_failed');
      return toConcept({ ...(await response.json()), coverage: null });
    },
    async mapConcept(conceptId: string, locatorIds: readonly string[], decision: 'confirmed' | 'rejected') {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/concepts/${encodeURIComponent(conceptId)}/mapping`, {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ locator_ids: locatorIds, decision }),
      });
      if (!response.ok) throw await requestError(response, 'mapping_failed');
      const payload = requireRecord(await response.json(), 'invalid_mapping_response');
      if (payload.decision !== decision) throw new ApiRequestError('invalid_mapping_response');
      return { decision, version: requirePositiveInteger(payload, 'version', 'invalid_mapping_response') };
    },
    async deleteMaterial(materialId: string): Promise<{ status: 'deleted' | 'delete_pending'; retryable: boolean }> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/materials/${encodeURIComponent(materialId)}`, {
        method: 'DELETE', credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      if (!response.ok) throw await requestError(response, 'material_delete_failed');
      const payload = requireRecord(await response.json(), 'invalid_delete_response');
      if (payload.status !== 'deleted' && payload.status !== 'delete_pending') {
        throw new ApiRequestError('invalid_delete_response');
      }
      return { status: payload.status, retryable: payload.retryable === true };
    },
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
