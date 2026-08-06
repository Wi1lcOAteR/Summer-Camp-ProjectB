from __future__ import annotations


class ApiError(RuntimeError):
    def __init__(
        self,
        code: str,
        status_code: int,
        *,
        retryable: bool = False,
        next_action: str = "check_request",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.status_code = status_code
        self.retryable = retryable
        self.next_action = next_action
