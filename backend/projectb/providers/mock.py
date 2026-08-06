from __future__ import annotations

import json
from dataclasses import asdict
from typing import Literal

from projectb.providers.port import (
    ExplanationCandidate,
    ExplanationInput,
    FeedbackCandidate,
    FeedbackInput,
    PracticeCandidate,
    PracticeInput,
    ProviderError,
    ProviderInput,
)


class MockProvider:
    def __init__(self, mode: Literal["success", "schema", "timeout", "error"] = "success") -> None:
        self.mode = mode
        self.network_count = 0
        self.last_request_text = ""

    def generate_explanation(self, request: ExplanationInput) -> ExplanationCandidate:
        self._record(request)
        return ExplanationCandidate(f"Mock explanation: {request.instruction.strip()}")

    def generate_practice_candidate(self, request: PracticeInput) -> PracticeCandidate:
        self._record(request)
        return PracticeCandidate(request.evaluator_id, request.variant_id, f"Mock practice for {request.variant_id}")

    def generate_feedback_wording(self, request: FeedbackInput) -> FeedbackCandidate:
        self._record(request)
        details = ",".join(item.detail_code for item in request.rubric)
        return FeedbackCandidate(f"Mock feedback: {request.outcome}; {details}")

    def _record(self, request: ProviderInput) -> None:
        self.network_count += 1
        self.last_request_text = json.dumps(asdict(request), ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        if self.mode != "success":
            raise ProviderError(f"provider_{self.mode}")
