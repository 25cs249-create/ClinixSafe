import type { RiskLevel } from "../types";

export interface DemoScenario {
  id: string;
  name: string;
  age: number;
  currentMedications: string;
  newMedication: string;
  expectedOutcome: RiskLevel;
}

export const DEMO_SCENARIOS: DemoScenario[] = [
  {
    id: "1",
    name: "Ravi Kumar",
    age: 67,
    currentMedications: "warfarin",
    newMedication: "ibuprofen",
    expectedOutcome: "HIGH",
  },
  {
    id: "2",
    name: "Priya Sharma",
    age: 48,
    currentMedications: "",
    newMedication: "lisinopril",
    expectedOutcome: "SAFE",
  },
  {
    id: "3",
    name: "Mohammed Asif",
    age: 50,
    currentMedications: "",
    newMedication: "zylofexamine",
    expectedOutcome: "LIMITED",
  },
];