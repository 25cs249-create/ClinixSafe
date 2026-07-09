from dataclasses import dataclass


@dataclass
class EvaluationMetrics:

    total: int = 0

    passed: int = 0

    failed: int = 0

    accuracy: float = 0.0