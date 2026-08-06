PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS course (
    course_id TEXT PRIMARY KEY CHECK (length(course_id) > 0),
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    timezone TEXT NOT NULL CHECK (length(trim(timezone)) > 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS material (
    material_id TEXT PRIMARY KEY CHECK (length(material_id) > 0),
    course_id TEXT NOT NULL REFERENCES course(course_id) ON DELETE CASCADE,
    filename TEXT NOT NULL CHECK (length(trim(filename)) > 0),
    media_type TEXT NOT NULL CHECK (length(trim(media_type)) > 0),
    content_hash TEXT NOT NULL CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    status TEXT NOT NULL CHECK (status IN ('pending', 'ready', 'failed', 'deleted')),
    created_at TEXT NOT NULL,
    UNIQUE(course_id, content_hash)
);

CREATE TABLE IF NOT EXISTS blob_object (
    content_hash TEXT PRIMARY KEY CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    storage_ref TEXT NOT NULL CHECK (length(trim(storage_ref)) > 0),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
    delete_pending INTEGER NOT NULL DEFAULT 0 CHECK (delete_pending IN (0, 1))
);

CREATE TABLE IF NOT EXISTS material_blob_ref (
    material_id TEXT NOT NULL REFERENCES material(material_id) ON DELETE CASCADE,
    content_hash TEXT NOT NULL REFERENCES blob_object(content_hash) ON DELETE RESTRICT,
    PRIMARY KEY(material_id, content_hash)
);

CREATE TABLE IF NOT EXISTS material_version (
    version_id TEXT PRIMARY KEY CHECK (length(version_id) > 0),
    material_id TEXT NOT NULL REFERENCES material(material_id) ON DELETE CASCADE,
    parser_id TEXT NOT NULL CHECK (length(trim(parser_id)) > 0),
    parser_version TEXT NOT NULL CHECK (length(trim(parser_version)) > 0),
    extraction_contract_version TEXT NOT NULL CHECK (length(trim(extraction_contract_version)) > 0),
    extraction_status TEXT NOT NULL CHECK (extraction_status IN ('pending', 'ready', 'failed')),
    locator_index_json TEXT NOT NULL DEFAULT '{}',
    content_hash TEXT NOT NULL CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    created_at TEXT NOT NULL,
    UNIQUE(material_id, parser_id, parser_version, extraction_contract_version)
);

CREATE TABLE IF NOT EXISTS source_locator (
    locator_id TEXT PRIMARY KEY CHECK (length(locator_id) > 0),
    material_version_id TEXT NOT NULL REFERENCES material_version(version_id) ON DELETE CASCADE,
    content_hash TEXT NOT NULL CHECK (length(content_hash) = 64 AND content_hash NOT GLOB '*[^0-9a-f]*'),
    locator_kind TEXT NOT NULL CHECK (locator_kind IN ('pdf_page', 'text_lines')),
    page_start INTEGER,
    page_end INTEGER,
    line_start INTEGER,
    line_end INTEGER,
    CHECK (
        (locator_kind = 'pdf_page' AND page_start IS NOT NULL AND page_end IS NOT NULL
            AND page_start > 0 AND page_start = page_end AND line_start IS NULL AND line_end IS NULL)
        OR
        (locator_kind = 'text_lines' AND line_start IS NOT NULL AND line_end IS NOT NULL
            AND line_start > 0 AND line_start <= line_end AND page_start IS NULL AND page_end IS NULL)
    )
);

CREATE TABLE IF NOT EXISTS knowledge_concept (
    concept_id TEXT PRIMARY KEY CHECK (length(concept_id) > 0),
    course_id TEXT NOT NULL REFERENCES course(course_id) ON DELETE CASCADE,
    name TEXT NOT NULL CHECK (length(trim(name)) > 0),
    evaluator_id TEXT,
    version INTEGER NOT NULL CHECK (version > 0),
    state TEXT NOT NULL CHECK (state IN ('active', 'explanation_only')),
    created_at TEXT NOT NULL,
    UNIQUE(course_id, name, version)
);

CREATE TABLE IF NOT EXISTS coverage_decision (
    decision_id TEXT PRIMARY KEY CHECK (length(decision_id) > 0),
    concept_id TEXT NOT NULL REFERENCES knowledge_concept(concept_id) ON DELETE CASCADE,
    locator_ids_json TEXT NOT NULL,
    decision TEXT NOT NULL CHECK (decision IN ('confirmed', 'rejected')),
    version INTEGER NOT NULL CHECK (version > 0),
    confirmed_at TEXT NOT NULL,
    UNIQUE(concept_id, version)
);

CREATE TABLE IF NOT EXISTS provider_profile (
    profile_id TEXT PRIMARY KEY CHECK (length(profile_id) > 0),
    adapter_id TEXT NOT NULL CHECK (length(trim(adapter_id)) > 0),
    model_id TEXT NOT NULL CHECK (length(trim(model_id)) > 0),
    budget_limit INTEGER NOT NULL CHECK (budget_limit >= 0),
    credential_ref TEXT NOT NULL CHECK (length(trim(credential_ref)) > 0),
    config_fingerprint TEXT NOT NULL CHECK (length(trim(config_fingerprint)) > 0),
    policy_fingerprint TEXT NOT NULL CHECK (length(trim(policy_fingerprint)) > 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS consent_record (
    consent_id TEXT PRIMARY KEY CHECK (length(consent_id) > 0),
    port TEXT NOT NULL CHECK (port = 'P'),
    locator_ids_json TEXT NOT NULL,
    source_hashes_json TEXT NOT NULL,
    preview_hash TEXT NOT NULL CHECK (length(preview_hash) = 64 AND preview_hash NOT GLOB '*[^0-9a-f]*'),
    profile_id TEXT NOT NULL REFERENCES provider_profile(profile_id) ON DELETE RESTRICT,
    policy_fingerprint TEXT NOT NULL,
    budget_limit INTEGER NOT NULL CHECK (budget_limit >= 0),
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS audit_event (
    event_id TEXT PRIMARY KEY CHECK (length(event_id) > 0),
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    result TEXT NOT NULL,
    opaque_refs_json TEXT NOT NULL,
    fingerprint TEXT NOT NULL,
    error_code TEXT,
    created_at TEXT NOT NULL
);

CREATE TRIGGER IF NOT EXISTS material_blob_ref_matches_material
BEFORE INSERT ON material_blob_ref
WHEN (SELECT content_hash FROM material WHERE material_id = NEW.material_id) <> NEW.content_hash
BEGIN
    SELECT RAISE(ABORT, 'material_blob_hash_mismatch');
END;

CREATE TRIGGER IF NOT EXISTS material_content_hash_immutable
BEFORE UPDATE OF content_hash ON material
WHEN NEW.content_hash <> OLD.content_hash
BEGIN
    SELECT RAISE(ABORT, 'material_content_hash_immutable');
END;

CREATE TRIGGER IF NOT EXISTS material_version_matches_material
BEFORE INSERT ON material_version
WHEN (SELECT content_hash FROM material WHERE material_id = NEW.material_id) <> NEW.content_hash
BEGIN
    SELECT RAISE(ABORT, 'material_version_hash_mismatch');
END;

CREATE TRIGGER IF NOT EXISTS source_locator_matches_version
BEFORE INSERT ON source_locator
WHEN (SELECT content_hash FROM material_version WHERE version_id = NEW.material_version_id) <> NEW.content_hash
BEGIN
    SELECT RAISE(ABORT, 'source_locator_hash_mismatch');
END;

CREATE TRIGGER IF NOT EXISTS material_version_immutable_update
BEFORE UPDATE ON material_version
BEGIN
    SELECT RAISE(ABORT, 'material_version_immutable');
END;

CREATE TRIGGER IF NOT EXISTS source_locator_immutable_update
BEFORE UPDATE ON source_locator
BEGIN
    SELECT RAISE(ABORT, 'source_locator_immutable');
END;

CREATE TRIGGER IF NOT EXISTS consent_record_immutable_update
BEFORE UPDATE ON consent_record
BEGIN
    SELECT RAISE(ABORT, 'consent_record_immutable');
END;

CREATE TRIGGER IF NOT EXISTS consent_record_immutable_delete
BEFORE DELETE ON consent_record
BEGIN
    SELECT RAISE(ABORT, 'consent_record_immutable');
END;

CREATE TRIGGER IF NOT EXISTS audit_event_immutable_update
BEFORE UPDATE ON audit_event
BEGIN
    SELECT RAISE(ABORT, 'audit_event_immutable');
END;

CREATE TRIGGER IF NOT EXISTS audit_event_immutable_delete
BEFORE DELETE ON audit_event
BEGIN
    SELECT RAISE(ABORT, 'audit_event_immutable');
END;

CREATE TRIGGER IF NOT EXISTS coverage_decision_immutable_update
BEFORE UPDATE ON coverage_decision
BEGIN
    SELECT RAISE(ABORT, 'coverage_decision_immutable');
END;

CREATE TRIGGER IF NOT EXISTS coverage_decision_immutable_delete
BEFORE DELETE ON coverage_decision
BEGIN
    SELECT RAISE(ABORT, 'coverage_decision_immutable');
END;
