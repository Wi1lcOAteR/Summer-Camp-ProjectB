from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


MasteryState = Literal["unknown", "demonstrated_now", "retained"]
Eligibility = Literal["ready", "stale_source", "system_error"]
Mode = Literal["continuous", "finals"]

BASE_INTERVALS = (1, 3, 7, 14, 30)
FINALS_INTERVALS: dict[str, tuple[int, ...]] = {
    "unknown": (1, 2, 4, 7, 15),
    "demonstrated_now": (1, 3, 6, 11, 23),
    "retained": BASE_INTERVALS,
}


class PlannerError(RuntimeError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True, slots=True)
class ReviewSeed:
    concept_id: str
    mastery_state: MasteryState
    weakness: int
    requested_local_date: date
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    eligibility: Eligibility = "ready"

    def __post_init__(self) -> None:
        if not self.concept_id.strip():
            raise PlannerError("concept_id_invalid")
        if self.mastery_state not in FINALS_INTERVALS:
            raise PlannerError("mastery_state_invalid")
        if type(self.weakness) is not int or self.weakness < 0:
            raise PlannerError("weakness_invalid")
        if isinstance(self.requested_local_date, datetime) or not isinstance(self.requested_local_date, date):
            raise PlannerError("request_date_invalid")
        if self.eligibility not in {"ready", "stale_source", "system_error"}:
            raise PlannerError("eligibility_invalid")
        object.__setattr__(self, "source_refs", self._refs(self.source_refs, "source_refs_invalid"))
        object.__setattr__(self, "evidence_refs", self._refs(self.evidence_refs, "evidence_refs_invalid"))

    @staticmethod
    def _refs(values: tuple[str, ...], code: str) -> tuple[str, ...]:
        normalized = tuple(sorted(set(values)))
        if not normalized or any(not value.strip() for value in normalized):
            raise PlannerError(code)
        return normalized


@dataclass(frozen=True, slots=True)
class PlannedReviewTask:
    task_key: str
    concept_id: str
    due_local_date: date
    duration_minutes: Literal[10]
    weakness: int
    requested_local_date: date
    source_refs: tuple[str, ...]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReviewPlan:
    input_hash: str
    archived: bool
    tasks: tuple[PlannedReviewTask, ...]


class ReviewPolicy:
    def __init__(
        self,
        mode: Mode = "continuous",
        timezone: str = "UTC",
        daily_budget_minutes: int = 30,
        exam_date: date | None = None,
    ) -> None:
        if mode not in {"continuous", "finals"}:
            raise PlannerError("mode_invalid")
        try:
            zone = ZoneInfo(timezone)
        except (ZoneInfoNotFoundError, ValueError):
            raise PlannerError("timezone_invalid") from None
        if type(daily_budget_minutes) is not int or not 10 <= daily_budget_minutes <= 120 or daily_budget_minutes % 5:
            raise PlannerError("budget_invalid")
        if mode == "finals" and exam_date is None:
            raise PlannerError("exam_date_required")
        if mode == "continuous" and exam_date is not None:
            raise PlannerError("exam_date_forbidden")
        if exam_date is not None and (isinstance(exam_date, datetime) or not isinstance(exam_date, date)):
            raise PlannerError("exam_date_invalid")
        self.mode = mode
        self.timezone = timezone
        self.daily_budget_minutes = daily_budget_minutes
        self.exam_date = exam_date
        self._zone = zone

    def plan(self, seeds: tuple[ReviewSeed, ...], *, generated_at: datetime) -> ReviewPlan:
        if not isinstance(generated_at, datetime) or generated_at.tzinfo is None:
            raise PlannerError("generated_at_invalid")
        local_date = generated_at.astimezone(self._zone).date()
        normalized = tuple(sorted(seeds, key=self._seed_identity))
        input_hash = self._input_hash(normalized, local_date)
        if self.mode == "finals" and self.exam_date is not None and self.exam_date < local_date:
            return ReviewPlan(input_hash, True, ())

        collapsed: dict[tuple[str, date], PlannedReviewTask] = {}
        for item in normalized:
            if item.eligibility != "ready":
                continue
            intervals = BASE_INTERVALS if self.mode == "continuous" else FINALS_INTERVALS[item.mastery_state]
            for interval in intervals:
                due = local_date + timedelta(days=interval)
                if self.mode == "continuous" and due > local_date + timedelta(days=30):
                    continue
                if self.mode == "finals" and self.exam_date is not None and due > self.exam_date:
                    continue
                candidate = PlannedReviewTask(
                    task_key=self._task_key(item, due),
                    concept_id=item.concept_id,
                    due_local_date=due,
                    duration_minutes=10,
                    weakness=item.weakness,
                    requested_local_date=item.requested_local_date,
                    source_refs=item.source_refs,
                    evidence_refs=item.evidence_refs,
                )
                key = (item.concept_id, due)
                current = collapsed.get(key)
                if current is None or self._priority(candidate) < self._priority(current):
                    collapsed[key] = candidate

        capacity = self.daily_budget_minutes // 10
        by_date: dict[date, list[PlannedReviewTask]] = {}
        for task in collapsed.values():
            by_date.setdefault(task.due_local_date, []).append(task)
        selected: list[PlannedReviewTask] = []
        for due in sorted(by_date):
            selected.extend(sorted(by_date[due], key=self._priority)[:capacity])
        return ReviewPlan(input_hash, False, tuple(selected))

    @staticmethod
    def _seed_identity(item: ReviewSeed) -> tuple[object, ...]:
        return (
            item.concept_id,
            item.mastery_state,
            item.weakness,
            item.requested_local_date,
            item.source_refs,
            item.evidence_refs,
            item.eligibility,
        )

    @staticmethod
    def _priority(task: PlannedReviewTask) -> tuple[object, ...]:
        return (-task.weakness, task.requested_local_date, task.concept_id, task.evidence_refs, task.source_refs)

    @staticmethod
    def _task_key(item: ReviewSeed, due: date) -> str:
        payload = {
            "concept_id": item.concept_id,
            "due_local_date": due.isoformat(),
            "evidence_refs": item.evidence_refs,
            "source_refs": item.source_refs,
        }
        canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True)
        return "review-" + hashlib.sha256(canonical.encode()).hexdigest()

    def _input_hash(self, seeds: tuple[ReviewSeed, ...], local_date: date) -> str:
        payload = {
            "daily_budget_minutes": self.daily_budget_minutes,
            "exam_date": None if self.exam_date is None else self.exam_date.isoformat(),
            "generated_local_date": local_date.isoformat(),
            "mode": self.mode,
            "policy_version": 1,
            "seeds": [asdict(item) for item in seeds],
            "timezone": self.timezone,
        }
        canonical = json.dumps(payload, ensure_ascii=True, separators=(",", ":"), sort_keys=True, default=str)
        return hashlib.sha256(canonical.encode()).hexdigest()
