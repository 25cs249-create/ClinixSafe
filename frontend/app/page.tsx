"use client";

import { useState } from "react";
import type { SafetyReport } from "./types";
import { analyzeMedication, BackendUnavailableError } from "./lib/api";
import { SafetyResult } from "../components/SafetyResult";

type AppState =  "idle"|  "loading"|  "success"| "error";

export default function Home() {
  const [currentMedications, setCurrentMedications] = useState("");
  const [newMedication, setNewMedication] = useState("");
  const [state, setState] = useState<AppState>("idle");
  const [report, setReport] = useState<SafetyReport | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!newMedication.trim()) return;

    setState("loading");
    setReport(null);
    setErrorMessage("");

    const currentMeds = currentMedications
      .split(",")
      .map((m) => m.trim().toLowerCase())
      .filter(Boolean);

    try {
      const result = await analyzeMedication({
        currentMedications: currentMeds,
        newMedication: newMedication.trim().toLowerCase(),
      });
      setReport(result);
      setState("success");
    } catch (error) {
      if (error instanceof BackendUnavailableError) {
        setErrorMessage(
          "Backend unavailable. Ensure the API server is running on port 8000."
        );
      } else {
        setErrorMessage("Analysis failed. Please try again.");
      }
      setState("error");
    }
  }

  function handleReset() {
    setCurrentMedications("");
    setNewMedication("");
    setReport(null);
    setState("idle");
    setErrorMessage("");
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-gray-900">ClinixSafe</h1>
            <p className="text-xs text-gray-500 mt-0.5">
              AI Medication Safety Verification
            </p>
          </div>
          <span className="text-xs px-2 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 font-medium">
            Prototype · Not for clinical use
          </span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">

          <section>
            <h2 className="text-lg font-semibold text-gray-900 mb-5">
              Verify Medication Safety
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label
                  htmlFor="currentMeds"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Current Medications
                </label>
                <input
                  id="currentMeds"
                  type="text"
                  value={currentMedications}
                  onChange={(e) => setCurrentMedications(e.target.value)}
                  placeholder="warfarin, metformin"
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <p className="text-xs text-gray-400 mt-1">Comma-separated</p>
              </div>

              <div>
                <label
                  htmlFor="newMed"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  New Medication <span className="text-red-500">*</span>
                </label>
                <input
                  id="newMed"
                  type="text"
                  value={newMedication}
                  onChange={(e) => setNewMedication(e.target.value)}
                  placeholder="ibuprofen"
                  required
                  className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="flex gap-3 pt-1">
                <button
                  type="submit"
                  disabled={state ===  "loading"|| !newMedication.trim()}
                  className="flex-1 bg-blue-600 text-white font-semibold py-2.5 px-4 rounded-lg text-sm hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {state ===  "loading"? "Analyzing... ": "Verify Medication"}
                </button>
                {state !==  "idle"&& (
                  <button
                    type="button"
                    onClick={handleReset}
                    className="px-4 py-2.5 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 text-sm"
                  >
                    Reset
                  </button>
                )}
              </div>
            </form>
          </section>

          <section aria-live="polite">
            {state ===  "idle"&& (
              <div className="flex flex-col items-center justify-center min-h-64 text-center py-12">
                <div className="text-5xl mb-4">🛡️</div>
                <h2 className="text-base font-medium text-gray-700 mb-2">
                  Ready to verify.
                </h2>
                <p className="text-sm text-gray-400 max-w-xs">
                  Enter medications and click Verify to begin.
                </p>
              </div>
            )}

            {state ===  "loading"&& (
              <div className="flex flex-col items-center justify-center min-h-64 py-12">
                <div className="w-10 h-10 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin mb-5 "/>
                <p className="text-gray-700 font-medium text-sm">
                  Analyzing medication safety...
                </p>
              </div>
            )}

            {state ===  "error"&& (
              <div className="flex flex-col items-center justify-center min-h-64 text-center py-12">
                <div className="text-5xl mb-4">⚠️</div>
                <h2 className="text-base font-semibold text-gray-800 mb-2">
                  Manual Review Required
                </h2>
                <p className="text-sm text-gray-500 max-w-xs">{errorMessage}</p>
              </div>
            )}

            {state ===  "success"&& report && <SafetyResult report={report} />}
          </section>

        </div>
      </main>

      <footer className="border-t border-gray-200 bg-white mt-12">
        <div className="max-w-4xl mx-auto px-4 py-4 text-center text-xs text-gray-400">
          ClinixSafe · Prototype · Build in AI for India · Not for clinical use
        </div>
      </footer>
    </div>
  );
}