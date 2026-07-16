import json

from backend.settings import get_settings


class KnowledgeBaseService:

    def __init__(self):

        settings = get_settings()

        with open(settings.kb_path, "r", encoding="utf-8") as file:
            self.data = json.load(file)

        self.entries = self.data["entries"]

        # Build a set of all recognized medications for O(1) lookup.
        # A medication is "known" if it either:
        #   - appears in the KB as drugA or drugB, OR
        #   - is the generic target of an alias mapping
        # This distinguishes truly unknown drugs (LIMITED) from
        # recognized drugs that simply have no interaction rules yet.
        self.known_drugs: set[str] = set()

        for entry in self.entries:
            self.known_drugs.add(entry["drugA"].lower())
            drug_b = entry.get("drugB")
            if drug_b:
                self.known_drugs.add(drug_b.lower())

        with open(settings.aliases_path, "r", encoding="utf-8") as file:
            aliases_data = json.load(file)

        for generic in aliases_data["aliases"].values():
            self.known_drugs.add(generic.lower())

    @property
    def version(self):
        return self.data["metadata"]["version"]

    @property
    def entry_count(self):
        return len(self.entries)

    def is_known(self, medication_name: str) -> bool:
        """
        Return True if the medication is recognized by the system.

        A medication is considered known if it appears in the KB
        (as drugA or drugB) OR is a canonical generic name that
        has at least one alias mapping.

        Comparison is case-insensitive and whitespace-trimmed.

        Used by RuleEngine to distinguish "no known interaction"
        (SAFE) from "drug not recognized" (LIMITED).
        """
        if not medication_name:
            return False
        return medication_name.strip().lower() in self.known_drugs

    def find_drug_interaction(self, drug_a: str, drug_b: str):

        drug_a = drug_a.lower()
        drug_b = drug_b.lower()

        for entry in self.entries:

            entry_drug_b = entry.get("drugB")
            if not entry_drug_b:
                continue

            a = entry["drugA"].lower()
            b = entry_drug_b.lower()

            if (
                (a == drug_a and b == drug_b)
                or
                (a == drug_b and b == drug_a)
            ):
                return entry

        return None