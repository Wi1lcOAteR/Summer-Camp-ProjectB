from __future__ import annotations

from collections import defaultdict

from projectb.domain.learning.evaluators.schemas import (
    DeadlockAnswer,
    DeadlockExercise,
    EvaluationRequest,
    EvaluationResult,
    Outcome,
    RubricItem,
)


def _canonical_cycle(cycle: tuple[str, ...]) -> tuple[str, ...]:
    if not cycle:
        return ()
    rotations = tuple(cycle[index:] + cycle[:index] for index in range(len(cycle)))
    return min(rotations)


def _find_cycle(graph: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    visited: set[str] = set()
    active: list[str] = []
    positions: dict[str, int] = {}

    def visit(node: str) -> tuple[str, ...]:
        if node in positions:
            return _canonical_cycle(tuple(active[positions[node] :]))
        if node in visited:
            return ()
        visited.add(node)
        positions[node] = len(active)
        active.append(node)
        for neighbor in graph.get(node, ()):
            cycle = visit(neighbor)
            if cycle:
                return cycle
        active.pop()
        positions.pop(node)
        return ()

    for node in sorted(graph):
        cycle = visit(node)
        if cycle:
            return cycle
    return ()


def _is_valid_cycle(graph: dict[str, tuple[str, ...]], cycle: tuple[str, ...]) -> bool:
    if not cycle or len(set(cycle)) != len(cycle):
        return False
    return all(cycle[(index + 1) % len(cycle)] in graph.get(node, ()) for index, node in enumerate(cycle))


class DeadlockEvaluator:
    evaluator_id = "os.deadlock.v1"
    version = "1"

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        if request.evaluator_id != self.evaluator_id:
            raise ValueError("evaluator_mismatch")
        if not isinstance(request.exercise, DeadlockExercise) or not isinstance(request.answer, DeadlockAnswer):
            raise ValueError("deadlock_schema_invalid")

        holders: dict[str, str] = {}
        well_formed = True
        for claim in request.exercise.holds:
            if claim.resource_id in holders:
                well_formed = False
            else:
                holders[claim.resource_id] = claim.thread_id
        graph_sets: defaultdict[str, set[str]] = defaultdict(set)
        seen_waits: set[tuple[str, str]] = set()
        for claim in request.exercise.waits:
            pair = (claim.thread_id, claim.resource_id)
            holder = holders.get(claim.resource_id)
            if pair in seen_waits or holder == claim.thread_id:
                well_formed = False
            seen_waits.add(pair)
            if holder is not None and holder != claim.thread_id:
                graph_sets[claim.thread_id].add(holder)
        graph = {node: tuple(sorted(neighbors)) for node, neighbors in graph_sets.items()}
        cycle = _find_cycle(graph) if well_formed else ()
        has_deadlock = bool(cycle)
        classification_matches = request.answer.has_deadlock == has_deadlock
        answer_cycle = _canonical_cycle(request.answer.cycle)
        cycle_matches = _is_valid_cycle(graph, answer_cycle) if has_deadlock else not answer_cycle
        progress_matches = classification_matches
        rubric = tuple(
            sorted(
                (
                    RubricItem("cycle_matches", cycle_matches, "wait_for_cycle_checked"),
                    RubricItem("deadlock_classification_matches", classification_matches, "classification_checked"),
                    RubricItem("graph_well_formed", well_formed, "hold_wait_checked"),
                    RubricItem("progress_assessment_matches", progress_matches, "progress_checked"),
                ),
                key=lambda item: item.code,
            )
        )
        outcome: Outcome
        if not well_formed:
            outcome = "refused"
        elif classification_matches and cycle_matches:
            outcome = "passed"
        elif classification_matches:
            outcome = "partial"
        else:
            outcome = "incorrect"
        return EvaluationResult(
            self.evaluator_id,
            self.version,
            request.check_kind,
            request.variant_id,
            request.source_locator_ids,
            outcome,
            rubric,
        )
