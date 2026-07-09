import json

from backend.settings import get_settings


class KnowledgeBaseService:

    def __init__(self):

        settings = get_settings()

        with open(settings.kb_path, "r") as file:
            self.data = json.load(file)

        self.entries = self.data["entries"]

    @property
    def version(self):
        return self.data["metadata"]["version"]

    @property
    def entry_count(self):
        return len(self.entries)

    def find_drug_interaction(self, drug_a: str, drug_b: str):

        drug_a = drug_a.lower()
        drug_b = drug_b.lower()

        for entry in self.entries:

            if entry["drugB"] is None:
                continue

            a = entry["drugA"].lower()
            b = entry["drugB"].lower()

            if (
                (a == drug_a and b == drug_b)
                or
                (a == drug_b and b == drug_a)
            ):
                return entry

        return None