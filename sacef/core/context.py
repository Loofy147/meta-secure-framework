from dataclasses import dataclass, field
from typing import List, Type


@dataclass
class TargetFunctionContext:
    """
    Provides metadata about a target function to guide the analysis.
    """
    expected_exceptions: List[Type[Exception]] = field(default_factory=list)
    # Future metadata, such as input constraints, can be added here.
