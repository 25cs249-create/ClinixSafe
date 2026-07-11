export type RiskLevel =
  | "SAFE"
  | "MONITOR"
  | "REVIEW"
  | "HIGH"
  | "CONTRAINDICATED"
  | "LIMITED";

export type EvidenceStrength = "HIGH" | "MODERATE" | "LIMITED";

export type SourceType =
  | "FDA_LABEL"
  | "GUIDELINE"
  | "INTERACTION_DB"
  | "CLINICAL_DATA";

export type Priority = "HIGH" | "MEDIUM" | "LOW";

export interface EvidenceTrace {
  evidenceId: string;
  title: string;
  description: string;
  source: string;
  sourceType: SourceType;
  priority: Priority;
}

export interface SafetyReport {
  riskLevel: RiskLevel;
  summary: string;
  recommendations: string[];

  reportId?: string;
  analysisVersion?: string;
  knowledgeBaseVersion?: string;
  evidenceStrength?: EvidenceStrength;
  alternativeMedications?: string[];
  evidenceTrace?: EvidenceTrace[];
  warnings?: string[];
  generatedAt?: string;
}

export interface AnalyzeRequest {
  currentMedications: string[];
  newMedication: string;
}