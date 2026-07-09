from pydantic import BaseModel


class AnalyzeRequest(BaseModel):

    currentMedications: list[str]

    newMedication: str