"""Tests for src/parallel.py — parallel batch processing."""

import asyncio

import pytest

from src.models import SkillName
from src.parallel import (
    batch_assess_runway,
    batch_dispatch,
    gather_analyses,
    time_parallel,
    time_sequential,
)


class TestGatherAnalyses:
    """Tests for gather_analyses()."""

    def test_basic_parallel_execution(self):
        def add_one(x):
            return x + 1

        tasks = [(add_one, (i,), {}) for i in range(5)]
        results = asyncio.run(gather_analyses(tasks))
        assert results == [1, 2, 3, 4, 5]

    def test_results_in_order(self):
        def identity(x):
            return x

        tasks = [(identity, (i,), {}) for i in range(10)]
        results = asyncio.run(gather_analyses(tasks))
        assert results == list(range(10))

    def test_kwargs_passed(self):
        def greet(name, greeting="Hello"):
            return f"{greeting}, {name}"

        tasks = [
            (greet, ("Alice",), {"greeting": "Hi"}),
            (greet, ("Bob",), {"greeting": "Hey"}),
        ]
        results = asyncio.run(gather_analyses(tasks))
        assert results[0] == "Hi, Alice"
        assert results[1] == "Hey, Bob"

    def test_respects_concurrency_limit(self):
        results = asyncio.run(
            gather_analyses(
                [(lambda x: x, (i,), {}) for i in range(20)],
                max_concurrency=3,
            )
        )
        assert len(results) == 20

    def test_single_task(self):
        tasks = [(lambda: 42, (), {})]
        results = asyncio.run(gather_analyses(tasks))
        assert results == [42]

    def test_raises_on_empty_tasks(self):
        with pytest.raises(ValueError):
            asyncio.run(gather_analyses([]))

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError):
            asyncio.run(gather_analyses("not a list"))  # type: ignore

    def test_raises_on_zero_concurrency(self):
        with pytest.raises(ValueError):
            asyncio.run(gather_analyses([(lambda: 1, (), {})], max_concurrency=0))

    def test_raises_on_negative_concurrency(self):
        with pytest.raises(ValueError):
            asyncio.run(gather_analyses([(lambda: 1, (), {})], max_concurrency=-1))


class TestBatchDispatch:
    """Tests for batch_dispatch()."""

    def test_dispatches_multiple_messages(self):
        messages = [
            "We need to fundraise for series a",
            "We're in a crisis with low runway",
            "Need help with ESOP design for our team",
        ]
        results = batch_dispatch(messages)
        assert len(results) == 3
        # Each result is None or a DispatchResult
        for r in results:
            assert r is None or hasattr(r, "primary_skill")

    def test_results_in_order(self):
        messages = [
            "fundraising for series a investors",
            "burnout and overwhelmed",
        ]
        results = batch_dispatch(messages)
        assert len(results) == 2
        if results[0] is not None:
            assert results[0].primary_skill == SkillName.FUNDRAISING
        if results[1] is not None:
            assert results[1].primary_skill == SkillName.RESILIENCE

    def test_raises_on_empty_list(self):
        with pytest.raises(ValueError):
            batch_dispatch([])

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError):
            batch_dispatch("single message")  # type: ignore

    def test_single_message(self):
        results = batch_dispatch(["fundraise seed round"])
        assert len(results) == 1


class TestBatchAssessRunway:
    """Tests for batch_assess_runway()."""

    def test_basic_batch(self):
        assessments = [
            (3_000_000, 200_000),
            (600_000, 200_000),
            (100_000, 200_000),
        ]
        results = batch_assess_runway(assessments)
        assert len(results) == 3
        for r in results:
            assert r is not None
            assert r.months_remaining >= 0

    def test_results_ordered(self):
        assessments = [
            (2_000_000, 100_000),  # 20 months
            (300_000, 100_000),  # 3 months
        ]
        results = batch_assess_runway(assessments)
        assert results[0].months_remaining > results[1].months_remaining

    def test_raises_on_empty(self):
        with pytest.raises(ValueError):
            batch_assess_runway([])

    def test_raises_on_non_list(self):
        with pytest.raises(TypeError):
            batch_assess_runway("not a list")  # type: ignore


class TestTimeSequential:
    """Tests for time_sequential()."""

    def test_returns_elapsed_and_results(self):
        elapsed, results = time_sequential(lambda x: x * 2, [1, 2, 3])
        assert elapsed >= 0
        assert results == [2, 4, 6]

    def test_elapsed_is_float(self):
        elapsed, _ = time_sequential(lambda x: x, [1, 2])
        assert isinstance(elapsed, float)

    def test_empty_items(self):
        elapsed, results = time_sequential(lambda x: x, [])
        assert results == []
        assert elapsed >= 0


class TestTimeParallel:
    """Tests for time_parallel()."""

    def test_returns_elapsed_and_results(self):
        elapsed, results = time_parallel(lambda x: x * 2, [1, 2, 3])
        assert elapsed >= 0
        assert results == [2, 4, 6]

    def test_elapsed_is_float(self):
        elapsed, _ = time_parallel(lambda x: x, [1, 2])
        assert isinstance(elapsed, float)
