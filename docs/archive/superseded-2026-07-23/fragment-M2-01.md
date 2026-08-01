# M2-01 Mutex/Race Oracle and Starting Probes Implementation Plan

> **Status: INCOMPLETE DRAFT - DO NOT DISPATCH.** Drafting was intentionally interrupted after the independent T-01/T-02 review found Critical template defects. This file is not linked from the PLAN ledger, has not passed `superpowers:writing-plans`, and must not be used for G-03 or implementation.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, replayable mutex/race trace oracle, five-criterion rubric, three bounded starting probes, and evidence-eligibility gates without model, persistence, mastery, or planning authority.

**Architecture:** Parse the exact `mutex-race.v1` trace and `mutex-race-answer.v1` answer unions into immutable domain values. Keep event execution, rubric evaluation, and starting-probe diagnosis in separate pure application modules, then expose one `projectb.application.mutex_race` facade for M2-02 consumers. All tests use synthetic fixtures and make zero provider or network calls.

**Tech Stack:** CPython 3.14.6 standard library (`copy`, `dataclasses`, `enum`, `json`, `pathlib`, `typing`) with pytest 9.1.1, Ruff 0.15.22, and mypy 2.3.0 from T-01's locked backend environment.

---

### Task M2-01: Implement the Mutex/Race Parameterized Oracle and Starting Probes

**Files:**
- Create: `backend/src/projectb/domain/learning.py`
- Create: `backend/src/projectb/application/__init__.py`
- Create: `backend/src/projectb/application/mutex_race_execution.py`
- Create: `backend/src/projectb/application/mutex_race_rubric.py`
- Create: `backend/src/projectb/application/mutex_race_probes.py`
- Create: `backend/src/projectb/application/mutex_race.py`
- Create: `backend/tests/fixtures/mutex_race_traces.json`
- Create: `backend/tests/unit/test_mutex_race_contract.py`
- Create: `backend/tests/unit/test_mutex_race_execution.py`
- Create: `backend/tests/unit/test_mutex_race_rubric.py`
- Create: `backend/tests/unit/test_mutex_race_probes.py`
- Create: `backend/tests/unit/test_mutex_race_exports.py`

**Dependencies / parallelism:** Formal implementation starts only after T-01, T-02, T-03C, G-03 approval, and the implementation gate are satisfied. This unit does not import a repository or source locator and cannot write evidence; T-02/T-03C remain ordering contracts for later M2 integration. During the disposable G-03 cold-start experiment, the experiment's explicit dependency exception permits this self-contained pure slice to run from only `SPEC.md` and `PLAN.md`. M2-01 exclusively owns every file listed above and may run beside X2-01 and M3-01 after formal dispatch because it edits no provider, repository, source, mastery, or plan file.

**Produced interfaces:**
- `trace_from_mapping(payload) -> TraceSpec` accepts only `trace_version="mutex-race.v1"`, sorted threads, globally unique event IDs, integer shared state, and the five event operations `read | add | write | lock | unlock` with their exact fields.
- `answer_from_mapping(payload) -> MutexRaceAnswer` accepts only `answer_version="mutex-race-answer.v1"` and the exact `interleaving | race_window | repair_invariant` branches.
- `enumerate_legal_interleavings(trace) -> Sequence[Interleaving]` preserves thread order, includes every event exactly once, and applies register, shared-state, and mutex-owner semantics deterministically.
- `evaluate_answer(answer, trace) -> OracleResult` always emits the five sorted criterion IDs `event_completeness | final_state | mutual_exclusion_invariant | race_window | thread_order`, using `not_applicable` outside the answer branch.
- `run_starting_probes(trace, attempts, max_probes=3) -> Sequence[ProbeResult]` accepts only the ordered diagnostic prefix `race_preconditions | read_modify_write_expansion | bad_interleaving`, never more than three, and exposes no mastery mutation.
- `evidence_gate(check_kind, oracle_results) -> EvidenceGate` makes starting probes permanently ineligible, requires all three interleaving criteria for `isomorphic`, requires both transfer criteria across race-window and repair-invariant results for `transfer`, and does not construct or persist `LearningEvidence`.

- [ ] **Step 1: Create the two synthetic trace fixtures**

Create `backend/tests/fixtures/mutex_race_traces.json` with exactly:

```json
{
  "traces": [
    {
      "trace_version": "mutex-race.v1",
      "trace_id": "lost-update-seed-11",
      "seed": 11,
      "initial_shared_state": {
        "counter": 0
      },
      "threads": [
        {
          "thread_id": "t-a",
          "events": [
            {
              "kind": "read",
              "event_id": "a-read",
              "variable": "counter",
              "register": "r-a"
            },
            {
              "kind": "add",
              "event_id": "a-add",
              "register": "r-a",
              "integer_delta": 1
            },
            {
              "kind": "write",
              "event_id": "a-write",
              "register": "r-a",
              "variable": "counter"
            }
          ]
        },
        {
          "thread_id": "t-b",
          "events": [
            {
              "kind": "read",
              "event_id": "b-read",
              "variable": "counter",
              "register": "r-b"
            },
            {
              "kind": "add",
              "event_id": "b-add",
              "register": "r-b",
              "integer_delta": 1
            },
            {
              "kind": "write",
              "event_id": "b-write",
              "register": "r-b",
              "variable": "counter"
            }
          ]
        }
      ],
      "expected_final_states": [
        {
          "counter": 1
        },
        {
          "counter": 2
        }
      ]
    },
    {
      "trace_version": "mutex-race.v1",
      "trace_id": "mutex-protected-seed-17",
      "seed": 17,
      "initial_shared_state": {
        "counter": 0
      },
      "threads": [
        {
          "thread_id": "t-a",
          "events": [
            {
              "kind": "lock",
              "event_id": "a-lock",
              "mutex_id": "m-counter"
            },
            {
              "kind": "read",
              "event_id": "a-read",
              "variable": "counter",
              "register": "r-a"
            },
            {
              "kind": "add",
              "event_id": "a-add",
              "register": "r-a",
              "integer_delta": 1
            },
            {
              "kind": "write",
              "event_id": "a-write",
              "register": "r-a",
              "variable": "counter"
            },
            {
              "kind": "unlock",
              "event_id": "a-unlock",
              "mutex_id": "m-counter"
            }
          ]
        },
        {
          "thread_id": "t-b",
          "events": [
            {
              "kind": "lock",
              "event_id": "b-lock",
              "mutex_id": "m-counter"
            },
            {
              "kind": "read",
              "event_id": "b-read",
              "variable": "counter",
              "register": "r-b"
            },
            {
              "kind": "add",
              "event_id": "b-add",
              "register": "r-b",
              "integer_delta": 1
            },
            {
              "kind": "write",
              "event_id": "b-write",
              "register": "r-b",
              "variable": "counter"
            },
            {
              "kind": "unlock",
              "event_id": "b-unlock",
              "mutex_id": "m-counter"
            }
          ]
        }
      ],
      "expected_final_states": [
        {
          "counter": 2
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: Write the failing trace and answer contract tests**

Create `backend/tests/unit/test_mutex_race_contract.py` with exactly:

```python
from copy import deepcopy
import json
from pathlib import Path

import pytest

from projectb.domain.learning import (
    AnswerKind,
    EventKind,
    InterleavingAnswer,
    MutexRaceContractError,
    RaceWindowAnswer,
    RepairInvariantAnswer,
    answer_from_mapping,
    canonical_trace_json,
    trace_from_mapping,
)


FIXTURE_PATH = Path("backend/tests/fixtures/mutex_race_traces.json")


def load_trace_payload(index: int = 0) -> dict[str, object]:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return deepcopy(document["traces"][index])


def test_trace_parser_preserves_versions_order_and_unique_events() -> None:
    trace = trace_from_mapping(load_trace_payload())
    assert trace.trace_version == "mutex-race.v1"
    assert trace.trace_id == "lost-update-seed-11"
    assert trace.seed == 11
    assert [thread.thread_id for thread in trace.threads] == ["t-a", "t-b"]
    event_ids = [event.event_id for thread in trace.threads for event in thread.events]
    assert event_ids == [
        "a-read",
        "a-add",
        "a-write",
        "b-read",
        "b-add",
        "b-write",
    ]


def test_canonical_trace_json_is_stable_after_round_trip() -> None:
    trace = trace_from_mapping(load_trace_payload())
    encoded = canonical_trace_json(trace)
    reparsed = trace_from_mapping(json.loads(encoded))
    assert canonical_trace_json(reparsed) == encoded
    assert " " not in encoded
    assert "\n" not in encoded


def test_event_kind_whitelist_is_exact() -> None:
    assert [kind.value for kind in EventKind] == [
        "read",
        "add",
        "write",
        "lock",
        "unlock",
    ]


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("wrong_version", "invalid_trace_version"),
        ("unknown_top_field", "invalid_shape"),
        ("unsorted_threads", "thread_order_invalid"),
        ("duplicate_event_id", "duplicate_event_id"),
        ("unknown_event_kind", "invalid_event_kind"),
        ("state_shape_mismatch", "state_shape_mismatch"),
    ],
)
def test_trace_parser_rejects_noncanonical_contracts(
    case: str,
    expected_code: str,
) -> None:
    payload = load_trace_payload()
    threads = payload["threads"]
    if case == "wrong_version":
        payload["trace_version"] = "mutex-race.v2"
    elif case == "unknown_top_field":
        payload["provider_feedback"] = "ignored"
    elif case == "unsorted_threads":
        payload["threads"] = list(reversed(threads))
    elif case == "duplicate_event_id":
        threads[1]["events"][0]["event_id"] = "a-read"
    elif case == "unknown_event_kind":
        threads[0]["events"][0]["kind"] = "sleep"
    else:
        payload["expected_final_states"] = [{"other": 1}]
    with pytest.raises(MutexRaceContractError) as caught:
        trace_from_mapping(payload)
    assert caught.value.code == expected_code


@pytest.mark.parametrize(
    ("payload", "expected_type", "expected_kind"),
    [
        (
            {
                "answer_version": "mutex-race-answer.v1",
                "kind": "interleaving",
                "trace_id": "lost-update-seed-11",
                "ordered_event_ids": [
                    "a-read",
                    "b-read",
                    "a-add",
                    "a-write",
                    "b-add",
                    "b-write",
                ],
                "reported_final_state": {"counter": 1},
            },
            InterleavingAnswer,
            AnswerKind.INTERLEAVING,
        ),
        (
            {
                "answer_version": "mutex-race-answer.v1",
                "kind": "race_window",
                "trace_id": "lost-update-seed-11",
                "variable": "counter",
                "first_event_id": "a-read",
                "second_event_id": "b-write",
            },
            RaceWindowAnswer,
            AnswerKind.RACE_WINDOW,
        ),
        (
            {
                "answer_version": "mutex-race-answer.v1",
                "kind": "repair_invariant",
                "trace_id": "lost-update-seed-11",
                "mutex_id": "m-counter",
                "protected_event_ids": [
                    "a-read",
                    "a-add",
                    "a-write",
                    "b-read",
                    "b-add",
                    "b-write",
                ],
                "invariant": "at_most_one_thread_in_critical_section",
            },
            RepairInvariantAnswer,
            AnswerKind.REPAIR_INVARIANT,
        ),
    ],
)
def test_answer_parser_accepts_each_exact_union_branch(
    payload: dict[str, object],
    expected_type: type[object],
    expected_kind: AnswerKind,
) -> None:
    answer = answer_from_mapping(payload)
    assert isinstance(answer, expected_type)
    assert answer.kind is expected_kind


@pytest.mark.parametrize(
    ("case", "expected_code"),
    [
        ("wrong_version", "invalid_answer_version"),
        ("unknown_kind", "invalid_answer_kind"),
        ("mixed_fields", "invalid_shape"),
        ("wrong_invariant", "invalid_invariant"),
    ],
)
def test_answer_parser_rejects_unknown_or_mixed_contracts(
    case: str,
    expected_code: str,
) -> None:
    payload: dict[str, object] = {
        "answer_version": "mutex-race-answer.v1",
        "kind": "repair_invariant",
        "trace_id": "lost-update-seed-11",
        "mutex_id": "m-counter",
        "protected_event_ids": ["a-read", "a-add", "a-write"],
        "invariant": "at_most_one_thread_in_critical_section",
    }
    if case == "wrong_version":
        payload["answer_version"] = "mutex-race-answer.v2"
    elif case == "unknown_kind":
        payload["kind"] = "free_text"
    elif case == "mixed_fields":
        payload["reported_final_state"] = {"counter": 1}
    else:
        payload["invariant"] = "eventually_every_thread_enters"
    with pytest.raises(MutexRaceContractError) as caught:
        answer_from_mapping(payload)
    assert caught.value.code == expected_code
```

- [ ] **Step 3: Run the contract tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_contract.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.domain.learning'`; no test passes.

- [ ] **Step 4: Implement the immutable trace, answer, rubric-result, and parser contracts**

Create `backend/src/projectb/domain/learning.py` with exactly:

```python
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from enum import StrEnum
import json
from typing import TypeAlias, cast


TRACE_VERSION = "mutex-race.v1"
ANSWER_VERSION = "mutex-race-answer.v1"
REPAIR_INVARIANT = "at_most_one_thread_in_critical_section"


class MutexRaceContractError(ValueError):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class EventKind(StrEnum):
    READ = "read"
    ADD = "add"
    WRITE = "write"
    LOCK = "lock"
    UNLOCK = "unlock"


class AnswerKind(StrEnum):
    INTERLEAVING = "interleaving"
    RACE_WINDOW = "race_window"
    REPAIR_INVARIANT = "repair_invariant"


class CriterionId(StrEnum):
    THREAD_ORDER = "thread_order"
    EVENT_COMPLETENESS = "event_completeness"
    FINAL_STATE = "final_state"
    RACE_WINDOW = "race_window"
    MUTUAL_EXCLUSION_INVARIANT = "mutual_exclusion_invariant"


class RubricStatus(StrEnum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"


class DiagnosticCode(StrEnum):
    RACE_PRECONDITIONS = "race_preconditions"
    READ_MODIFY_WRITE_EXPANSION = "read_modify_write_expansion"
    BAD_INTERLEAVING = "bad_interleaving"


class CheckKind(StrEnum):
    STARTING_PROBE = "starting_probe"
    ISOMORPHIC = "isomorphic"
    TRANSFER = "transfer"


StateItems: TypeAlias = Sequence[tuple[str, int]]


def _require_id(value: str, code: str = "invalid_id") -> None:
    if not isinstance(value, str) or not value or value.strip() != value:
        raise MutexRaceContractError(code)


def _require_integer(value: int, code: str = "invalid_integer") -> None:
    if type(value) is not int:
        raise MutexRaceContractError(code)


def _normalize_state_items(value: StateItems) -> tuple:
    items = tuple(value)
    names = [item[0] for item in items]
    if names != sorted(names) or len(names) != len(set(names)):
        raise MutexRaceContractError("state_not_canonical")
    for name, integer in items:
        _require_id(name, "state_shape_mismatch")
        _require_integer(integer, "state_shape_mismatch")
    return items


@dataclass(frozen=True, slots=True)
class EventSpec:
    kind: EventKind
    event_id: str
    variable: str | None = None
    register: str | None = None
    integer_delta: int | None = None
    mutex_id: str | None = None

    def __post_init__(self) -> None:
        _require_id(self.event_id)
        if self.kind is EventKind.READ:
            if self.variable is None or self.register is None:
                raise MutexRaceContractError("invalid_event_shape")
            _require_id(self.variable)
            _require_id(self.register)
            if self.integer_delta is not None or self.mutex_id is not None:
                raise MutexRaceContractError("invalid_event_shape")
        elif self.kind is EventKind.ADD:
            if self.register is None or self.integer_delta is None:
                raise MutexRaceContractError("invalid_event_shape")
            _require_id(self.register)
            _require_integer(self.integer_delta)
            if self.variable is not None or self.mutex_id is not None:
                raise MutexRaceContractError("invalid_event_shape")
        elif self.kind is EventKind.WRITE:
            if self.register is None or self.variable is None:
                raise MutexRaceContractError("invalid_event_shape")
            _require_id(self.register)
            _require_id(self.variable)
            if self.integer_delta is not None or self.mutex_id is not None:
                raise MutexRaceContractError("invalid_event_shape")
        else:
            if self.mutex_id is None:
                raise MutexRaceContractError("invalid_event_shape")
            _require_id(self.mutex_id)
            if (
                self.variable is not None
                or self.register is not None
                or self.integer_delta is not None
            ):
                raise MutexRaceContractError("invalid_event_shape")


@dataclass(frozen=True, slots=True)
class ThreadSpec:
    thread_id: str
    events: Sequence[EventSpec]

    def __post_init__(self) -> None:
        _require_id(self.thread_id)
        events = tuple(self.events)
        if not events or len({event.event_id for event in events}) != len(events):
            raise MutexRaceContractError("duplicate_event_id")
        object.__setattr__(self, "events", events)


@dataclass(frozen=True, slots=True)
class TraceSpec:
    trace_version: str
    trace_id: str
    seed: int
    initial_shared_state: StateItems
    threads: Sequence[ThreadSpec]
    expected_final_states: Sequence[StateItems]

    def __post_init__(self) -> None:
        if self.trace_version != TRACE_VERSION:
            raise MutexRaceContractError("invalid_trace_version")
        _require_id(self.trace_id)
        _require_integer(self.seed)
        initial = _normalize_state_items(self.initial_shared_state)
        if not initial:
            raise MutexRaceContractError("state_shape_mismatch")
        threads = tuple(self.threads)
        thread_ids = [thread.thread_id for thread in threads]
        if not threads or thread_ids != sorted(thread_ids):
            raise MutexRaceContractError("thread_order_invalid")
        if len(thread_ids) != len(set(thread_ids)):
            raise MutexRaceContractError("thread_order_invalid")
        event_ids = [event.event_id for thread in threads for event in thread.events]
        if len(event_ids) != len(set(event_ids)):
            raise MutexRaceContractError("duplicate_event_id")
        state_names = {name for name, _ in initial}
        for thread in threads:
            for event in thread.events:
                if event.kind in (EventKind.READ, EventKind.WRITE):
                    if event.variable not in state_names:
                        raise MutexRaceContractError("state_shape_mismatch")
        expected = tuple(
            _normalize_state_items(state) for state in self.expected_final_states
        )
        if not expected or any({name for name, _ in state} != state_names for state in expected):
            raise MutexRaceContractError("state_shape_mismatch")
        object.__setattr__(self, "initial_shared_state", initial)
        object.__setattr__(self, "threads", threads)
        object.__setattr__(self, "expected_final_states", expected)


@dataclass(frozen=True, slots=True)
class InterleavingAnswer:
    trace_id: str
    ordered_event_ids: Sequence[str]
    reported_final_state: StateItems
    answer_version: str = field(default=ANSWER_VERSION, init=False)
    kind: AnswerKind = field(default=AnswerKind.INTERLEAVING, init=False)

    def __post_init__(self) -> None:
        _require_id(self.trace_id)
        event_ids = tuple(self.ordered_event_ids)
        for event_id in event_ids:
            _require_id(event_id)
        object.__setattr__(self, "ordered_event_ids", event_ids)
        object.__setattr__(
            self,
            "reported_final_state",
            _normalize_state_items(self.reported_final_state),
        )


@dataclass(frozen=True, slots=True)
class RaceWindowAnswer:
    trace_id: str
    variable: str
    first_event_id: str
    second_event_id: str
    answer_version: str = field(default=ANSWER_VERSION, init=False)
    kind: AnswerKind = field(default=AnswerKind.RACE_WINDOW, init=False)

    def __post_init__(self) -> None:
        _require_id(self.trace_id)
        _require_id(self.variable)
        _require_id(self.first_event_id)
        _require_id(self.second_event_id)


@dataclass(frozen=True, slots=True)
class RepairInvariantAnswer:
    trace_id: str
    mutex_id: str
    protected_event_ids: Sequence[str]
    invariant: str
    answer_version: str = field(default=ANSWER_VERSION, init=False)
    kind: AnswerKind = field(default=AnswerKind.REPAIR_INVARIANT, init=False)

    def __post_init__(self) -> None:
        _require_id(self.trace_id)
        _require_id(self.mutex_id)
        protected = tuple(self.protected_event_ids)
        for event_id in protected:
            _require_id(event_id)
        object.__setattr__(self, "protected_event_ids", protected)
        if self.invariant != REPAIR_INVARIANT:
            raise MutexRaceContractError("invalid_invariant")


MutexRaceAnswer: TypeAlias = (
    InterleavingAnswer | RaceWindowAnswer | RepairInvariantAnswer
)


@dataclass(frozen=True, slots=True)
class RubricResult:
    criterion_id: CriterionId
    status: RubricStatus
    error_code: str | None = None

    def __post_init__(self) -> None:
        if self.status is RubricStatus.FAIL and self.error_code is None:
            raise MutexRaceContractError("missing_rubric_error")
        if self.status is not RubricStatus.FAIL and self.error_code is not None:
            raise MutexRaceContractError("unexpected_rubric_error")


@dataclass(frozen=True, slots=True)
class OracleResult:
    answer_kind: AnswerKind
    rubric_results: Sequence[RubricResult]

    def __post_init__(self) -> None:
        results = tuple(self.rubric_results)
        ids = [result.criterion_id.value for result in results]
        if ids != sorted(ids) or len(ids) != len(set(ids)):
            raise MutexRaceContractError("rubric_not_canonical")
        object.__setattr__(self, "rubric_results", results)


def _require_keys(payload: Mapping[str, object], expected: set[str]) -> None:
    if set(payload) != expected:
        raise MutexRaceContractError("invalid_shape")


def _mapping(value: object) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise MutexRaceContractError("invalid_shape")
    return cast(Mapping[str, object], value)


def _sequence(value: object) -> Sequence[object]:
    if not isinstance(value, (list, tuple)):
        raise MutexRaceContractError("invalid_shape")
    return cast(Sequence[object], value)


def _string(payload: Mapping[str, object], key: str) -> str:
    value = payload[key]
    if not isinstance(value, str):
        raise MutexRaceContractError("invalid_shape")
    _require_id(value, "invalid_shape")
    return value


def _integer(payload: Mapping[str, object], key: str) -> int:
    value = payload[key]
    _require_integer(value, "invalid_shape")
    return cast(int, value)


def _state_from_object(value: object) -> tuple:
    mapping = _mapping(value)
    items: list[tuple[str, int]] = []
    for name in sorted(mapping):
        integer = mapping[name]
        _require_id(name, "state_shape_mismatch")
        _require_integer(integer, "state_shape_mismatch")
        items.append((name, cast(int, integer)))
    return tuple(items)


def _parse_event(value: object) -> EventSpec:
    payload = _mapping(value)
    kind_value = payload.get("kind")
    try:
        kind = EventKind(kind_value)
    except (TypeError, ValueError) as error:
        raise MutexRaceContractError("invalid_event_kind") from error
    if kind is EventKind.READ:
        _require_keys(payload, {"kind", "event_id", "variable", "register"})
        return EventSpec(
            kind=kind,
            event_id=_string(payload, "event_id"),
            variable=_string(payload, "variable"),
            register=_string(payload, "register"),
        )
    if kind is EventKind.ADD:
        _require_keys(payload, {"kind", "event_id", "register", "integer_delta"})
        return EventSpec(
            kind=kind,
            event_id=_string(payload, "event_id"),
            register=_string(payload, "register"),
            integer_delta=_integer(payload, "integer_delta"),
        )
    if kind is EventKind.WRITE:
        _require_keys(payload, {"kind", "event_id", "register", "variable"})
        return EventSpec(
            kind=kind,
            event_id=_string(payload, "event_id"),
            register=_string(payload, "register"),
            variable=_string(payload, "variable"),
        )
    _require_keys(payload, {"kind", "event_id", "mutex_id"})
    return EventSpec(
        kind=kind,
        event_id=_string(payload, "event_id"),
        mutex_id=_string(payload, "mutex_id"),
    )


def trace_from_mapping(payload: Mapping[str, object]) -> TraceSpec:
    _require_keys(
        payload,
        {
            "trace_version",
            "trace_id",
            "seed",
            "initial_shared_state",
            "threads",
            "expected_final_states",
        },
    )
    if payload["trace_version"] != TRACE_VERSION:
        raise MutexRaceContractError("invalid_trace_version")
    threads: list[ThreadSpec] = []
    for raw_thread in _sequence(payload["threads"]):
        thread_payload = _mapping(raw_thread)
        _require_keys(thread_payload, {"thread_id", "events"})
        threads.append(
            ThreadSpec(
                thread_id=_string(thread_payload, "thread_id"),
                events=tuple(
                    _parse_event(event)
                    for event in _sequence(thread_payload["events"])
                ),
            )
        )
    return TraceSpec(
        trace_version=TRACE_VERSION,
        trace_id=_string(payload, "trace_id"),
        seed=_integer(payload, "seed"),
        initial_shared_state=_state_from_object(payload["initial_shared_state"]),
        threads=tuple(threads),
        expected_final_states=tuple(
            _state_from_object(state)
            for state in _sequence(payload["expected_final_states"])
        ),
    )


def answer_from_mapping(payload: Mapping[str, object]) -> MutexRaceAnswer:
    if payload.get("answer_version") != ANSWER_VERSION:
        raise MutexRaceContractError("invalid_answer_version")
    kind_value = payload.get("kind")
    try:
        kind = AnswerKind(kind_value)
    except (TypeError, ValueError) as error:
        raise MutexRaceContractError("invalid_answer_kind") from error
    if kind is AnswerKind.INTERLEAVING:
        _require_keys(
            payload,
            {
                "answer_version",
                "kind",
                "trace_id",
                "ordered_event_ids",
                "reported_final_state",
            },
        )
        return InterleavingAnswer(
            trace_id=_string(payload, "trace_id"),
            ordered_event_ids=tuple(
                cast(str, event_id)
                for event_id in _sequence(payload["ordered_event_ids"])
            ),
            reported_final_state=_state_from_object(payload["reported_final_state"]),
        )
    if kind is AnswerKind.RACE_WINDOW:
        _require_keys(
            payload,
            {
                "answer_version",
                "kind",
                "trace_id",
                "variable",
                "first_event_id",
                "second_event_id",
            },
        )
        return RaceWindowAnswer(
            trace_id=_string(payload, "trace_id"),
            variable=_string(payload, "variable"),
            first_event_id=_string(payload, "first_event_id"),
            second_event_id=_string(payload, "second_event_id"),
        )
    _require_keys(
        payload,
        {
            "answer_version",
            "kind",
            "trace_id",
            "mutex_id",
            "protected_event_ids",
            "invariant",
        },
    )
    invariant = _string(payload, "invariant")
    if invariant != REPAIR_INVARIANT:
        raise MutexRaceContractError("invalid_invariant")
    return RepairInvariantAnswer(
        trace_id=_string(payload, "trace_id"),
        mutex_id=_string(payload, "mutex_id"),
        protected_event_ids=tuple(
            cast(str, event_id)
            for event_id in _sequence(payload["protected_event_ids"])
        ),
        invariant=invariant,
    )


def _event_to_mapping(event: EventSpec) -> dict[str, object]:
    result: dict[str, object] = {"event_id": event.event_id, "kind": event.kind.value}
    if event.kind is EventKind.READ:
        result["register"] = event.register
        result["variable"] = event.variable
    elif event.kind is EventKind.ADD:
        result["integer_delta"] = event.integer_delta
        result["register"] = event.register
    elif event.kind is EventKind.WRITE:
        result["register"] = event.register
        result["variable"] = event.variable
    else:
        result["mutex_id"] = event.mutex_id
    return result


def trace_to_mapping(trace: TraceSpec) -> dict[str, object]:
    return {
        "expected_final_states": [dict(state) for state in trace.expected_final_states],
        "initial_shared_state": dict(trace.initial_shared_state),
        "seed": trace.seed,
        "threads": [
            {
                "events": [_event_to_mapping(event) for event in thread.events],
                "thread_id": thread.thread_id,
            }
            for thread in trace.threads
        ],
        "trace_id": trace.trace_id,
        "trace_version": trace.trace_version,
    }


def canonical_trace_json(trace: TraceSpec) -> str:
    return json.dumps(
        trace_to_mapping(trace),
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
```

- [ ] **Step 5: Run the contract tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_contract.py -q
```

Expected: exit code 0 with `16 passed`.

- [ ] **Step 6: Write the failing execution-engine tests**

Create `backend/tests/unit/test_mutex_race_execution.py` with exactly:

```python
from copy import deepcopy
import json
from pathlib import Path

import pytest

from projectb.application.mutex_race_execution import (
    enumerate_legal_interleavings,
    event_completeness_ok,
    execute_order,
    thread_order_ok,
)
from projectb.domain.learning import MutexRaceContractError, trace_from_mapping


FIXTURE_PATH = Path("backend/tests/fixtures/mutex_race_traces.json")


def load_trace_payload(index: int = 0) -> dict[str, object]:
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return deepcopy(document["traces"][index])


def test_lost_update_enumeration_is_deterministic_and_has_two_final_states() -> None:
    trace = trace_from_mapping(load_trace_payload())
    first = enumerate_legal_interleavings(trace)
    second = enumerate_legal_interleavings(trace)
    assert first == second
    assert {tuple(item.final_state) for item in first} == {
        (("counter", 1),),
        (("counter", 2),),
    }


def test_every_enumerated_order_is_complete_and_preserves_each_thread() -> None:
    trace = trace_from_mapping(load_trace_payload())
    for interleaving in enumerate_legal_interleavings(trace):
        assert event_completeness_ok(trace, interleaving.ordered_event_ids)
        assert thread_order_ok(trace, interleaving.ordered_event_ids)
        assert len(interleaving.ordered_event_ids) == 6


def test_register_and_shared_state_semantics_replay_serial_and_lost_orders() -> None:
    trace = trace_from_mapping(load_trace_payload())
    serial = execute_order(
        trace,
        ("a-read", "a-add", "a-write", "b-read", "b-add", "b-write"),
    )
    lost = execute_order(
        trace,
        ("a-read", "b-read", "a-add", "a-write", "b-add", "b-write"),
    )
    assert serial is not None and tuple(serial.final_state) == (("counter", 2),)
    assert lost is not None and tuple(lost.final_state) == (("counter", 1),)


def test_mutex_owner_semantics_allow_only_final_counter_two() -> None:
    trace = trace_from_mapping(load_trace_payload(1))
    interleavings = enumerate_legal_interleavings(trace)
    assert interleavings
    assert {tuple(item.final_state) for item in interleavings} == {
        (("counter", 2),)
    }


def test_non_owner_unlock_has_no_legal_interleaving() -> None:
    payload = load_trace_payload(1)
    payload["threads"][0]["events"][0] = {
        "kind": "unlock",
        "event_id": "a-lock",
        "mutex_id": "m-counter",
    }
    trace = trace_from_mapping(payload)
    assert enumerate_legal_interleavings(trace) == ()


def test_event_bound_rejects_unbounded_enumeration() -> None:
    payload = load_trace_payload()
    payload["threads"] = [
        {
            "thread_id": f"t-{index:02d}",
            "events": [
                {
                    "kind": "read",
                    "event_id": f"event-{index:02d}",
                    "variable": "counter",
                    "register": f"r-{index:02d}",
                }
            ],
        }
        for index in range(13)
    ]
    payload["expected_final_states"] = [{"counter": 0}]
    trace = trace_from_mapping(payload)
    with pytest.raises(MutexRaceContractError) as caught:
        enumerate_legal_interleavings(trace)
    assert caught.value.code == "trace_too_large"
```

- [ ] **Step 7: Run the execution tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_execution.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.application.mutex_race_execution'`; no test passes.

- [ ] **Step 8: Create the application package marker**

Create `backend/src/projectb/application/__init__.py` with exactly:

```python
"""ProjectB application services."""
```

- [ ] **Step 9: Implement bounded interleaving execution and event helpers**

Create `backend/src/projectb/application/mutex_race_execution.py` with exactly:

```python
from collections.abc import Sequence
from dataclasses import dataclass

from projectb.domain.learning import (
    EventKind,
    EventSpec,
    MutexRaceContractError,
    StateItems,
    TraceSpec,
)


MAX_TRACE_EVENTS = 12
MAX_INTERLEAVINGS = 10_000


@dataclass(frozen=True, slots=True)
class Interleaving:
    ordered_event_ids: Sequence[str]
    final_state: StateItems

    def __post_init__(self) -> None:
        object.__setattr__(self, "ordered_event_ids", tuple(self.ordered_event_ids))
        object.__setattr__(self, "final_state", tuple(self.final_state))


@dataclass(slots=True)
class _Machine:
    shared: dict[str, int]
    registers: dict[str, dict[str, int]]
    mutex_owners: dict[str, str]

    def clone(self) -> "_Machine":
        return _Machine(
            shared=dict(self.shared),
            registers={
                thread_id: dict(registers)
                for thread_id, registers in self.registers.items()
            },
            mutex_owners=dict(self.mutex_owners),
        )


def _new_machine(trace: TraceSpec) -> _Machine:
    return _Machine(
        shared=dict(trace.initial_shared_state),
        registers={thread.thread_id: {} for thread in trace.threads},
        mutex_owners={},
    )


def event_locations(trace: TraceSpec) -> dict[str, tuple[str, int, EventSpec]]:
    return {
        event.event_id: (thread.thread_id, index, event)
        for thread in trace.threads
        for index, event in enumerate(thread.events)
    }


def event_completeness_ok(trace: TraceSpec, ordered_event_ids: Sequence[str]) -> bool:
    expected = tuple(event_locations(trace))
    observed = tuple(ordered_event_ids)
    return len(observed) == len(expected) and set(observed) == set(expected)


def thread_order_ok(trace: TraceSpec, ordered_event_ids: Sequence[str]) -> bool:
    locations = event_locations(trace)
    last_index: dict[str, int] = {}
    for event_id in ordered_event_ids:
        location = locations.get(event_id)
        if location is None:
            return False
        thread_id, index, _ = location
        if index <= last_index.get(thread_id, -1):
            return False
        last_index[thread_id] = index
    return True


def _apply(machine: _Machine, thread_id: str, event: EventSpec) -> bool:
    if event.kind is EventKind.READ:
        if event.variable is None or event.register is None:
            return False
        if event.variable not in machine.shared:
            return False
        machine.registers[thread_id][event.register] = machine.shared[event.variable]
        return True
    if event.kind is EventKind.ADD:
        if event.register is None or event.integer_delta is None:
            return False
        if event.register not in machine.registers[thread_id]:
            return False
        machine.registers[thread_id][event.register] += event.integer_delta
        return True
    if event.kind is EventKind.WRITE:
        if event.variable is None or event.register is None:
            return False
        if event.variable not in machine.shared:
            return False
        if event.register not in machine.registers[thread_id]:
            return False
        machine.shared[event.variable] = machine.registers[thread_id][event.register]
        return True
    if event.mutex_id is None:
        return False
    if event.kind is EventKind.LOCK:
        if event.mutex_id in machine.mutex_owners:
            return False
        machine.mutex_owners[event.mutex_id] = thread_id
        return True
    if machine.mutex_owners.get(event.mutex_id) != thread_id:
        return False
    del machine.mutex_owners[event.mutex_id]
    return True


def execute_order(
    trace: TraceSpec,
    ordered_event_ids: Sequence[str],
) -> Interleaving | None:
    ordered = tuple(ordered_event_ids)
    if not event_completeness_ok(trace, ordered) or not thread_order_ok(trace, ordered):
        return None
    locations = event_locations(trace)
    machine = _new_machine(trace)
    for event_id in ordered:
        thread_id, _, event = locations[event_id]
        if not _apply(machine, thread_id, event):
            return None
    if machine.mutex_owners:
        return None
    return Interleaving(
        ordered_event_ids=ordered,
        final_state=tuple(sorted(machine.shared.items())),
    )


def enumerate_legal_interleavings(trace: TraceSpec) -> tuple:
    event_count = sum(len(thread.events) for thread in trace.threads)
    if event_count > MAX_TRACE_EVENTS:
        raise MutexRaceContractError("trace_too_large")
    positions = {thread.thread_id: 0 for thread in trace.threads}
    results: list[Interleaving] = []

    def visit(machine: _Machine, ordered_event_ids: tuple) -> None:
        if len(ordered_event_ids) == event_count:
            if not machine.mutex_owners:
                results.append(
                    Interleaving(
                        ordered_event_ids=ordered_event_ids,
                        final_state=tuple(sorted(machine.shared.items())),
                    )
                )
                if len(results) > MAX_INTERLEAVINGS:
                    raise MutexRaceContractError("too_many_interleavings")
            return
        for thread in trace.threads:
            position = positions[thread.thread_id]
            if position >= len(thread.events):
                continue
            event = thread.events[position]
            candidate = machine.clone()
            if not _apply(candidate, thread.thread_id, event):
                continue
            positions[thread.thread_id] = position + 1
            visit(candidate, ordered_event_ids + (event.event_id,))
            positions[thread.thread_id] = position

    visit(_new_machine(trace), ())
    return tuple(results)


def event_access(
    trace: TraceSpec,
    event_id: str,
) -> tuple[str, str, str] | None:
    location = event_locations(trace).get(event_id)
    if location is None:
        return None
    thread_id, _, event = location
    if event.kind is EventKind.READ and event.variable is not None:
        return thread_id, event.variable, "read"
    if event.kind is EventKind.WRITE and event.variable is not None:
        return thread_id, event.variable, "write"
    return None


def conflicting_event_pair(
    trace: TraceSpec,
    first_event_id: str,
    second_event_id: str,
    variable: str | None = None,
) -> bool:
    first = event_access(trace, first_event_id)
    second = event_access(trace, second_event_id)
    if first is None or second is None:
        return False
    first_thread, first_variable, first_mode = first
    second_thread, second_variable, second_mode = second
    return (
        first_thread != second_thread
        and first_variable == second_variable
        and (variable is None or first_variable == variable)
        and "write" in (first_mode, second_mode)
    )


def candidate_rmw_spans(trace: TraceSpec) -> tuple:
    spans: list[tuple[str, str, str]] = []
    for thread in trace.threads:
        events = tuple(thread.events)
        for index in range(len(events) - 2):
            read_event, add_event, write_event = events[index : index + 3]
            if (
                read_event.kind is EventKind.READ
                and add_event.kind is EventKind.ADD
                and write_event.kind is EventKind.WRITE
                and read_event.register == add_event.register == write_event.register
                and read_event.variable == write_event.variable
            ):
                spans.append(
                    (
                        read_event.event_id,
                        add_event.event_id,
                        write_event.event_id,
                    )
                )
    return tuple(spans)
```

- [ ] **Step 10: Run the execution tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_execution.py -q
```

Expected: exit code 0 with `6 passed`.

- [ ] **Step 11: Write the failing rubric and evidence-boundary tests**

Create `backend/tests/unit/test_mutex_race_rubric.py` with exactly:

```python
import json
from pathlib import Path

import pytest

from projectb.application.mutex_race_rubric import (
    criterion_status,
    demonstrated_now_eligible,
    evaluate_interleaving,
    evaluate_race_window,
    evaluate_repair_invariant,
    evidence_gate,
)
from projectb.domain.learning import (
    CheckKind,
    CriterionId,
    InterleavingAnswer,
    OracleResult,
    RaceWindowAnswer,
    RepairInvariantAnswer,
    RubricStatus,
    trace_from_mapping,
)


FIXTURE_PATH = Path("backend/tests/fixtures/mutex_race_traces.json")
LOST_ORDER = (
    "a-read",
    "b-read",
    "a-add",
    "a-write",
    "b-add",
    "b-write",
)
PROTECTED_EVENTS = (
    "a-read",
    "a-add",
    "a-write",
    "b-read",
    "b-add",
    "b-write",
)


def load_trace():
    document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return trace_from_mapping(document["traces"][0])


def valid_interleaving_answer() -> InterleavingAnswer:
    return InterleavingAnswer(
        trace_id="lost-update-seed-11",
        ordered_event_ids=LOST_ORDER,
        reported_final_state=(("counter", 1),),
    )


def valid_race_answer() -> RaceWindowAnswer:
    return RaceWindowAnswer(
        trace_id="lost-update-seed-11",
        variable="counter",
        first_event_id="a-read",
        second_event_id="b-write",
    )


def valid_repair_answer() -> RepairInvariantAnswer:
    return RepairInvariantAnswer(
        trace_id="lost-update-seed-11",
        mutex_id="m-counter",
        protected_event_ids=PROTECTED_EVENTS,
        invariant="at_most_one_thread_in_critical_section",
    )


def test_every_result_has_the_five_sorted_criterion_ids() -> None:
    result = evaluate_interleaving(valid_interleaving_answer(), load_trace())
    assert [item.criterion_id.value for item in result.rubric_results] == [
        "event_completeness",
        "final_state",
        "mutual_exclusion_invariant",
        "race_window",
        "thread_order",
    ]


def test_valid_interleaving_passes_only_the_three_isomorphic_criteria() -> None:
    result = evaluate_interleaving(valid_interleaving_answer(), load_trace())
    assert criterion_status(result, CriterionId.THREAD_ORDER) is RubricStatus.PASS
    assert criterion_status(result, CriterionId.EVENT_COMPLETENESS) is RubricStatus.PASS
    assert criterion_status(result, CriterionId.FINAL_STATE) is RubricStatus.PASS
    assert criterion_status(result, CriterionId.RACE_WINDOW) is RubricStatus.NOT_APPLICABLE
    assert (
        criterion_status(result, CriterionId.MUTUAL_EXCLUSION_INVARIANT)
        is RubricStatus.NOT_APPLICABLE
    )


@pytest.mark.parametrize(
    ("case", "expected_failed_criterion"),
    [
        ("thread_order", CriterionId.THREAD_ORDER),
        ("event_completeness", CriterionId.EVENT_COMPLETENESS),
        ("final_state", CriterionId.FINAL_STATE),
    ],
)
def test_interleaving_failures_are_attributed_to_the_exact_criterion(
    case: str,
    expected_failed_criterion: CriterionId,
) -> None:
    ordered = LOST_ORDER
    final_state = (("counter", 1),)
    if case == "thread_order":
        ordered = (
            "a-add",
            "a-read",
            "b-read",
            "a-write",
            "b-add",
            "b-write",
        )
    elif case == "event_completeness":
        ordered = LOST_ORDER[:-1]
    else:
        final_state = (("counter", 2),)
    result = evaluate_interleaving(
        InterleavingAnswer(
            trace_id="lost-update-seed-11",
            ordered_event_ids=ordered,
            reported_final_state=final_state,
        ),
        load_trace(),
    )
    assert criterion_status(result, expected_failed_criterion) is RubricStatus.FAIL


def test_cross_thread_conflicting_access_passes_race_window() -> None:
    result = evaluate_race_window(valid_race_answer(), load_trace())
    assert criterion_status(result, CriterionId.RACE_WINDOW) is RubricStatus.PASS


@pytest.mark.parametrize("case", ["same_thread", "read_read", "wrong_variable"])
def test_nonconflicting_pairs_fail_race_window(case: str) -> None:
    first_event_id = "a-read"
    second_event_id = "b-write"
    variable = "counter"
    if case == "same_thread":
        second_event_id = "a-write"
    elif case == "read_read":
        second_event_id = "b-read"
    else:
        variable = "other"
    result = evaluate_race_window(
        RaceWindowAnswer(
            trace_id="lost-update-seed-11",
            variable=variable,
            first_event_id=first_event_id,
            second_event_id=second_event_id,
        ),
        load_trace(),
    )
    assert criterion_status(result, CriterionId.RACE_WINDOW) is RubricStatus.FAIL


def test_complete_contiguous_rmw_protection_passes_invariant() -> None:
    result = evaluate_repair_invariant(valid_repair_answer(), load_trace())
    assert (
        criterion_status(result, CriterionId.MUTUAL_EXCLUSION_INVARIANT)
        is RubricStatus.PASS
    )


@pytest.mark.parametrize("case", ["missing_span_event", "unknown_event"])
def test_incomplete_or_unknown_protection_fails_invariant(case: str) -> None:
    protected = PROTECTED_EVENTS[:-1]
    if case == "unknown_event":
        protected = PROTECTED_EVENTS + ("provider-suggested-event",)
    result = evaluate_repair_invariant(
        RepairInvariantAnswer(
            trace_id="lost-update-seed-11",
            mutex_id="m-counter",
            protected_event_ids=protected,
            invariant="at_most_one_thread_in_critical_section",
        ),
        load_trace(),
    )
    assert (
        criterion_status(result, CriterionId.MUTUAL_EXCLUSION_INVARIANT)
        is RubricStatus.FAIL
    )


def test_starting_probe_is_never_evidence_and_isomorphic_requires_three_passes() -> None:
    result = evaluate_interleaving(valid_interleaving_answer(), load_trace())
    assert evidence_gate(CheckKind.STARTING_PROBE, (result,)).eligible is False
    assert evidence_gate(CheckKind.ISOMORPHIC, (result,)).eligible is True
    wrong = evaluate_interleaving(
        InterleavingAnswer(
            trace_id="lost-update-seed-11",
            ordered_event_ids=LOST_ORDER,
            reported_final_state=(("counter", 2),),
        ),
        load_trace(),
    )
    assert evidence_gate(CheckKind.ISOMORPHIC, (wrong,)).eligible is False


def test_transfer_requires_race_and_repair_before_demonstrated_now() -> None:
    race_result = evaluate_race_window(valid_race_answer(), load_trace())
    repair_result = evaluate_repair_invariant(valid_repair_answer(), load_trace())
    isomorphic = evidence_gate(
        CheckKind.ISOMORPHIC,
        (evaluate_interleaving(valid_interleaving_answer(), load_trace()),),
    )
    race_only = evidence_gate(CheckKind.TRANSFER, (race_result,))
    transfer = evidence_gate(CheckKind.TRANSFER, (race_result, repair_result))
    assert race_only.eligible is False
    assert transfer.eligible is True
    assert demonstrated_now_eligible(isomorphic, race_only) is False
    assert demonstrated_now_eligible(isomorphic, transfer) is True


def test_oracle_result_has_no_provider_feedback_or_mastery_fields() -> None:
    assert "provider_feedback" not in OracleResult.__dataclass_fields__
    assert "mastery" not in OracleResult.__dataclass_fields__
    first = evaluate_interleaving(valid_interleaving_answer(), load_trace())
    second = evaluate_interleaving(valid_interleaving_answer(), load_trace())
    assert first == second
```

- [ ] **Step 12: Run the rubric tests and capture the expected red result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_rubric.py -q
```

Expected: exit code 2 with collection error `ModuleNotFoundError: No module named 'projectb.application.mutex_race_rubric'`; no test passes.

- [ ] **Step 13: Implement the five-criterion rubric and evidence gates**

Create `backend/src/projectb/application/mutex_race_rubric.py` with exactly:

```python
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

from projectb.application.mutex_race_execution import (
    candidate_rmw_spans,
    conflicting_event_pair,
    event_completeness_ok,
    event_locations,
    execute_order,
    thread_order_ok,
)
from projectb.domain.learning import (
    AnswerKind,
    CheckKind,
    CriterionId,
    InterleavingAnswer,
    MutexRaceAnswer,
    MutexRaceContractError,
    OracleResult,
    RaceWindowAnswer,
    RepairInvariantAnswer,
    RubricResult,
    RubricStatus,
    TraceSpec,
)


CRITERION_ORDER = tuple(sorted(CriterionId, key=lambda item: item.value))


def _oracle_result(
    answer_kind: AnswerKind,
    updates: Mapping[CriterionId, tuple[RubricStatus, str | None]],
) -> OracleResult:
    results = []
    for criterion_id in CRITERION_ORDER:
        status, error_code = updates.get(
            criterion_id,
            (RubricStatus.NOT_APPLICABLE, None),
        )
        results.append(
            RubricResult(
                criterion_id=criterion_id,
                status=status,
                error_code=error_code,
            )
        )
    return OracleResult(answer_kind=answer_kind, rubric_results=tuple(results))


def criterion_status(result: OracleResult, criterion_id: CriterionId) -> RubricStatus:
    for item in result.rubric_results:
        if item.criterion_id is criterion_id:
            return item.status
    raise MutexRaceContractError("criterion_missing")


def evaluate_interleaving(
    answer: InterleavingAnswer,
    trace: TraceSpec,
) -> OracleResult:
    trace_matches = answer.trace_id == trace.trace_id
    order_ok = trace_matches and thread_order_ok(trace, answer.ordered_event_ids)
    complete_ok = trace_matches and event_completeness_ok(
        trace,
        answer.ordered_event_ids,
    )
    execution = (
        execute_order(trace, answer.ordered_event_ids)
        if order_ok and complete_ok
        else None
    )
    final_ok = (
        execution is not None
        and tuple(answer.reported_final_state) == tuple(execution.final_state)
        and tuple(execution.final_state)
        in {tuple(state) for state in trace.expected_final_states}
    )
    return _oracle_result(
        AnswerKind.INTERLEAVING,
        {
            CriterionId.THREAD_ORDER: (
                RubricStatus.PASS if order_ok else RubricStatus.FAIL,
                None if order_ok else "thread_order_invalid",
            ),
            CriterionId.EVENT_COMPLETENESS: (
                RubricStatus.PASS if complete_ok else RubricStatus.FAIL,
                None if complete_ok else "event_set_mismatch",
            ),
            CriterionId.FINAL_STATE: (
                RubricStatus.PASS if final_ok else RubricStatus.FAIL,
                None if final_ok else "final_state_mismatch",
            ),
        },
    )


def evaluate_race_window(
    answer: RaceWindowAnswer,
    trace: TraceSpec,
) -> OracleResult:
    passed = (
        answer.trace_id == trace.trace_id
        and conflicting_event_pair(
            trace,
            answer.first_event_id,
            answer.second_event_id,
            answer.variable,
        )
    )
    return _oracle_result(
        AnswerKind.RACE_WINDOW,
        {
            CriterionId.RACE_WINDOW: (
                RubricStatus.PASS if passed else RubricStatus.FAIL,
                None if passed else "race_window_invalid",
            )
        },
    )


def _protected_events_are_contiguous(
    answer: RepairInvariantAnswer,
    trace: TraceSpec,
) -> bool:
    locations = event_locations(trace)
    positions_by_thread: dict[str, list[int]] = {}
    for event_id in answer.protected_event_ids:
        location = locations.get(event_id)
        if location is None:
            return False
        thread_id, index, _ = location
        positions_by_thread.setdefault(thread_id, []).append(index)
    for positions in positions_by_thread.values():
        ordered = sorted(positions)
        if ordered != list(range(ordered[0], ordered[-1] + 1)):
            return False
    return True


def evaluate_repair_invariant(
    answer: RepairInvariantAnswer,
    trace: TraceSpec,
) -> OracleResult:
    protected = tuple(answer.protected_event_ids)
    protected_set = set(protected)
    spans = candidate_rmw_spans(trace)
    all_spans_covered = bool(spans) and all(
        set(span).issubset(protected_set) for span in spans
    )
    passed = (
        answer.trace_id == trace.trace_id
        and len(protected) == len(protected_set)
        and all_spans_covered
        and _protected_events_are_contiguous(answer, trace)
    )
    return _oracle_result(
        AnswerKind.REPAIR_INVARIANT,
        {
            CriterionId.MUTUAL_EXCLUSION_INVARIANT: (
                RubricStatus.PASS if passed else RubricStatus.FAIL,
                None if passed else "mutual_exclusion_invariant_invalid",
            )
        },
    )


def evaluate_answer(answer: MutexRaceAnswer, trace: TraceSpec) -> OracleResult:
    if isinstance(answer, InterleavingAnswer):
        return evaluate_interleaving(answer, trace)
    if isinstance(answer, RaceWindowAnswer):
        return evaluate_race_window(answer, trace)
    return evaluate_repair_invariant(answer, trace)


@dataclass(frozen=True, slots=True)
class EvidenceGate:
    check_kind: CheckKind
    eligible: bool
    required_criteria: Sequence[CriterionId]
    error_code: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "required_criteria", tuple(self.required_criteria))


def _criterion_passed(result: OracleResult, criterion_id: CriterionId) -> bool:
    return criterion_status(result, criterion_id) is RubricStatus.PASS


def evidence_gate(
    check_kind: CheckKind,
    oracle_results: Sequence[OracleResult],
) -> EvidenceGate:
    results = tuple(oracle_results)
    if check_kind is CheckKind.STARTING_PROBE:
        return EvidenceGate(
            check_kind=check_kind,
            eligible=False,
            required_criteria=(),
            error_code="starting_probe_not_evidence",
        )
    if check_kind is CheckKind.ISOMORPHIC:
        required = (
            CriterionId.THREAD_ORDER,
            CriterionId.EVENT_COMPLETENESS,
            CriterionId.FINAL_STATE,
        )
        eligible = len(results) == 1 and all(
            _criterion_passed(results[0], criterion_id) for criterion_id in required
        )
        return EvidenceGate(
            check_kind=check_kind,
            eligible=eligible,
            required_criteria=required,
            error_code=None if eligible else "isomorphic_criteria_incomplete",
        )
    required = (
        CriterionId.RACE_WINDOW,
        CriterionId.MUTUAL_EXCLUSION_INVARIANT,
    )
    race_passed = any(
        result.answer_kind is AnswerKind.RACE_WINDOW
        and _criterion_passed(result, CriterionId.RACE_WINDOW)
        for result in results
    )
    repair_passed = any(
        result.answer_kind is AnswerKind.REPAIR_INVARIANT
        and _criterion_passed(result, CriterionId.MUTUAL_EXCLUSION_INVARIANT)
        for result in results
    )
    eligible = race_passed and repair_passed
    return EvidenceGate(
        check_kind=check_kind,
        eligible=eligible,
        required_criteria=required,
        error_code=None if eligible else "transfer_criteria_incomplete",
    )


def demonstrated_now_eligible(
    isomorphic_gate: EvidenceGate,
    transfer_gate: EvidenceGate,
) -> bool:
    return (
        isomorphic_gate.check_kind is CheckKind.ISOMORPHIC
        and transfer_gate.check_kind is CheckKind.TRANSFER
        and isomorphic_gate.eligible
        and transfer_gate.eligible
    )
```

- [ ] **Step 14: Run the rubric tests and capture the green result**

Run:

```powershell
$env:PYTHONPATH = (Resolve-Path 'backend/src').Path
python -m pytest backend/tests/unit/test_mutex_race_rubric.py -q
```

Expected: exit code 0 with `15 passed`.
