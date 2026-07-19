import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";
import type { SafetyReport } from "../types";

export function downloadClinicalReport(report: SafetyReport) {
  const doc = new jsPDF();

  doc.setFontSize(22);
  doc.text("ClinixSafe", 14, 18);

  doc.setFontSize(11);
  doc.text("AI Medication Safety Verification Report", 14, 26);

  doc.setDrawColor(180);
  doc.line(14, 30, 196, 30);

  autoTable(doc, {
    startY: 38,
    head: [["Field", "Value"]],
    body: [
      ["Risk Level", report.riskLevel],
      ["Evidence Strength", report.evidenceStrength ?? "N/A"],
      ["Report ID", report.reportId ?? "N/A"],
      ["Knowledge Base", report.knowledgeBaseVersion ?? "v1.0"],
      ["Generated", report.generatedAt ?? new Date().toLocaleString()],
    ],
  });

  let y = (doc as any).lastAutoTable.finalY + 12;

  doc.setFontSize(15);
  doc.text("Clinical Summary", 14, y);

  y += 8;

  doc.setFontSize(11);
  doc.text(report.summary, 14, y, {
    maxWidth: 180,
  });

  y += 24;

  doc.setFontSize(15);
  doc.text("Recommended Clinical Actions", 14, y);

  y += 8;

  report.recommendations.forEach((rec) => {
    doc.text(`• ${rec}`, 18, y);
    y += 7;
  });

  if (report.alternativeMedications?.length) {
    y += 8;

    doc.setFontSize(15);
    doc.text("Safer Alternatives", 14, y);

    y += 8;

    report.alternativeMedications.forEach((alt) => {
      doc.text(`• ${alt}`, 18, y);
      y += 7;
    });
  }

  if (report.warnings?.length) {
    y += 8;

    doc.setFontSize(15);
    doc.text("Critical Safety Alerts", 14, y);

    y += 8;

    report.warnings.forEach((warning) => {
      doc.text(`• ${warning}`, 18, y);
      y += 7;
    });
  }

  if (report.evidenceTrace?.length) {
    y += 8;

    doc.setFontSize(15);
    doc.text("Clinical Evidence", 14, y);

    y += 8;

        report.evidenceTrace.forEach((e) => {
        doc.setFontSize(13);
        doc.text(e.title, 18, y);

        y += 6;

        doc.setFontSize(10);
        doc.text(`Source: ${e.source}`, 22, y);

        y += 5;

        doc.text(`Type: ${e.sourceType}`, 22, y);

        y += 5;

        doc.text(`Priority: ${e.priority}`, 22, y);

        y += 5;

        doc.text(e.description, 22, y, {
            maxWidth: 165,
        });

        y += 15;
        });
  }

  doc.save(
    `ClinixSafe_Report_${report.reportId ?? Date.now()}.pdf`
  );
}