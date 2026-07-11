import type { SafetyReport } from "../app/types";
import { RiskBadge } from "./RiskBadge";
import { EvidenceCard } from "./EvidenceCard";

interface Props {
  report: SafetyReport;
}

export function SafetyResult({ report }: Props) {
  const hasEvidence     = (report.evidenceTrace?.length ?? 0) > 0;
  const hasAlternatives = (report.alternativeMedications?.length ?? 0) > 0;
  const hasWarnings     = (report.warnings?.length ?? 0) > 0;

  return (
    <div className="space-y-5">
      <RiskBadge riskLevel={report.riskLevel} size="lg" />

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
              <li key={i} className="text-sm text-amber-700">{w}</li>
            ))}
          </ul>
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