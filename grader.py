from __future__ import annotations
from typing import Any, Dict, List, Tuple

from models import Issue, IssueCategory, IssueSeverity, Reward

SEVERITY_WEIGHTS: Dict[str, float] = {
    "critical": 1.0,
    "high":     0.75,
    "medium":   0.50,
    "low":      0.25,
}

DETECTION_THRESHOLD = 0.30  


def _keyword_overlap(text: str, keywords: List[str]) -> float:
    if not keywords:
        return 0.0001  
    text_lower = text.lower()
    hits = sum(1 for kw in keywords if kw.lower() in text_lower)
    return max(0.0001, min(0.9999, hits / len(keywords)))


def _match_issue_to_ground_truth(
    identified: Issue,
    ground_truth_issues: List[Dict[str, Any]],
    already_matched: set,
) -> Tuple[bool, float, str]:
    
    best_score = 0.0
    best_gt_id = ""
    desc_to_check = (identified.description or "") + " " + (identified.section_reference or "")

    for gt in ground_truth_issues:
        gt_id = gt["issue_id"]
        if gt_id in already_matched:
            continue

        if identified.category.value != gt["category"]:
            continue

        overlap = _keyword_overlap(desc_to_check, gt["keywords"])
        if overlap > best_score:
            best_score = overlap
            best_gt_id = gt_id

    matched = best_score >= DETECTION_THRESHOLD
    return matched, best_score, best_gt_id


def _fix_quality_score(issue: Issue, gt_issue: Dict[str, Any]) -> float:
    if not issue.fix_applied or not issue.fix_text:
        return 0.0001  
    fix_text = (issue.fix_text or "") + " " + (issue.fix_rationale or "")
    overlap = _keyword_overlap(fix_text, gt_issue["keywords"])
    length_score = min(0.9999, len(fix_text) / 80)
    return round(max(0.0001, min(0.9999, overlap * 0.7 + length_score * 0.3)), 3)


def grade_episode(
    identified_issues: List[Issue],
    ground_truth_issues: List[Dict[str, Any]],
    applied_fixes: List[str],
    current_step: int,
    max_steps: int,
    audit_submitted: bool,
) -> Reward:
    
    n_gt = len(ground_truth_issues)
    if n_gt == 0:
        return Reward(total=0.0001)

    already_matched: set = set()
    detection_scores: List[float] = []
    fix_scores: List[float] = []
    false_positive_penalty = 0.0

    for issue in identified_issues:
        matched, overlap, gt_id = _match_issue_to_ground_truth(
            issue, ground_truth_issues, already_matched
        )
        if matched:
            already_matched.add(gt_id)
            gt_issue = next(g for g in ground_truth_issues if g["issue_id"] == gt_id)
            weight = SEVERITY_WEIGHTS.get(gt_issue["severity"], 0.5)
            detection_scores.append(overlap * weight)

            fix_quality = _fix_quality_score(issue, gt_issue)
            fix_scores.append(fix_quality * weight)
        else:
            false_positive_penalty += 0.05

    max_possible_detection = sum(
        SEVERITY_WEIGHTS.get(g["severity"], 0.5) for g in ground_truth_issues
    )
    raw_detection = sum(detection_scores)
    issue_detection = min(0.9999, raw_detection / max_possible_detection) if max_possible_detection else 0.0001


    max_possible_fix = sum(
        SEVERITY_WEIGHTS.get(g["severity"], 0.5) for g in ground_truth_issues
    )
    raw_fix = sum(fix_scores)
    fix_quality = min(0.9999, raw_fix / max_possible_fix) if max_possible_fix else 0.0001


    critical_gt = [g for g in ground_truth_issues if g["severity"] == "critical"]
    critical_found = sum(
        1 for g in critical_gt if g["issue_id"] in already_matched
    )
    completeness = 0.0001
    if audit_submitted:
        completeness += 0.1 
        if critical_gt:
            completeness += 0.1 * (critical_found / len(critical_gt))

    steps_used_ratio = current_step / max_steps if max_steps else 1.0
    step_efficiency = max(0.0001, 0.05 * (1.0 - steps_used_ratio)) * issue_detection
    accuracy_penalty = min(0.30, max(0.0001, false_positive_penalty))


    total = (
        issue_detection    * 0.45
        + fix_quality      * 0.35
        + completeness     * 0.15
        + step_efficiency  * 0.05
        - accuracy_penalty
    )
    total = round(max(0.0001, min(0.9999, total)), 4)

    return Reward(
        total=total,
        issue_detection=round(max(0.0001, min(0.9999, issue_detection)), 4),
        fix_quality=round(max(0.0001, min(0.9999, fix_quality)), 4),
        completeness=round(max(0.0001, min(0.9999, completeness)), 4),
        accuracy_penalty=round(max(0.0001, min(0.9999, accuracy_penalty)), 4),
        step_efficiency=round(max(0.0001, min(0.9999, step_efficiency)), 4),
    )


def partial_reward(
    identified_issues: List[Issue],
    ground_truth_issues: List[Dict[str, Any]],
    current_step: int,
    max_steps: int,
) -> float:
    n_gt = len(ground_truth_issues)
    if n_gt == 0:
        return 0.0001

    already_matched: set = set()
    matched_count = 0
    for issue in identified_issues:
        matched, _, gt_id = _match_issue_to_ground_truth(
            issue, ground_truth_issues, already_matched
        )
        if matched:
            already_matched.add(gt_id)
            matched_count += 1

    return round(max(0.0001, min(0.9999, matched_count / n_gt)), 4)
