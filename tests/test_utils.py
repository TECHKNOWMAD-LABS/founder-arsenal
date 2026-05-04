"""Tests for src/utils.py — shared utilities."""

import pytest

from src.utils import (
    retry_with_backoff,
    sanitize_non_negative_float,
    sanitize_positive_float,
    sanitize_string,
    truncate_for_processing,
)


class TestRetryWithBackoff:
    """Tests for retry_with_backoff decorator."""

    def test_succeeds_first_try(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0)
        def always_succeeds():
            nonlocal call_count
            call_count += 1
            return "ok"

        result = always_succeeds()
        assert result == "ok"
        assert call_count == 1

    def test_retries_on_failure(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0)
        def fails_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("fail")
            return "ok"

        result = fails_twice()
        assert result == "ok"
        assert call_count == 3

    def test_raises_after_max_retries(self):
        @retry_with_backoff(max_retries=2, base_delay=0)
        def always_fails():
            raise RuntimeError("always fail")

        with pytest.raises(RuntimeError, match="always fail"):
            always_fails()

    def test_call_count_with_max_retries(self):
        call_count = 0

        @retry_with_backoff(max_retries=2, base_delay=0)
        def fails():
            nonlocal call_count
            call_count += 1
            raise ValueError("fail")

        with pytest.raises(ValueError):
            fails()
        assert call_count == 3  # initial + 2 retries

    def test_only_retries_specified_exceptions(self):
        call_count = 0

        @retry_with_backoff(max_retries=3, base_delay=0, exceptions=(ValueError,))
        def raises_type_error():
            nonlocal call_count
            call_count += 1
            raise TypeError("not retried")

        with pytest.raises(TypeError):
            raises_type_error()
        assert call_count == 1  # Should NOT retry TypeError

    def test_preserves_return_value(self):
        @retry_with_backoff(max_retries=1, base_delay=0)
        def returns_dict():
            return {"key": "value"}

        result = returns_dict()
        assert result == {"key": "value"}

    def test_preserves_function_name(self):
        @retry_with_backoff(max_retries=1, base_delay=0)
        def my_function():
            pass

        assert my_function.__name__ == "my_function"


class TestSanitizeString:
    """Tests for sanitize_string()."""

    def test_normal_string(self):
        assert sanitize_string("hello") == "hello"

    def test_strips_whitespace(self):
        assert sanitize_string("  hello  ") == "hello"

    def test_empty_raises_by_default(self):
        with pytest.raises(ValueError):
            sanitize_string("")

    def test_whitespace_only_raises(self):
        with pytest.raises(ValueError):
            sanitize_string("   ")

    def test_allow_empty(self):
        result = sanitize_string("", allow_empty=True)
        assert result == ""

    def test_too_long_raises(self):
        with pytest.raises(ValueError):
            sanitize_string("x" * 200, max_length=100)

    def test_at_max_length_ok(self):
        result = sanitize_string("x" * 100, max_length=100)
        assert len(result) == 100

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            sanitize_string(None)  # type: ignore

    def test_raises_on_int(self):
        with pytest.raises(TypeError):
            sanitize_string(42)  # type: ignore

    def test_raises_on_list(self):
        with pytest.raises(TypeError):
            sanitize_string(["hello"])  # type: ignore

    def test_custom_name_in_error(self):
        with pytest.raises(ValueError, match="my_param"):
            sanitize_string("", name="my_param")

    def test_unicode_ok(self):
        result = sanitize_string("नमस्ते")
        assert result == "नमस्ते"

    def test_very_long_string_raises(self):
        with pytest.raises(ValueError):
            sanitize_string("x" * (100_001))


class TestSanitizePositiveFloat:
    """Tests for sanitize_positive_float()."""

    def test_positive_int(self):
        assert sanitize_positive_float(5) == 5.0

    def test_positive_float(self):
        assert sanitize_positive_float(3.14) == 3.14

    def test_very_small_positive(self):
        result = sanitize_positive_float(1e-10)
        assert result > 0

    def test_raises_on_zero(self):
        with pytest.raises(ValueError):
            sanitize_positive_float(0)

    def test_raises_on_negative(self):
        with pytest.raises(ValueError):
            sanitize_positive_float(-1.0)

    def test_raises_on_nan(self):
        with pytest.raises(ValueError):
            sanitize_positive_float(float("nan"))

    def test_raises_on_inf(self):
        with pytest.raises(ValueError):
            sanitize_positive_float(float("inf"))

    def test_raises_on_string(self):
        with pytest.raises(TypeError):
            sanitize_positive_float("5")  # type: ignore

    def test_raises_on_none(self):
        with pytest.raises(TypeError):
            sanitize_positive_float(None)  # type: ignore

    def test_returns_float(self):
        result = sanitize_positive_float(5)
        assert isinstance(result, float)


class TestSanitizeNonNegativeFloat:
    """Tests for sanitize_non_negative_float()."""

    def test_zero_ok(self):
        assert sanitize_non_negative_float(0) == 0.0

    def test_positive_ok(self):
        assert sanitize_non_negative_float(5.5) == 5.5

    def test_raises_on_negative(self):
        with pytest.raises(ValueError):
            sanitize_non_negative_float(-0.001)

    def test_raises_on_nan(self):
        with pytest.raises(ValueError):
            sanitize_non_negative_float(float("nan"))

    def test_raises_on_string(self):
        with pytest.raises(TypeError):
            sanitize_non_negative_float("0")  # type: ignore


class TestTruncateForProcessing:
    """Tests for truncate_for_processing()."""

    def test_short_string_unchanged(self):
        assert truncate_for_processing("hello") == "hello"

    def test_at_limit_unchanged(self):
        text = "x" * 4096
        result = truncate_for_processing(text, max_len=4096)
        assert len(result) == 4096

    def test_truncates_long_string(self):
        text = "x" * 5000
        result = truncate_for_processing(text, max_len=4096)
        assert len(result) <= 4096

    def test_truncates_at_word_boundary(self):
        text = "hello world foo bar " * 300
        result = truncate_for_processing(text, max_len=100)
        assert not result.endswith(" ")
        assert len(result) <= 100

    def test_empty_string(self):
        assert truncate_for_processing("") == ""

    def test_custom_max_len(self):
        result = truncate_for_processing("a" * 1000, max_len=10)
        assert len(result) <= 10
