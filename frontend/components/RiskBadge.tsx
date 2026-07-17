import type { RiskLevel } from "../app/types";

const RISK_CONFIG: Record<
  RiskLevel,
  {
    label: string;
    icon: string;
    bg: string;
    text: string;
    border: string;
  }
> = {
  SAFE: {
    label: "Safe",
    icon: "🟢",
    bg: "bg-green-50",
    text: "text-green-800",
    border: "border-green-200",
  },
  MONITOR: {
    label: "Monitor",
    icon: "🟡",
    bg: "bg-yellow-50",
    text: "text-yellow-800",
    border: "border-yellow-200",
  },
  REVIEW: {
    label: "Review Required",
    icon: "🟠",
    bg: "bg-orange-50",
    text: "text-orange-800",
    border: "border-orange-200",
  },
  HIGH: {
    label: "High Risk",
    icon: "🔴",
    bg: "bg-red-50",
    text: "text-red-800",
    border: "border-red-200",
  },
  CONTRAINDICATED: {
    label: "Contraindicated",
    icon: "⛔",
    bg: "bg-red-50",
    text: "text-red-900",
    border: "border-red-300",
  },
  LIMITED: {
    label: "Limited Info",
    icon: "⚪",
    bg: "bg-gray-50",
    text: "text-gray-700",
    border: "border-gray-200",
  },
};

interface Props {
  riskLevel: RiskLevel;
  size?: "sm" | "lg";
}

export function RiskBadge({
  riskLevel,
  size = "sm",
}: Props) {
  const c = RISK_CONFIG[riskLevel];

  const textSize =
    size === "lg"
      ? "text-2xl font-bold"
      : "text-sm font-semibold";

  return (
    <span
      className={`inline-flex items-center gap-2 px-3 py-1.5 rounded-full border ${textSize} ${c.bg} ${c.text} ${c.border}`}
      role="status"
      aria-label={`Risk level: ${c.label}`}
    >
      <span aria-hidden="true">{c.icon}</span>
      {c.label}
    </span>
  );
}