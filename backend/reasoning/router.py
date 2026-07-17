from  reasoning.models import RoutingDecision


class ReasoningRouter:

    def decide(
        self,
        current_medications: list[str],
        new_medication: str,
    ) -> RoutingDecision:

        # Simple heuristic for MVP

        if len(current_medications) >= 3:

            return RoutingDecision(
                requires_ai=True,
                reason="Polypharmacy",
            )

        if new_medication.lower() == "unknown":

            return RoutingDecision(
                requires_ai=True,
                reason="Unknown medication",
            )

        return RoutingDecision(
            requires_ai=False,
            reason="Deterministic rules sufficient",
        )