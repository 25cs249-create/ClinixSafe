"""
Unit tests for AliasResolver.

Tests the alias resolution contract in isolation:
    - JSON loads correctly at startup
    - Known brand names resolve to their generic equivalents
    - Normalization: strip whitespace, lowercase
    - Unknown medications pass through unchanged (normalized)
    - Empty and whitespace-only inputs return empty string
    - Behavior is deterministic
"""

import pytest

from backend.services.alias_resolver import AliasResolver


@pytest.fixture(scope="module")
def resolver():
    """One resolver instance shared across all tests in this module."""
    return AliasResolver()


# ─── Loader ──────────────────────────────────────────────────────────

def test_loader_exposes_version(resolver):
    assert resolver.version == "1.0.0"


def test_loader_exposes_alias_count(resolver):
    """
    Verifies alias_count reflects the actual JSON contents.
    Does not hardcode a specific number — the count grows over time.
    """
    assert resolver.alias_count > 0
    assert resolver.alias_count == len(resolver.aliases)


# ─── Basic resolution ────────────────────────────────────────────────

def test_resolves_known_brand_to_generic(resolver):
    assert resolver.resolve("crocin") == "paracetamol"


def test_resolves_case_insensitively(resolver):
    assert resolver.resolve("CROCIN") == "paracetamol"


def test_resolves_with_leading_and_trailing_whitespace(resolver):
    assert resolver.resolve(" Crocin ") == "paracetamol"


def test_resolves_with_mixed_case_and_whitespace(resolver):
    """Combined trim + case normalization for a multi-word brand."""
    assert resolver.resolve("   DOLO 650   ") == "paracetamol"


# ─── Passthrough behavior ────────────────────────────────────────────

def test_generic_name_passes_through_unchanged(resolver):
    assert resolver.resolve("warfarin") == "warfarin"


def test_unknown_medication_passes_through_normalized(resolver):
    assert resolver.resolve("Zylofexamine") == "zylofexamine"


# ─── Edge cases ──────────────────────────────────────────────────────

def test_empty_string_returns_empty(resolver):
    assert resolver.resolve("") == ""


def test_whitespace_only_returns_empty(resolver):
    assert resolver.resolve("   ") == ""


# ─── India-specific coverage ─────────────────────────────────────────

def test_combiflam_resolves_to_ibuprofen(resolver):
    """
    Combiflam is a fixed-dose combination (ibuprofen + paracetamol).
    Currently mapped to ibuprofen only — the interacting component.
    FUTURE ENHANCEMENT: proper FDC decomposition to also flag paracetamol.
    """
    assert resolver.resolve("combiflam") == "ibuprofen"


def test_multi_word_brand_with_strength_resolves(resolver):
    assert resolver.resolve("brufen 400") == "ibuprofen"


# ─── Determinism ─────────────────────────────────────────────────────

def test_same_input_produces_same_output(resolver):
    """The resolver is deterministic — no randomness, no state changes."""
    first = resolver.resolve("Crocin")
    second = resolver.resolve("Crocin")
    third = resolver.resolve("Crocin")
    assert first == second == third == "paracetamol"