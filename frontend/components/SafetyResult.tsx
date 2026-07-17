import type { SafetyReport, CommunicationDraft } from "../app/types";
import { RiskBadge } from "./RiskBadge";
import { EvidenceCard } from "./EvidenceCard";

interface Props {
  report: SafetyReport;
}

function draftLabel(type: CommunicationDraft["type"]) {
  switch (type) {
    case "CLINICIAN":
      return "Clinician";
    case "PATIENT":
      return "Patient";
    case "FOLLOW_UP":
      return "Follow-up";
    default:
      return type;
  }
}

export function SafetyResult({ report }: Props) {
  const hasEvidence = (report.evidenceTrace?.length ?? 0) > 0;
  const hasAlternatives = (report.alternativeMedications?.length ?? 0) > 0;
  const hasWarnings = (report.warnings?.length ?? 0) > 0;
  const hasDrafts = (report.communicationDrafts?.length ?? 0) > 0;

  return (
    <div className="space-y-5">
      <RiskBadge riskLevel={report.riskLevel} size="lg "/>

      <p className="text-sm text-gray-800 leading-relaxed">{report.summary}</p>

      {report.recommendations.length > 0 && (
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Recommendations
          </h2>
          <ul className="space-y-2">
            {report.recommendations.map((rec, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-gray-800">
                <span className="text-green-500 mt-0.5 shrink-0 font-bold">✓</span>
                {rec}
              </li>
            ))}
          </ul>
        </div>
      )}

      {hasAlternatives && (
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Consider Instead
          </h2>
          <div className="flex flex-wrap gap-2">
            {report.alternativeMedications!.map((alt, i) => (
              <span
                key={i}
                className="px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-sm border border-blue-200"
              >
                {alt}
              </span>
            ))}
          </div>
        </div>
      )}

      {hasWarnings && (
        <div className="rounded-lg border border-amber-200 bg-amber-50 p-4">
          <h2 className="text-xs font-semibold text-amber-800 uppercase tracking-wide mb-2">
            ⚠ Warnings
          </h2>
          <ul className="space-y-1">
            {report.warnings!.map((w, i) => (
              <li key={i} className="text-sm text-amber-700">
                {w}
              </li>
            ))}
          </ul>
        </div>
      )}

      {hasDrafts && (
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Communication Drafts
          </h2>

          <div className="space-y-3">
            {report.communicationDrafts!.map((draft, i) => (
              <div
                key={`${draft.type}-${i}`}
                className="rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-3 mb-2">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-gray-500">
                      {draftLabel(draft.type)}
                    </p>
                    <h3 className="text-sm font-semibold text-gray-900">
                      {draft.title}
                    </h3>
                  </div>

                  {draft.reviewRequired && (
                    <span className="shrink-0 rounded-full border border-amber-200 bg-amber-50 px-2.5 py-0.5 text-xs font-medium text-amber-800">
                      Review Required
                    </span>
                  )}
                </div>

                <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-line">
                  {draft.content}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {hasEvidence && (
        <div>
          <h2 className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
            Evidence Trace
          </h2>
          <div className="space-y-3">
            {report.evidenceTrace!.map((trace) => (
              <EvidenceCard key={trace.evidenceId} evidence={trace} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}