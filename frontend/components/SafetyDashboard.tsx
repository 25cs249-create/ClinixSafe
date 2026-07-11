type Props = {
  report: any;
};

export default function SafetyDashboard({ report }: Props) {
  if (!report) return null;

  return (
    <div className="bg-white rounded-xl shadow p-6 mt-8">
      <h2 className="text-2xl font-bold">
        Analysis Result
      </h2>

      <p className="mt-4">
        <strong>Risk:</strong> {report.riskLevel}
      </p>

      <p>
        <strong>Summary:</strong> {report.summary}
      </p>

      <h3 className="font-bold mt-6">
        Recommendations
      </h3>

      <ul className="list-disc ml-6">
        {report.recommendations.map((r: string) => (
          <li key={r}>{r}</li>
        ))}
      </ul>
    </div>
  );
}