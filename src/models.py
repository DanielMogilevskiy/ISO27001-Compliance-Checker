from dataclasses import dataclass
from enum import Enum

class ComplianceStatus(Enum):
    IMPLEMENTED = "Implemented"
    PARTIAL = "Partially Implemented"
    NOT_IMPLEMENTED = "Not Implemented"
    NOT_APPLICABLE = "Not Applicable"

@dataclass
class Control:
    id: str
    category: str
    name: str
    description: str
    status: ComplianceStatus = None