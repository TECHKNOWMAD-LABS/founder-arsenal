"""
Parallel execution engine for Founder Arsenal.

Provides async batch processing for running multiple founder analyses
concurrently using asyncio.gather with a semaphore for rate limiting.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Coroutine, Optional, TypeVar

T = TypeVar("T")

# Default concurrency limit
DEFAULT_SEMAPHORE = 8


async def run_with_semaphore(
    semaphore: asyncio.Semaphore,
    func: Callable[..., T],
    *args: Any,
    **kwargs: Any,
) -> T:
    """
    Run a synchronous function under an asyncio semaphore.

    Args:
        semaphore: Semaphore to limit concurrency.
        func: Synchronous callable to run.
        *args: Positional arguments for func.
        **kwargs: Keyword arguments for func.

    Returns:
        Return value of func(*args, **kwargs).
    """
    async with semaphore:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))


async def gather_analyses(
    tasks: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]],
    *,
    max_concurrency: int = DEFAULT_SEMAPHORE,
) -> list[Any]:
    """
    Run multiple analysis functions concurrently.

    Each task is a (function, args, kwargs) tuple. All tasks run concurrently
    up to max_concurrency limit.

    Args:
        tasks: List of (callable, args_tuple, kwargs_dict) to run in parallel.
        max_concurrency: Maximum concurrent executions (default 8).

    Returns:
        List of results in the same order as input tasks.

    Raises:
        ValueError: If tasks is empty or max_concurrency is not positive.
        TypeError: If tasks is not a list.
    """
    if not isinstance(tasks, list):
        raise TypeError(f"tasks must be a list, got {type(tasks).__name__}")
    if not tasks:
        raise ValueError("tasks must not be empty")
    if not isinstance(max_concurrency, int) or max_concurrency <= 0:
        raise ValueError(f"max_concurrency must be a positive int, got {max_concurrency}")

    semaphore = asyncio.Semaphore(max_concurrency)
    coroutines = [
        run_with_semaphore(semaphore, fn, *args, **kwargs)
        for fn, args, kwargs in tasks
    ]
    return list(await asyncio.gather(*coroutines))


def batch_dispatch(
    messages: list[str],
    *,
    max_concurrency: int = DEFAULT_SEMAPHORE,
) -> list[Any]:
    """
    Dispatch multiple messages concurrently using asyncio.gather.

    This is the parallel version of dispatcher.dispatch(). For N messages,
    this runs all dispatches concurrently instead of sequentially.

    Args:
        messages: List of founder messages to dispatch.
        max_concurrency: Concurrency limit (default 8).

    Returns:
        List of DispatchResult (or None) in input order.

    Raises:
        TypeError: If messages is not a list.
        ValueError: If messages is empty.
    """
    from .dispatcher import dispatch

    if not isinstance(messages, list):
        raise TypeError(f"messages must be a list, got {type(messages).__name__}")
    if not messages:
        raise ValueError("messages must not be empty")

    tasks = [(dispatch, (msg,), {}) for msg in messages]
    return asyncio.run(gather_analyses(tasks, max_concurrency=max_concurrency))


def batch_assess_runway(
    assessments: list[tuple[float, float]],
    *,
    max_concurrency: int = DEFAULT_SEMAPHORE,
) -> list[Any]:
    """
    Run multiple runway assessments concurrently.

    Args:
        assessments: List of (cash_on_hand, monthly_burn) tuples.
        max_concurrency: Concurrency limit.

    Returns:
        List of RunwayAssessment results in input order.
    """
    from .crisis import assess_runway

    if not isinstance(assessments, list):
        raise TypeError(f"assessments must be a list, got {type(assessments).__name__}")
    if not assessments:
        raise ValueError("assessments must not be empty")

    tasks = [(assess_runway, (cash, burn), {}) for cash, burn in assessments]
    return asyncio.run(gather_analyses(tasks, max_concurrency=max_concurrency))


def time_sequential(fn: Callable, items: list, **kwargs: Any) -> tuple[float, list]:
    """
    Run fn(item, **kwargs) for each item sequentially and measure elapsed time.

    Returns:
        (elapsed_seconds, results)
    """
    start = time.perf_counter()
    results = [fn(item, **kwargs) for item in items]
    return time.perf_counter() - start, results


def time_parallel(
    fn: Callable,
    items: list,
    max_concurrency: int = DEFAULT_SEMAPHORE,
    **kwargs: Any,
) -> tuple[float, list]:
    """
    Run fn(item, **kwargs) for each item in parallel and measure elapsed time.

    Returns:
        (elapsed_seconds, results)
    """
    tasks = [(fn, (item,), kwargs) for item in items]
    start = time.perf_counter()
    results = asyncio.run(gather_analyses(tasks, max_concurrency=max_concurrency))
    return time.perf_counter() - start, results
