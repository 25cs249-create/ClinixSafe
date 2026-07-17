import axios from "axios";
import type { AnalyzeRequest, SafetyReport } from "../types";

const API_BASE =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const client = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { "Content-Type": "application/json "},
});

export class BackendUnavailableError extends Error {
  constructor() {
    super("Backend unavailable");
    this.name = "BackendUnavailableError";
  }
}

export async function analyzeMedication(
  request: AnalyzeRequest
): Promise<SafetyReport> {
  try {
    const res = await client.post("/api/v1/analyze", request);
    return res.data;
  } catch (error) {
    if (axios.isAxiosError(error) && !error.response) {
      throw new BackendUnavailableError();
    }
    throw error;
  }
}