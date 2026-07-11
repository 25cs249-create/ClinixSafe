"use client";

import { useState } from "react";

type Props = {
  onAnalyze: (current: string, next: string) => void;
};

export default function PatientForm({ onAnalyze }: Props) {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");

  return (
    <div className="bg-white p-6 rounded-xl shadow mt-8">
      <h2 className="text-2xl font-bold mb-4">
        Medication Verification
      </h2>

      <input
        className="border p-2 rounded w-full mb-4"
        placeholder="Current Medication (Example: Warfarin)"
        value={current}
        onChange={(e) => setCurrent(e.target.value)}
      />

      <input
        className="border p-2 rounded w-full mb-4"
        placeholder="New Medication (Example: Ibuprofen)"
        value={next}
        onChange={(e) => setNext(e.target.value)}
      />

      <button
        onClick={() => onAnalyze(current, next)}
        className="bg-blue-600 text-white px-5 py-2 rounded"
      >
        Verify Medication
      </button>
    </div>
  );
}