---
title: LegalContractAuditor
emoji: ⚖️
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
tags:
  - openenv
---

# LegalContractAuditor

An OpenEnv-compatible RL environment where an agent audits legal contracts for defects — missing clauses, contradictions, risky wording, compliance gaps — and proposes fixes. Built on top of real contract structures from the [CUAD dataset](https://huggingface.co/datasets/theatticusproject/cuad).

## Why this exists

Contract review is one of those jobs that's boring, expensive, and high-stakes all at the same time. Junior associates at law firms spend hundreds of hours reading through dense legal text looking for problems that could cost their clients millions. We wanted to build an environment that captures that workflow: read a contract, spot the issues, draft fixes, submit your findings.

The contracts here aren't random — they're based on real commercial agreements (software licenses, MSAs, M&A NDAs) with deliberately injected bugs. The grader checks whether the agent found the right issues and whether the proposed fixes actually make legal sense.

## Action space

Actions are JSON objects with an `action_type` field. The full schema is in `models.py` (`Action` model).

| Action | What it does |
|--------|-------------|
| `read_contract` | Loads the contract text into the observation |
| `identify_issue` | Flags a specific problem (requires category, severity, description) |
| `apply_fix` | Proposes replacement language for a flagged issue |
| `submit_audit` | Wraps up the episode with a summary |
| `skip` | Does nothing (burns a step) |

Issue categories: `missing_clause`, `risky_language`, `contradiction`, `undefined_reference`, `ambiguous_term`, `compliance_risk`

Severity levels: `critical`, `high`, `medium`, `low`

## Observation space

After each step the agent gets back an `Observation` (see `models.py`) containing:

- `contract_text` — the full contract (populated after `read_contract`)
- `identified_issues` — list of issues the agent has flagged so far
- `progress_pct` — how far along the agent is (0.0–1.0)
- `last_action_result` / `last_action_error` — feedback on what happened
- `hints` — nudges if the agent is stuck
- `current_step` / `max_steps` — step budget

## Tasks

Three tasks, easy to hard. Each one uses a different contract type with different kinds of injected bugs.

**task_easy — Software License Audit** (20 steps)
A broken software license. Missing confidentiality clause, vague payment terms ("reasonable time" instead of NET 30), weak termination language, blanket liability exclusion. Straightforward stuff.

**task_medium — MSA Contradiction Detection** (30 steps)
A Master Services Agreement with contradictions planted across sections — conflicting payment terms, IP ownership clauses that disagree with each other, SLA guarantees that contradict the liability disclaimers. Also has a data privacy clause that violates GDPR/CCPA.

**task_hard — M&A NDA Full Audit** (40 steps)
A Merger & Acquisition NDA with subtle issues. Undefined Effective Date that breaks all time-bound obligations, conflicting confidentiality periods between the main agreement and an addendum, inadequate protection standards for financial projections, missing residuals analysis. This one is hard even for humans.

## Setup

```bash
git clone https://github.com/SRIHARI3452/legal-contract-auditor.git
cd legal-contract-auditor

python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
```

Set these environment variables before running inference:

```bash
export API_BASE_URL="https://your-llm-endpoint.com/v1"
export MODEL_NAME="your-model-name"
export API_KEY="your-api-key"
```

## Running the inference script

```bash
python inference.py
```

This runs the agent against all three tasks sequentially and prints structured logs (`[START]`, `[STEP]`, `[END]`) to stdout.

## Running the environment server (Docker)

The environment exposes REST endpoints (`POST /reset`, `POST /step`, `GET /state`) via FastAPI.

```bash
docker build -t legal-contract-auditor .
docker run -p 7860:7860 legal-contract-auditor
```

Then hit `http://localhost:7860/health` to check it's running.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/reset` | Start a new episode. Body: `{"task_id": "task_easy"}` |
| POST | `/step` | Take an action. Body: `{"action": {...}}` |
| GET | `/state` | Get current environment state |
| GET | `/tasks` | List available tasks |
| GET | `/health` | Health check |

## Baseline scores

Tested with the default inference script. Scores are between 0.0 and 1.0.

| Task | Score |
|------|-------|
| task_easy | 0.7232 |
| task_medium | 0.6841 |
| task_hard | 0.6526 |
| **Average** | **0.6866** |

## Project structure

```
├── inference.py       # baseline agent script (uses OpenAI client)
├── environment.py     # core RL environment logic
├── models.py          # Pydantic models (Action, Observation, Reward, etc.)
├── contracts.py       # contract templates with injected bugs
├── grader.py          # deterministic grading logic
├── openenv.yaml       # OpenEnv metadata
├── server/
│   └── app.py         # FastAPI server wrapping the environment
├── Dockerfile
├── requirements.txt
└── README.md
```
