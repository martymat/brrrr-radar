from dataclasses import dataclass
from typing import Any, Optional, Dict

@dataclass
class ApiError(Exception):
    code: str
    message: str
    status: int = 400
    details: Optional[Dict[str, Any]] = None


def error_response(
    code: str,
    message: str,
    status: int,
    details: Optional[Dict[str, Any]] = None,
):
    payload = {
        "error": {
            "code": code,
            "message": message,
        }
    }

    if details is not None:
        payload["error"]["details"] = details

    return payload, status
