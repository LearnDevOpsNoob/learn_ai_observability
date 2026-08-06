import secrets
from contextvars import ContextVar

correlation_id: ContextVar[str] = ContextVar("correlation_id", default="")

def new_correlation_id() -> str:
    cid = secrets.token_hex(16)   # 16 bytes -> 32 hex chars
    correlation_id.set(cid)
    return cid


def get_correlation_id() -> str:
    return correlation_id.get()