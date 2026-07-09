import json
from pathlib import Path


OUTPUT = Path("backend/evaluation/output")


OUTPUT.mkdir(parents=True, exist_ok=True)


def write_json(results):

    with open(
        OUTPUT / "evaluation_results.json",
        "w",
    ) as f:

        json.dump(results, f, indent=4)


def write_markdown(metrics):

    with open(
        OUTPUT / "evaluation_report.md",
        "w",
    ) as f:

        f.write("# ClinixSafe Evaluation Report\n\n")

        f.write(f"Total Cases: {metrics.total}\n\n")

        f.write(f"Passed: {metrics.passed}\n\n")

        f.write(f"Failed: {metrics.failed}\n\n")

        f.write(f"Accuracy: {metrics.accuracy:.2f}%\n")