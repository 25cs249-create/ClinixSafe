import json
from pathlib import Path

from backend.settings import get_settings


class KnowledgeBaseService:

    def __init__(self):
        settings = get_settings()

        with open(settings.kb_path, "r") as file:
            self.data = json.load(file)

    @property
    def version(self):
        return self.data["metadata"]["version"]

    @property
    def entry_count(self):
        return len(self.data["entries"])