from __future__ import annotations
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ActionType(str, Enum):
    READ_CONTRACT   = "read_contract"
    IDENTIFY_ISSUE  = "identify_issue"
    PROPOSE_FIX     = "propose_fix"
    APPLY_FIX       = "apply_fix"
    REQUEST_CLAUSE  = "request_clause"
    SUBMIT_AUDIT    = "submit_audit"
    SKIP            = "skip"


class IssueSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH     = "high"
    MEDIUM   = "medium"
    LOW      = "low"


class IssueCategory(str, Enum):
    MISSING_CLAUSE      = "missing_clause"
    RISKY_LANGUAGE      = "risky_language"
    CONTRADICTION       = "contradiction"
    UNDEFINED_REFERENCE = "undefined_reference"
    AMBIGUOUS_TERM      = "ambiguous_term"
    COMPLIANCE_RISK     = "compliance_risk"


class Action(BaseModel):
    action_type:       ActionType
    issue_id:          Optional[str]           = None
    issue_category:    Optional[IssueCategory] = None
    issue_severity:    Optional[IssueSeverity] = None
    issue_description: Optional[str]           = None
    clause_name:       Optional[str]           = None
    fix_text:          Optional[str]           = None
    fix_rationale:     Optional[str]           = None
    section_reference: Optional[str]           = None
    audit_summary:     Optional[str]           = None


class Issue(BaseModel):
    issue_id:          str
    category:          IssueCategory
    severity:          IssueSeverity
    description:       str
    section_reference: Optional[str] = None
    fix_applied:       bool          = False
    fix_text:          Optional[str] = None
    fix_rationale:     Optional[str] = None
    score_contribution: float        = 0.0


class Observation(BaseModel):
    contract_text:      str
    contract_id:        str
    task_id:            str
    task_description:   str
    current_step:       int
    max_steps:          int
    identified_issues:  List[Issue]       = []
    applied_fixes:      List[str]         = []
    available_actions:  List[ActionType]  = []
    last_action_result: str               = ""
    last_action_error:  Optional[str]     = None
    progress_pct:       float             = 0.0
    hints:              List[str]         = []


class Reward(BaseModel):
    total:            float = 0.0
    issue_detection:  float = 0.0
    fix_quality:      float = 0.0
    completeness:     float = 0.0
    accuracy_penalty: float = 0.0
    step_efficiency:  float = 0.0


class StepResult(BaseModel):
    observation: Observation
    reward:      Reward
    done:        bool
    info:        Dict[str, Any] = {}


class EnvironmentState(BaseModel):
    contract_id:          str
    contract_text:        str
    task_id:              str
    task_description:     str
    ground_truth_issues:  List[Dict[str, Any]] = []
    identified_issues:    List[Issue]           = []
    applied_fixes:        List[str]             = []
    current_step:         int                   = 0
    max_steps:            int                   = 30
    done:                 bool                  = False
    episode_id:           str = Field(default_factory=lambda: str(uuid.uuid4()))
    cumulative_reward:    float                 = 0.0
    audit_submitted:      bool                  = False
    contract_read:        bool                  = False