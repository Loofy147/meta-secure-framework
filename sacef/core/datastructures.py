from dataclasses import dataclass
from enum import Enum
from typing import List


class AttackVector(Enum):
    OVERFLOW = "overflow"
    TYPE_CONFUSION = "type_confusion"
    LOGIC_BYPASS = "logic_bypass"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    INJECTION = "injection"
    CODE_INJECTION = "code_injection"
    META_VULNERABILITY = "meta_vulnerability"  # Vulnerabilities in the framework itself!


class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Vulnerability:
    attack_vector: AttackVector
    severity: float
    severity_level: SeverityLevel
    exploit_code: str
    failure_trace: List[str]
    discovered_at: float
    patch_suggestions: List[str]

    def __post_init__(self):
        if self.severity >= 0.8:
            self.severity_level = SeverityLevel.CRITICAL
        elif self.severity >= 0.6:
            self.severity_level = SeverityLevel.HIGH
        elif self.severity >= 0.4:
            self.severity_level = SeverityLevel.MEDIUM
        else:
            self.severity_level = SeverityLevel.LOW
