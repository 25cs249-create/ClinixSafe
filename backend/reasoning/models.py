from dataclasses import dataclass


@dataclass
class RoutingDecision:

    requires_ai: bool

    reason: str