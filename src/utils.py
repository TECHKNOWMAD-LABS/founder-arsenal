"""
Shared utilities: retry logic, timeout handling, and input sanitization.
"""

from __future__ import annotations

import functools
import math
import time
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

# Maximum string length accepted for any public API input
MAX_STR_LEN = 100_000

# Default retry config
DEFAULT_MAX_RETRIES = 3
DEFAULT_BASE_DELAY = 0.5  # seconds
DEFAULT_MAX_DELAY = 10.0  # seconds
DEFAULT_TIMEOUT = 30.0  # seconds


def retry_with_backoff(
    max_retries: int = DEFAULT_MAX_RETRIES,
    base_delay: float = DEFAULT_BASE_DELAY,
    max_delay: float = DEFAULT_MAX_DELAY,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Decorator: retry a function up to max_retries times with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts (default 3).
        base_delay: Initial delay in seconds (default 0.5).
        max_delay: Maximum delay cap in seconds (default 10).
        exceptions: Exception types to catch and retry on.

    Returns:
        Decorated function that retries on specified exceptions.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Exception | None = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_retries:
                        delay = min(base_delay * (2**attempt), max_delay)
                        time.sleep(delay)
            raise last_exc  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator


def sanitize_string(
    value: Any,
    name: str = "input",
    *,
    max_length: int = MAX_STR_LEN,
    allow_empty: bool = False,
) -> str:
    """
    Validate and sanitize a string input.

    - Raises TypeError if value is not a str.
    - Raises ValueError if value is empty (unless allow_empty=True).
    - Raises ValueError if value exceeds max_length.
    - Strips leading/trailing whitespace.

    Args:
        value: The value to sanitize.
        name: Parameter name for error messages.
        max_length: Maximum allowed string length.
        allow_empty: If True, allow empty strings after stripping.

    Returns:
        Sanitized string value.

    Raises:
        TypeError: If value is not a string.
        ValueError: If string is empty or too long.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    value = value.strip()
    if not allow_empty and not value:
        raise ValueError(f"{name} must not be empty")
    if len(value) > max_length:
        raise ValueError(f"{name} exceeds maximum length of {max_length} characters")
    return value


def sanitize_positive_float(value: Any, name: str = "value") -> float:
    """
    Validate a value is a positive finite float.

    Raises:
        TypeError: If value is not numeric.
        ValueError: If value is not finite or not positive.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, got {value}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def sanitize_non_negative_float(value: Any, name: str = "value") -> float:
    """
    Validate a value is a non-negative finite float.

    Raises:
        TypeError: If value is not numeric.
        ValueError: If value is not finite or is negative.
    """
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, got {value}")
    if value < 0:
        raise ValueError(f"{name} must be non-negative, got {value}")
    return value


def truncate_for_processing(text: str, max_len: int = 4096) -> str:
    """
    Safely truncate a string for processing.

    Args:
        text: Input text.
        max_len: Maximum length before truncation.

    Returns:
        Truncated string (at word boundary if possible).
    """
    if len(text) <= max_len:
        return text
    # Try to truncate at word boundary
    truncated = text[:max_len]
    last_space = truncated.rfind(" ")
    if last_space > max_len // 2:
        return truncated[:last_space]
    return truncated
