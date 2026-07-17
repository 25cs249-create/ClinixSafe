"""
Alias Resolver — Indian medication brand-name to generic-name normalization.

Loads a static mapping of brand names to generic names from
medication_aliases.json and provides deterministic name resolution.

Used by the RuleEngine to normalize medication inputs before
knowledge base lookups, so that a judge typing "Crocin 650"
gets the same result as a judge typing "paracetamol".

Design:
    - Deterministic: same input always produces same output.
    - Strict matching: strip whitespace, lowercase, exact dict lookup.
    - No fuzzy matching, no spelling correction.
    - Unknown medication names are returned unchanged (normalized).
      The RuleEngine decides how to interpret unresolved names.
    - Loaded once at startup. Missing or malformed data fails loudly
      at boot rather than silently at request time.
"""

import json
from pathlib import Path

from  settings import get_settings


class AliasResolver:
    """Resolves medication brand names to their canonical generic names."""

    def __init__(self, aliases_path: Path | None = None):
        path = aliases_path or get_settings().aliases_path

        with path.open("r", encoding="utf-8") as file:
            self.data = json.load(file)

        # Keys in the JSON are already normalized (lowercase, trimmed).
        self.aliases: dict[str, str] = self.data["aliases"]

    @property
    def version(self) -> str:
        return self.data["metadata"]["version"]

    @property
    def alias_count(self) -> int:
        return len(self.aliases)

    def resolve(self, medication_name: str) -> str:
        """
        Return the canonical generic name for a medication.

        If the normalized input matches a known brand alias,
        return the mapped generic name. Otherwise, return the
        normalized input unchanged.

        Normalization: strip whitespace, lowercase.
        """
        normalized = medication_name.strip().lower()

        if not normalized:
            return ""

        return self.aliases.get(normalized, normalized)