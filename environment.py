from __future__ import annotations
import copy
import uuid
from typing import Any, Dict, List, Optional

from contracts import CONTRACTS, TASKS
from grader import grade_episode, partial_reward
from models import (
    Action,
    ActionType,
    EnvironmentState,
    Issue,
    IssueCategory,
    IssueSeverity,
    Observation,
    Reward,
    StepResult,
)

VALID_ACTIONS_ALWAYS = [ActionType.SKIP]


class LegalContractAuditorEnv:

    def __init__(self) -> None:
        self._state: Optional[EnvironmentState] = None

    def reset(self, task_id: str = "task_easy") -> Observation:
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id '{task_id}'. Valid: {list(TASKS.keys())}")

        task = TASKS[task_id]
        contract = CONTRACTS[task["contract_id"]]

        self._state = EnvironmentState(
            contract_id=task["contract_id"],
            contract_text=contract["text"],
            task_id=task_id,
            task_description=task["description"],
            ground_truth_issues=copy.deepcopy(contract["ground_truth_issues"]),
            identified_issues=[],
            applied_fixes=[],
            current_step=0,
            max_steps=task["max_steps"],
            done=False,
            episode_id=str(uuid.uuid4()),
            cumulative_reward=0.0,
            audit_submitted=False,
            contract_read=False,
        )

        return self._build_observation(
            last_result="Environment reset. Read the contract first using action_type='read_contract'.",
            last_error=None,
        )

    def step(self, action: Action) -> StepResult:
        if self._state is None:
            raise RuntimeError("Call reset() before step().")
        if self._state.done:
            raise RuntimeError("Episode is done. Call reset() to start a new episode.")

        self._state.current_step += 1
        last_error: Optional[str] = None
        last_result: str = ""

        if action.action_type == ActionType.READ_CONTRACT:
            self._state.contract_read = True
            n = len(self._state.ground_truth_issues)
            last_result = (
                f"Contract loaded ({len(self._state.contract_text)} chars). "
                f"Contract: '{CONTRACTS[self._state.contract_id]['title']}'. "
                f"Your task: find all legal issues. Hint: there are approximately {n} issues."
            )

        elif action.action_type == ActionType.IDENTIFY_ISSUE:
            if not self._state.contract_read:
                last_error = "You must read_contract before identifying issues."
            elif not action.issue_description:
                last_error = "issue_description is required for identify_issue."
            elif not action.issue_category:
                last_error = "issue_category is required for identify_issue."
            elif not action.issue_severity:
                last_error = "issue_severity is required for identify_issue."
            else:
                new_issue = Issue(
                    issue_id=action.issue_id or str(uuid.uuid4())[:8],
                    category=action.issue_category,
                    severity=action.issue_severity,
                    description=action.issue_description,
                    section_reference=action.section_reference,
                )
                self._state.identified_issues.append(new_issue)
                pr = partial_reward(
                    self._state.identified_issues,
                    self._state.ground_truth_issues,
                    self._state.current_step,
                    self._state.max_steps,
                )
                last_result = (
                    f"Issue recorded: [{action.issue_severity.upper()}] {action.issue_category} "
                    f"in {action.section_reference or 'unspecified section'}. "
                    f"Detection progress: {pr*100:.0f}%"
                )

        elif action.action_type == ActionType.PROPOSE_FIX:
            if not action.issue_id:
                last_error = "issue_id required for propose_fix. Use an issue_id from your identified issues."
            elif not action.fix_text:
                last_error = "fix_text is required for propose_fix."
            else:
                last_result = (
                    f"Fix proposed for issue {action.issue_id}. "
                    "Use apply_fix to apply it."
                )

        elif action.action_type == ActionType.APPLY_FIX:
            if not action.issue_id:
                last_error = "issue_id required for apply_fix."
            elif not action.fix_text:
                last_error = "fix_text required for apply_fix."
            else:
                matched = False
                for issue in self._state.identified_issues:
                    if issue.issue_id == action.issue_id:
                        issue.fix_applied = True
                        issue.fix_text = action.fix_text
                        issue.fix_rationale = action.fix_rationale or ""
                        self._state.applied_fixes.append(
                            f"[{action.issue_id}] {action.fix_text[:120]}"
                        )
                        matched = True
                        last_result = f"Fix applied to issue {action.issue_id}."
                        break
                if not matched:
                    last_error = (
                        f"No identified issue with id '{action.issue_id}'. "
                        "Identify the issue first with identify_issue."
                    )

        elif action.action_type == ActionType.REQUEST_CLAUSE:
            clause = action.clause_name or "unspecified"
            last_result = (
                f"Clause '{clause}' requested for reference. "
                "Use this information to identify or fix related issues."
            )

        elif action.action_type == ActionType.SUBMIT_AUDIT:
            if not action.audit_summary:
                last_error = "audit_summary is required for submit_audit."
            else:
                self._state.audit_submitted = True
                self._state.done = True
                n_found = len(self._state.identified_issues)
                n_fixed = sum(1 for i in self._state.identified_issues if i.fix_applied)
                last_result = (
                    f"Audit submitted. Found {n_found} issues, applied {n_fixed} fixes. "
                    f"Summary: {action.audit_summary[:200]}"
                )

        elif action.action_type == ActionType.SKIP:
            last_result = "Action skipped."

        if self._state.current_step >= self._state.max_steps and not self._state.done:
            self._state.done = True
            last_result += " [MAX STEPS REACHED — episode ending]"

        reward = grade_episode(
            identified_issues=self._state.identified_issues,
            ground_truth_issues=self._state.ground_truth_issues,
            applied_fixes=self._state.applied_fixes,
            current_step=self._state.current_step,
            max_steps=self._state.max_steps,
            audit_submitted=self._state.audit_submitted,
        )
        self._state.cumulative_reward = reward.total

        obs = self._build_observation(last_result, last_error)

        info: Dict[str, Any] = {
            "episode_id": self._state.episode_id,
            "step": self._state.current_step,
            "reward_breakdown": reward.model_dump(),
            "issues_found": len(self._state.identified_issues),
            "issues_fixed": sum(1 for i in self._state.identified_issues if i.fix_applied),
            "ground_truth_count": len(self._state.ground_truth_issues),
        }

        return StepResult(
            observation=obs,
            reward=reward,
            done=self._state.done,
            info=info,
        )

    def state(self) -> Dict[str, Any]:
        if self._state is None:
            return {"status": "not_initialized", "message": "Call reset() first."}
        return self._state.model_dump()

    def _build_observation(
        self,
        last_result: str,
        last_error: Optional[str],
    ) -> Observation:
        s = self._state
        assert s is not None

        progress = len(s.identified_issues) / max(1, len(s.ground_truth_issues))
        progress = min(1.0, round(progress, 3))

        available: List[ActionType] = [ActionType.SKIP]
        if not s.contract_read:
            available.append(ActionType.READ_CONTRACT)
        else:
            available += [
                ActionType.READ_CONTRACT,
                ActionType.IDENTIFY_ISSUE,
                ActionType.PROPOSE_FIX,
                ActionType.APPLY_FIX,
                ActionType.REQUEST_CLAUSE,
                ActionType.SUBMIT_AUDIT,
            ]

        hints: List[str] = []
        if not s.contract_read:
            hints.append("Start by using 'read_contract' to load the contract.")
        elif len(s.identified_issues) == 0:
            hints.append("No issues identified yet. Use 'identify_issue' with category, severity, description, and section_reference.")
        elif s.current_step > s.max_steps * 0.7 and not s.audit_submitted:
            hints.append("You are running out of steps. Consider submitting your audit soon.")

        return Observation(
            contract_text=s.contract_text,
            contract_id=s.contract_id,
            task_id=s.task_id,
            task_description=s.task_description,
            current_step=s.current_step,
            max_steps=s.max_steps,
            identified_issues=list(s.identified_issues),
            applied_fixes=list(s.applied_fixes),
            available_actions=available,
            last_action_result=last_result,
            last_action_error=last_error,
            progress_pct=progress,
            hints=hints,
        )

    def get_tasks(self) -> Dict[str, Any]:
        return {
            tid: {
                "description": t["description"],
                "difficulty": t["difficulty"],
                "max_steps": t["max_steps"],
                "num_issues": t["num_issues"],
            }
            for tid, t in TASKS.items()
        }