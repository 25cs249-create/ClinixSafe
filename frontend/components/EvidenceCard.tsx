import type { EvidenceTrace } from "../app/types";

const PRIORITY_COLOR: Record<string, string> = {
  HIGH:   "bg-red-100 text-red-700 border-red-200",
  MEDIUM: "bg-yellow-100 text-yellow-700 border-yellow-200",
  LOW:    "bg-gray-100 text-gray-600 border-gray-200",
};

interface Props {
  evidence: EvidenceTrace;
}

export function EvidenceCard({ evidence }: Props) {
  return (
    <div className="border border-gray-200 rounded-lg p-4 bg-white">
      <div className="flex items-start justify-between gap-3 mb-2">
        <h3 className="font-semibold text-gray-900 text-sm">
          {evidence.title}
        </h3>
        <div className="flex items-center gap-2 shrink-0">
          <span
            className={`text-xs px-2 py-0.5 rounded-full border font-medium ${
              PRIORITY_COLOR[evidence.priority] ?? PRIORITY_COLOR.LOW
            }`}
          >
            {evidence.priority}
          </span>
          <code className="text-xs text-gray-400 bg-gray-50 px-2 py-0.5 rounded">
            {evidence.evidenceId}
          </code>
        </div>
      </div>
      <p className="text-sm text-gray-700 mb-3 leading-relaxed">
        {evidence.description}
      </p>
      <div className="text-xs text-gray-500">
        {evidence.source}
      </div>
    </div>
  );
}