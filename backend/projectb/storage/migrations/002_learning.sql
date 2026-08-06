PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS attempt (
    attempt_id TEXT PRIMARY KEY CHECK (length(attempt_id) > 0),
    attempt_key TEXT NOT NULL UNIQUE CHECK (length(trim(attempt_key)) > 0),
    concept_id TEXT NOT NULL REFERENCES knowledge_concept(concept_id) ON DELETE RESTRICT,
    check_kind TEXT NOT NULL CHECK (check_kind IN ('starting_probe', 'isomorphic', 'transfer', 'delayed_variant')),
    variant_id TEXT NOT NULL CHECK (length(trim(variant_id)) > 0),
    answer_json TEXT NOT NULL CHECK (json_valid(answer_json)),
    status TEXT NOT NULL CHECK (status IN ('started', 'submitted', 'evaluated', 'abandoned')),
    created_at TEXT NOT NULL CHECK (length(trim(created_at)) > 0),
    updated_at TEXT NOT NULL CHECK (length(trim(updated_at)) > 0)
);

CREATE TABLE IF NOT EXISTS learning_evidence (
    evidence_id TEXT PRIMARY KEY CHECK (length(evidence_id) > 0),
    attempt_id TEXT NOT NULL UNIQUE REFERENCES attempt(attempt_id) ON DELETE RESTRICT,
    course_id TEXT NOT NULL REFERENCES course(course_id) ON DELETE RESTRICT,
    concept_id TEXT NOT NULL REFERENCES knowledge_concept(concept_id) ON DELETE RESTRICT,
    evaluator_id TEXT NOT NULL CHECK (length(trim(evaluator_id)) > 0),
    evaluator_version TEXT NOT NULL CHECK (length(trim(evaluator_version)) > 0),
    check_kind TEXT NOT NULL CHECK (check_kind IN ('starting_probe', 'isomorphic', 'transfer', 'delayed_variant')),
    outcome TEXT NOT NULL CHECK (outcome IN ('incorrect', 'partial', 'passed', 'refused', 'source_insufficient', 'skipped')),
    rubric_json TEXT NOT NULL CHECK (json_valid(rubric_json)),
    source_ids_json TEXT NOT NULL CHECK (json_valid(source_ids_json)),
    evidence_version INTEGER NOT NULL CHECK (evidence_version > 0),
    idempotency_key TEXT NOT NULL UNIQUE CHECK (length(trim(idempotency_key)) > 0),
    created_at TEXT NOT NULL
        CHECK (substr(created_at, -1) = 'Z' AND strftime('%Y-%m-%dT%H:%M:%fZ', created_at) IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS mastery_estimate (
    estimate_id TEXT PRIMARY KEY CHECK (length(estimate_id) > 0),
    concept_id TEXT NOT NULL REFERENCES knowledge_concept(concept_id) ON DELETE RESTRICT,
    derived_state TEXT NOT NULL CHECK (derived_state IN ('unknown', 'demonstrated_now', 'retained')),
    evidence_input_hash TEXT NOT NULL
        CHECK (length(evidence_input_hash) = 64 AND evidence_input_hash NOT GLOB '*[^0-9a-f]*'),
    created_at TEXT NOT NULL CHECK (length(trim(created_at)) > 0),
    UNIQUE(concept_id, evidence_input_hash)
);

CREATE TABLE IF NOT EXISTS review_plan_revision (
    revision_id TEXT PRIMARY KEY CHECK (length(revision_id) > 0),
    course_id TEXT NOT NULL REFERENCES course(course_id) ON DELETE RESTRICT,
    mode TEXT NOT NULL CHECK (mode IN ('continuous', 'finals')),
    timezone TEXT NOT NULL CHECK (length(trim(timezone)) > 0),
    budget_minutes INTEGER NOT NULL DEFAULT 30 CHECK (budget_minutes BETWEEN 10 AND 120 AND budget_minutes % 5 = 0),
    exam_date TEXT,
    input_hash TEXT NOT NULL CHECK (length(input_hash) = 64 AND input_hash NOT GLOB '*[^0-9a-f]*'),
    parent_revision_id TEXT REFERENCES review_plan_revision(revision_id) ON DELETE RESTRICT,
    created_at TEXT NOT NULL CHECK (length(trim(created_at)) > 0),
    CHECK (parent_revision_id IS NULL OR parent_revision_id <> revision_id),
    CHECK (
        (mode = 'continuous' AND exam_date IS NULL)
        OR
        (mode = 'finals' AND exam_date IS NOT NULL AND length(trim(exam_date)) > 0)
    ),
    UNIQUE(course_id, input_hash)
);

CREATE TABLE IF NOT EXISTS review_task (
    task_id TEXT PRIMARY KEY CHECK (length(task_id) > 0),
    revision_id TEXT NOT NULL REFERENCES review_plan_revision(revision_id) ON DELETE CASCADE,
    concept_id TEXT NOT NULL REFERENCES knowledge_concept(concept_id) ON DELETE RESTRICT,
    due_local_date TEXT NOT NULL CHECK (length(trim(due_local_date)) > 0),
    duration_minutes INTEGER NOT NULL DEFAULT 10 CHECK (duration_minutes = 10),
    status TEXT NOT NULL CHECK (status IN ('pending', 'completed', 'skipped')),
    source_refs_json TEXT NOT NULL CHECK (json_valid(source_refs_json)),
    evidence_refs_json TEXT NOT NULL CHECK (json_valid(evidence_refs_json)),
    completed_at TEXT,
    created_at TEXT NOT NULL CHECK (length(trim(created_at)) > 0),
    CHECK ((status = 'completed') = (completed_at IS NOT NULL)),
    UNIQUE(revision_id, concept_id, due_local_date)
);

CREATE TRIGGER IF NOT EXISTS learning_evidence_immutable_update
BEFORE UPDATE ON learning_evidence
BEGIN
    SELECT RAISE(ABORT, 'learning_evidence_immutable');
END;

CREATE TRIGGER IF NOT EXISTS learning_evidence_matches_attempt
BEFORE INSERT ON learning_evidence
WHEN NOT EXISTS (
    SELECT 1
    FROM attempt
    JOIN knowledge_concept ON knowledge_concept.concept_id = attempt.concept_id
    WHERE attempt.attempt_id = NEW.attempt_id
      AND attempt.concept_id = NEW.concept_id
      AND knowledge_concept.course_id = NEW.course_id
      AND attempt.check_kind = NEW.check_kind
)
BEGIN
    SELECT RAISE(ABORT, 'learning_evidence_context_mismatch');
END;

CREATE TRIGGER IF NOT EXISTS learning_evidence_immutable_delete
BEFORE DELETE ON learning_evidence
BEGIN
    SELECT RAISE(ABORT, 'learning_evidence_immutable');
END;

CREATE TRIGGER IF NOT EXISTS mastery_estimate_immutable_update
BEFORE UPDATE ON mastery_estimate
BEGIN
    SELECT RAISE(ABORT, 'mastery_estimate_immutable');
END;

CREATE TRIGGER IF NOT EXISTS mastery_estimate_immutable_delete
BEFORE DELETE ON mastery_estimate
BEGIN
    SELECT RAISE(ABORT, 'mastery_estimate_immutable');
END;

CREATE TRIGGER IF NOT EXISTS review_plan_revision_parent_same_course
BEFORE INSERT ON review_plan_revision
WHEN NEW.parent_revision_id IS NOT NULL
    AND NOT EXISTS (
        SELECT 1
        FROM review_plan_revision AS parent
        WHERE parent.revision_id = NEW.parent_revision_id
          AND parent.course_id = NEW.course_id
    )
BEGIN
    SELECT RAISE(ABORT, 'review_plan_revision_parent_course_mismatch');
END;

CREATE TRIGGER IF NOT EXISTS review_plan_revision_immutable_update
BEFORE UPDATE ON review_plan_revision
BEGIN
    SELECT RAISE(ABORT, 'review_plan_revision_immutable');
END;

CREATE TRIGGER IF NOT EXISTS review_task_completed_immutable_update
BEFORE UPDATE ON review_task
WHEN OLD.status = 'completed'
BEGIN
    SELECT RAISE(ABORT, 'completed_review_task_immutable');
END;

CREATE TRIGGER IF NOT EXISTS review_task_completed_immutable_delete
BEFORE DELETE ON review_task
WHEN OLD.status = 'completed'
BEGIN
    SELECT RAISE(ABORT, 'completed_review_task_immutable');
END;

CREATE TRIGGER IF NOT EXISTS review_task_matches_revision_course
BEFORE INSERT ON review_task
WHEN NOT EXISTS (
    SELECT 1
    FROM review_plan_revision AS revision
    JOIN knowledge_concept ON knowledge_concept.concept_id = NEW.concept_id
    WHERE revision.revision_id = NEW.revision_id
      AND revision.course_id = knowledge_concept.course_id
)
BEGIN
    SELECT RAISE(ABORT, 'review_task_course_mismatch');
END;
