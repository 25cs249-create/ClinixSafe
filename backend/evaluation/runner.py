import json
from pathlib import Path

from  services.rule_engine import RuleEngine
from  evaluation.metrics import EvaluationMetrics
from  evaluation.report_writer import (
    write_json,
    write_markdown,
)

DATASET = Path( "evaluation/evaluation_dataset.json")


def load_dataset():

    with open(DATASET, "r") as f:
        return json.load(f)


def run():

    engine = RuleEngine()

    dataset = load_dataset()

    metrics = EvaluationMetrics()

    results = []

    for case in dataset:

        metrics.total += 1

        report = engine.analyze(
            case["currentMedications"],
            case["newMedication"],
        )

        actual = report.riskLevel

        expected = case["expectedRisk"]

        passed = actual == expected

        if passed:
            metrics.passed += 1
        else:
            metrics.failed += 1

        results.append(
            {
                "id": case["id"],
                "description": case["description"],
                "expected": expected,
                "actual": actual,
                "passed": passed,
            }
        )

    metrics.accuracy = (
        metrics.passed / metrics.total
    ) * 100

    write_json(results)

    write_markdown(metrics)

    print()

    print("========== Evaluation ==========")

    print(f"Total    : {metrics.total}")

    print(f"Passed   : {metrics.passed}")

    print(f"Failed   : {metrics.failed}")

    print(f"Accuracy : {metrics.accuracy:.2f}%")

    print()

    print("Reports generated successfully.")


if __name__ == "__main__":
    run()