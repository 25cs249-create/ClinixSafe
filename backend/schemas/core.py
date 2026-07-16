from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    MONITOR = "MONITOR"
    REVIEW = "REVIEW"
    HIGH = "HIGH"
    CONTRAINDICATED = "CONTRAINDICATED"
    LIMITED = "LIMITED"


class EvidenceStrength(str, Enum):
    HIGH = "HIGH"
    MODERATE = "MODERATE"
    LIMITED = "LIMITED"


class CommunicationType(str, Enum):
    CLINICIAN = "CLINICIAN"
    PATIENT = "PATIENT"
    FOLLOW_UP = "FOLLOW_UP"


class ObservationType(str, Enum):
    EGFR = "eGFR"
    CREATININE = "Creatinine"
    ALT = "ALT"
    AST = "AST"
    POTASSIUM = "Potassium"


class Condition(BaseModel):
    name: str
    status: str


class Allergy(BaseModel):
    allergen: str
    reaction: str
    severity: str


class Patient(BaseModel):
    id: str
    fullName: str
    age: int
    sex: str

    conditions: list[Condition] = []
    allergies: list[Allergy] = []


class Medication(BaseModel):
    id: str
    genericName: str
    drugClass: Optional[str] = None


class Observation(BaseModel):
    type: ObservationType
    value: float
    unit: str

    effectiveDateTime: datetime


class EvidenceTrace(BaseModel):
    evidenceId: str

    title: str

    description: str

    source: str

    sourceType: str

    priority: str


class ToolCall(BaseModel):
    name: str

    status: str

    model: Optional[str] = None

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    requestId: str = Field(
        default_factory=lambda: f"REQ-{uuid4().hex[:8].upper()}"
    )


class CommunicationDraft(BaseModel):
    type: CommunicationType

    title: str

    content: str

    reviewRequired: bool = True


class SafetyReport(BaseModel):

    reportId: str = Field(
        default_factory=lambda: f"REP-{uuid4().hex[:8].upper()}"
    )

    analysisVersion: str

    knowledgeBaseVersion: str

    riskLevel: RiskLevel

    evidenceStrength: EvidenceStrength

    summary: str

    recommendations: list[str] = []

    alternativeMedications: list[str] = []

    evidenceTrace: list[EvidenceTrace] = []

    warnings: list[str] = []

    toolCalls: list[ToolCall] = []

    communicationDrafts: list[CommunicationDraft] = []

    generatedAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

