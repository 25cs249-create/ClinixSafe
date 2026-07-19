"use client";



import { useState, useRef, type FormEvent } from "react";

import type { SafetyReport } from "./types";

import { analyzeMedication, BackendUnavailableError } from "./lib/api";

import { SafetyResult } from "../components/SafetyResult";



type AppState = "idle" | "loading" | "success" | "error";



export default function Home() {

  const [currentMedications, setCurrentMedications] = useState("");

  const [newMedication, setNewMedication] = useState("");

  const [state, setState] = useState<AppState>("idle");

  const [report, setReport] = useState<SafetyReport | null>(null);

  const [errorMessage, setErrorMessage] = useState("");



  // NEW: Report auto-scroll

  const reportRef = useRef<HTMLDivElement>(null);



  const demoCases = [

    {

      title: "🩸 High Risk",

      subtitle: "Warfarin + Ibuprofen",

      current: "warfarin",

      newMed: "ibuprofen",

      tone: "red",

    },

    {

      title: "⚠ Monitor",

      subtitle: "Lanoxin + Calaptin",

      current: "lanoxin",

      newMed: "calaptin",

      tone: "amber",

    },

    {

      title: "✅ Safe",

      subtitle: "Warfarin + Paracetamol",

      current: "warfarin",

      newMed: "paracetamol",

      tone: "green",

    },

    {

      title: "ℹ Limited",

      subtitle: "Warfarin + Zylofexamine",

      current: "warfarin",

      newMed: "zylofexamine",

      tone: "slate",

    },

  ] as const;



  async function handleSubmit(e: FormEvent<HTMLFormElement>) {

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



      // NEW: Smooth scroll to generated report

      setTimeout(() => {

        reportRef.current?.scrollIntoView({

          behavior: "smooth",

          block: "start",

        });

      }, 150);

    } catch (error) {

      if (error instanceof BackendUnavailableError) {

        setErrorMessage(

          "Unable to reach the ClinixSafe service right now. Please try again in a moment."

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



  function loadDemoCase(current: string, next: string) {

    setCurrentMedications(current);

    setNewMedication(next);

    setReport(null);

    setState("idle");

    setErrorMessage("");

  }



  const toneStyles = {

    red: "border-red-200 bg-red-50 text-red-700 hover:bg-red-100",

    amber:

      "border-amber-200 bg-amber-50 text-amber-700 hover:bg-amber-100",

    green:

      "border-emerald-200 bg-emerald-50 text-emerald-700 hover:bg-emerald-100",

    slate:

      "border-slate-200 bg-slate-50 text-slate-700 hover:bg-slate-100",

  } as const;



  return (

    <div className="min-h-screen bg-slate-50 text-slate-900">

      <header className="sticky top-0 z-20 border-b border-slate-200 bg-white/90 backdrop-blur">

        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">

          <div>

            <div className="flex items-center gap-2">

              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-slate-900 text-white shadow-sm">

                🛡️

              </div>



              <div>

                <h1 className="text-lg font-bold tracking-tight text-slate-950">

                  ClinixSafe

                </h1>



                <p className="text-xs text-slate-500">

                  AI-powered medication safety verification

                </p>

              </div>

            </div>

          </div>



          <span className="hidden rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-medium text-amber-700 sm:inline-flex">

            Prototype · Educational Demonstration Only

          </span>

        </div>

      </header>



      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">

        <section className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm">

          <div className="grid gap-0 lg:grid-cols-12">

            <div className="p-6 lg:col-span-7 lg:p-10">

              <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-600">

                <span className="text-emerald-600">●</span>

                Deterministic first · Explainable second · Human review always

              </div>



              <h2 className="mt-5 max-w-2xl text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">

                AI Medication Safety Verification for Indian Clinical Workflows

              </h2>



              <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600 sm:text-lg">

                Verify interactions, surface evidence, and generate

                clinician-ready communication drafts before a medication

                reaches the patient.

              </p>



              <div className="mt-6 flex flex-wrap gap-3">

                <button

                  type="button"

                  onClick={() => loadDemoCase("warfarin", "ibuprofen")}

                  className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800"

                >

                  Try High-Risk Demo

                </button>



                <a

                  href="#analysis"

                  className="rounded-xl border border-slate-300 bg-white px-5 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"

                >

                  Open Analyzer

                </a>

              </div>



              <div className="mt-8 grid gap-3 sm:grid-cols-3">

                {[

                  {

                    label: "Evidence-backed",

                    value: "10 Rules",

                  },

                  {

                    label: "Explainable",

                    value: "Traceable",

                  },

                  {

                    label: "Human-reviewed",

                    value: "Clinician Control",

                  },

                ].map((item) => (

                  <div

                    key={item.label}

                    className="rounded-2xl border border-slate-200 bg-slate-50 p-4"

                  >

                    <p className="text-xs font-medium uppercase tracking-wide text-slate-500">

                      {item.label}

                    </p>



                    <p className="mt-1 text-lg font-semibold text-slate-950">

                      {item.value}

                    </p>

                  </div>

                ))}

              </div>

            </div>



            <div className="border-t border-slate-200 bg-linear-to-br from-slate-950 to-slate-800 p-6 text-white lg:col-span-5 lg:border-l lg:border-t-0 lg:p-8">

              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-400">

                Core Product Capabilities

              </p>



              <div className="mt-5 grid gap-4">

                {[

                  {

                    title: "Drug Interaction Detection",

                    text: "Deterministic rule engine checks known interactions first.",

                  },

                  {

                    title: "Evidence Trace",

                    text: "Every recommendation is backed by an explainable source trail.",

                  },

                  {

                    title: "Clinical Communication",

                    text: "Generate clinician, patient and follow-up drafts.",

                  },

                  {

                    title: "India-ready Workflow",

                    text: "Designed for busy pharmacies, clinics and hospitals.",

                  },

                ].map((feature) => (

                  <div

                    key={feature.title}

                    className="rounded-2xl border border-white/10 bg-white/5 p-4 backdrop-blur"

                  >

                    <h3 className="text-sm font-semibold">

                      {feature.title}

                    </h3>



                    <p className="mt-1 text-sm leading-6 text-slate-300">

                      {feature.text}

                    </p>

                  </div>

                ))}

              </div>

            </div>

          </div>

        </section>

        <section

          id="analysis"

          className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2"

        >

          <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

            <div className="mb-5">

              <h2 className="text-lg font-semibold text-slate-950">

                Verify Medication Safety

              </h2>



              <p className="mt-1 text-sm text-slate-500">

                Select a demo case or enter your own medication combination.

              </p>

            </div>



            <div className="mb-6">

              <p className="mb-2 text-sm font-medium text-slate-700">

                Quick Demo Cases

              </p>



              <div className="grid grid-cols-1 gap-2 sm:grid-cols-2">

                {demoCases.map((demo) => (

                  <button

                    key={demo.subtitle}

                    type="button"

                    onClick={() =>

                      loadDemoCase(demo.current, demo.newMed)

                    }

                    className={`rounded-2xl border px-4 py-3 text-left transition ${

                      toneStyles[demo.tone]

                    }`}

                  >

                    <div className="text-sm font-semibold">

                      {demo.title}

                    </div>



                    <div className="mt-0.5 text-xs opacity-80">

                      {demo.subtitle}

                    </div>

                  </button>

                ))}

              </div>

            </div>



            <form onSubmit={handleSubmit} className="space-y-4">

              <div>

                <label

                  htmlFor="currentMeds"

                  className="mb-1 block text-sm font-medium text-slate-700"

                >

                  Current Medications

                </label>



                <input

                  id="currentMeds"

                  type="text"

                  value={currentMedications}

                  onChange={(e) =>

                    setCurrentMedications(e.target.value)

                  }

                  placeholder="warfarin, metformin"

                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"

                />



                <p className="mt-1 text-xs text-slate-400">

                  Separate multiple medications with commas.

                </p>

              </div>



              <div>

                <label

                  htmlFor="newMed"

                  className="mb-1 block text-sm font-medium text-slate-700"

                >

                  New Medication

                  <span className="text-red-500"> *</span>

                </label>



                <input

                  id="newMed"

                  type="text"

                  value={newMedication}

                  onChange={(e) =>

                    setNewMedication(e.target.value)

                  }

                  placeholder="ibuprofen"

                  required

                  className="w-full rounded-xl border border-slate-300 px-4 py-3 text-sm outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"

                />

              </div>



              <div className="flex gap-3 pt-1">

                <button

                  type="submit"

                  disabled={

                    state === "loading" ||

                    !newMedication.trim()

                  }

                  className="flex-1 rounded-xl bg-slate-900 px-4 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"

                >

                  {state === "loading"

                    ? "Analyzing..."

                    : "Verify Medication"}

                </button>



                {state !== "idle" && (

                  <button

                    type="button"

                    onClick={handleReset}

                    className="rounded-xl border border-slate-300 px-4 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"

                  >

                    Reset

                  </button>

                )}

              </div>

            </form>

          </div>



          <section

            aria-live="polite"

            ref={reportRef}

          >

            <div className="rounded-3xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">

              {state === "idle" && (

                <div className="flex min-h-112 flex-col items-center justify-center text-center">

                  <div className="mb-4 text-5xl">🛡️</div>



                  <h2 className="text-xl font-semibold text-slate-900">

                    Ready to verify.

                  </h2>



                  <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">

                    Enter medications or select a demo case to

                    generate a complete clinical safety report with

                    evidence and communication templates.

                  </p>

                </div>

              )}



              {state === "loading" && (

                <div className="flex min-h-112 flex-col items-center justify-center text-center">

                  <div className="mb-5 h-12 w-12 animate-spin rounded-full border-4 border-slate-200 border-t-slate-900" />



                  <p className="text-sm font-medium text-slate-700">

                    Analyzing medication safety...

                  </p>

                </div>

              )}



              {state === "error" && (

                <div className="flex min-h-112 flex-col items-center justify-center text-center">

                  <div className="mb-4 text-5xl">⚠️</div>



                  <h2 className="text-xl font-semibold text-slate-900">

                    Manual Review Required

                  </h2>



                  <p className="mt-2 max-w-sm text-sm leading-6 text-slate-500">

                    {errorMessage}

                  </p>

                </div>

              )}



              {state === "success" &&

                report && <SafetyResult report={report} />}

            </div>

          </section>

        </section>

      </main>



      <footer className="border-t border-slate-200 bg-white">

        <div className="mx-auto max-w-7xl px-4 py-5 text-center text-xs text-slate-400 sm:px-6 lg:px-8">

          ClinixSafe · Build in AI for India · Prototype · Educational Demonstration Only

        </div>

      </footer>

    </div>

  );

}