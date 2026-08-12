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

export type ReviewTaskStatus = 'pending' | 'skipped' | 'completed';

export interface ReviewTaskSummary {
  taskId: string;
  revisionId: string;
  conceptId: string;
  dueLocalDate: string;
  durationMinutes: number;
  status: ReviewTaskStatus;
  sourceRefs: string[];
  evidenceRefs: string[];
  completedAt: string | null;
  createdAt: string;
}

export interface ReviewRevisionSummary {
  revisionId: string;
  courseId: string;
  inputHash: string;
  parentRevisionId: string | null;
  createdAt: string;
  tasks: ReviewTaskSummary[];
  diff: { added: string[]; removed: string[]; changed: string[]; retained: string[] };
}

export interface ProviderProfileSummary {
  profileId: string;
  adapterId: 'openai';
  modelId: 'gpt-5.6-terra' | 'gpt-5.6-luna';
  inputTokenCap: number;
  outputTokenCap: number;
  maxCostMicrousd: number;
  configFingerprint: string;
  policyFingerprint: string;
}

export interface ProviderSettingsSummary {
  providerMode: 'L' | 'L+P';
  providerProfile: ProviderProfileSummary | null;
}

export interface ProviderPreviewSummary {
  previewId: string;
  operation: 'generate_explanation';
  profileId: string;
  adapterId: 'openai';
  modelId: string;
  inputTokenCap: number;
  outputTokenCap: number;
  maxCostMicrousd: number;
  configFingerprint: string;
  policyFingerprint: string;
  sources: ProviderPreviewSourceSummary[];
}

export interface ProviderPreviewSourceSummary {
  locatorId: string;
  materialVersionId: string;
  contentHash: string;
  text: string;
}

export interface ProviderCandidateSummary {
  text: string;
  authoritative: false;
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

function toProviderProfile(value: unknown): ProviderProfileSummary {
  const profile = requireRecord(value, 'invalid_provider_settings');
  const adapterId = requireString(profile, 'adapter_id', 'invalid_provider_settings');
  const modelId = requireString(profile, 'model_id', 'invalid_provider_settings');
  if (adapterId !== 'openai' || (modelId !== 'gpt-5.6-terra' && modelId !== 'gpt-5.6-luna')) {
    throw new ApiRequestError('invalid_provider_settings');
  }
  return {
    profileId: requireNonEmptyString(profile, 'profile_id', 'invalid_provider_settings'),
    adapterId,
    modelId,
    inputTokenCap: requirePositiveInteger(profile, 'input_token_cap', 'invalid_provider_settings'),
    outputTokenCap: requirePositiveInteger(profile, 'output_token_cap', 'invalid_provider_settings'),
    maxCostMicrousd: requirePositiveInteger(profile, 'max_cost_microusd', 'invalid_provider_settings'),
    configFingerprint: requireNonEmptyString(profile, 'config_fingerprint', 'invalid_provider_settings'),
    policyFingerprint: requireNonEmptyString(profile, 'policy_fingerprint', 'invalid_provider_settings'),
  };
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

function toProviderPreviewSource(value: unknown): ProviderPreviewSourceSummary {
  const source = requireRecord(value, 'invalid_provider_preview');
  const contentHash = requireNonEmptyString(source, 'content_hash', 'invalid_provider_preview');
  if (!/^[0-9a-f]{64}$/.test(contentHash)) throw new ApiRequestError('invalid_provider_preview');
  return {
    locatorId: requireNonEmptyString(source, 'locator_id', 'invalid_provider_preview'),
    materialVersionId: requireNonEmptyString(source, 'material_version_id', 'invalid_provider_preview'),
    contentHash,
    text: requireNonEmptyString(source, 'text', 'invalid_provider_preview'),
  };
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

function requireStringArray(record: Record<string, unknown>, key: string, errorCode: string): string[] {
  const value = record[key];
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string' || !item)) {
    throw new ApiRequestError(errorCode);
  }
  return [...value];
}

function toReviewTask(value: unknown): ReviewTaskSummary {
  const task = requireRecord(value, 'invalid_review_response');
  const status = requireString(task, 'status', 'invalid_review_response');
  if (status !== 'pending' && status !== 'skipped' && status !== 'completed') {
    throw new ApiRequestError('invalid_review_response');
  }
  const completedAt = task.completed_at;
  if (completedAt !== null && typeof completedAt !== 'string') throw new ApiRequestError('invalid_review_response');
  return {
    taskId: requireNonEmptyString(task, 'task_id', 'invalid_review_response'),
    revisionId: requireNonEmptyString(task, 'revision_id', 'invalid_review_response'),
    conceptId: requireNonEmptyString(task, 'concept_id', 'invalid_review_response'),
    dueLocalDate: requireNonEmptyString(task, 'due_local_date', 'invalid_review_response'),
    durationMinutes: requirePositiveInteger(task, 'duration_minutes', 'invalid_review_response'),
    status,
    sourceRefs: requireStringArray(task, 'source_refs', 'invalid_review_response'),
    evidenceRefs: requireStringArray(task, 'evidence_refs', 'invalid_review_response'),
    completedAt,
    createdAt: requireNonEmptyString(task, 'created_at', 'invalid_review_response'),
  };
}

function toReviewRevision(value: unknown): ReviewRevisionSummary {
  const revision = requireRecord(value, 'invalid_review_response');
  if (!Array.isArray(revision.tasks)) throw new ApiRequestError('invalid_review_response');
  const diff = requireRecord(revision.diff, 'invalid_review_response');
  const parent = revision.parent_revision_id;
  if (parent !== null && typeof parent !== 'string') throw new ApiRequestError('invalid_review_response');
  return {
    revisionId: requireNonEmptyString(revision, 'revision_id', 'invalid_review_response'),
    courseId: requireNonEmptyString(revision, 'course_id', 'invalid_review_response'),
    inputHash: requireNonEmptyString(revision, 'input_hash', 'invalid_review_response'),
    parentRevisionId: parent,
    createdAt: requireNonEmptyString(revision, 'created_at', 'invalid_review_response'),
    tasks: revision.tasks.map(toReviewTask),
    diff: {
      added: requireStringArray(diff, 'added', 'invalid_review_response'),
      removed: requireStringArray(diff, 'removed', 'invalid_review_response'),
      changed: requireStringArray(diff, 'changed', 'invalid_review_response'),
      retained: requireStringArray(diff, 'retained', 'invalid_review_response'),
    },
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
    async getProviderSettings(): Promise<ProviderSettingsSummary> {
      const response = await fetchImpl('/api/settings', {
        credentials: 'same-origin', headers: { accept: 'application/json' },
      });
      if (!response.ok) throw await requestError(response, 'provider_settings_unavailable');
      const payload = requireRecord(await response.json(), 'invalid_provider_settings');
      if (payload.provider_mode === 'L') return { providerMode: 'L', providerProfile: null };
      if (payload.provider_mode !== 'L+P') throw new ApiRequestError('invalid_provider_settings');
      return { providerMode: 'L+P', providerProfile: toProviderProfile(payload.provider_profile) };
    },
    async previewExplanation(input: {
      locatorIds: readonly string[];
      profileId: string;
      instruction: string;
      nonce: string;
    }): Promise<ProviderPreviewSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl('/api/providers/previews/explanation', {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({
          locator_ids: input.locatorIds,
          profile_id: input.profileId,
          instruction: input.instruction,
          nonce: input.nonce,
        }),
      });
      if (!response.ok) throw await requestError(response, 'provider_preview_failed');
      const payload = requireRecord(await response.json(), 'invalid_provider_preview');
      if (payload.operation !== 'generate_explanation' || payload.adapter_id !== 'openai') {
        throw new ApiRequestError('invalid_provider_preview');
      }
      if (!Array.isArray(payload.sources) || payload.sources.length === 0) {
        throw new ApiRequestError('invalid_provider_preview');
      }
      return {
        previewId: requireNonEmptyString(payload, 'preview_id', 'invalid_provider_preview'),
        operation: 'generate_explanation',
        profileId: requireNonEmptyString(payload, 'profile_id', 'invalid_provider_preview'),
        adapterId: 'openai',
        modelId: requireNonEmptyString(payload, 'model_id', 'invalid_provider_preview'),
        inputTokenCap: requirePositiveInteger(payload, 'input_token_cap', 'invalid_provider_preview'),
        outputTokenCap: requirePositiveInteger(payload, 'max_tokens', 'invalid_provider_preview'),
        maxCostMicrousd: requirePositiveInteger(payload, 'max_cost_microusd', 'invalid_provider_preview'),
        configFingerprint: requireNonEmptyString(payload, 'config_fingerprint', 'invalid_provider_preview'),
        policyFingerprint: requireNonEmptyString(payload, 'policy_fingerprint', 'invalid_provider_preview'),
        sources: payload.sources.map(toProviderPreviewSource),
      };
    },
    async grantProviderConsent(previewId: string): Promise<{ consentId: string }> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl('/api/providers/consents', {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ preview_id: previewId }),
      });
      if (!response.ok) throw await requestError(response, 'provider_consent_failed');
      const payload = requireRecord(await response.json(), 'invalid_provider_consent');
      return { consentId: requireNonEmptyString(payload, 'consent_id', 'invalid_provider_consent') };
    },
    async executeProvider(previewId: string, consentId: string): Promise<ProviderCandidateSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl('/api/providers/execute', {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ preview_id: previewId, consent_id: consentId }),
      });
      if (!response.ok) throw await requestError(response, 'provider_execute_failed');
      const payload = requireRecord(await response.json(), 'invalid_provider_candidate');
      if (payload.authoritative !== false) throw new ApiRequestError('invalid_provider_candidate');
      return { text: requireNonEmptyString(payload, 'text', 'invalid_provider_candidate'), authoritative: false };
    },
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
    async generateReviewRevision(input: {
      courseId: string;
      mode: 'continuous' | 'finals';
      timezone: string;
      dailyBudgetMinutes: number;
      examDate?: string;
      generatedAt: string;
    }): Promise<ReviewRevisionSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl('/api/review/revisions', {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({
          course_id: input.courseId,
          mode: input.mode,
          timezone: input.timezone,
          daily_budget_minutes: input.dailyBudgetMinutes,
          exam_date: input.examDate,
          generated_at: input.generatedAt,
        }),
      });
      if (!response.ok) throw await requestError(response, 'review_revision_failed');
      return toReviewRevision(await response.json());
    },
    async completeReviewTask(taskId: string, completedAt: string): Promise<ReviewTaskSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/review/tasks/${encodeURIComponent(taskId)}/complete`, {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'content-type': 'application/json', 'x-csrf-token': csrfHeader },
        body: JSON.stringify({ completed_at: completedAt }),
      });
      if (!response.ok) throw await requestError(response, 'review_task_failed');
      return toReviewTask(await response.json());
    },
    async skipReviewTask(taskId: string): Promise<ReviewTaskSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/review/tasks/${encodeURIComponent(taskId)}/skip`, {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      if (!response.ok) throw await requestError(response, 'review_task_failed');
      return toReviewTask(await response.json());
    },
    async recoverReviewTask(taskId: string): Promise<ReviewTaskSummary> {
      const csrfHeader = await csrfToken();
      const response = await fetchImpl(`/api/review/tasks/${encodeURIComponent(taskId)}/recover`, {
        method: 'POST', credentials: 'same-origin',
        headers: { accept: 'application/json', 'x-csrf-token': csrfHeader },
      });
      if (!response.ok) throw await requestError(response, 'review_task_failed');
      return toReviewTask(await response.json());
    },
  };
}

export type ApiClient = ReturnType<typeof createApiClient>;
