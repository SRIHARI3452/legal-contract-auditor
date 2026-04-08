# LegalContractAuditor

## Environment Description
**LegalContractAuditor** is a Reinforcement Learning environment designed for Automated Contract Compliance Review. 
An AI agent acting as a paralegal or lawyer audits real commercial contracts spanning multiple legal domains. The agent must systematically traverse a contract, identify injected legal bugs (missing clauses, contradictions, undefined references, compliance risks), propose specific fixes, and conclude with a summarized audit report.

## Real-World Motivation
Reviewing highly dense legal text is tedious, error-prone, and incredibly expensive. The LegalContractAuditor simulates an actual human workflow (reading, spotting risks, drafting fixes) against real-world data derived from the standard CUAD (Contract Understanding Atticus Dataset). This ensures models are graded not on toy puzzles, but on genuine capability to perform commercially valuable paralegal auditing safely.

---

## Action Space
The agent interacts with the environment using a typed JSON payload mapped to a Pydantic `Action` schema. 
*   `read_contract`: Retrieves the full contract text.
*   `identify_issue`: Logs a specific defect mapping to rigorous categories (`missing_clause`, `contradiction`, etc) and severities.
*   `propose_fix` & `apply_fix`: Re-drafts the clause with updated, binding legal terminology.
*   `request_clause`: Requests specific sections or external referencing.
*   `submit_audit`: Submits a compiled history of changes and securely terminates the episode.
*   `skip`: Null action.

## Observation Space
The Pydantic `Observation` schema provides rich, stateful context back to the agent:
*   `contract_text`: The full legal copy (loaded via read command).
*   `task_description` & `max_steps`: Meta objectives.
*   `identified_issues`: Array tracking stateful bugs the agent has logged.
*   `last_action_result`: Status of the last API call.
*   `last_action_error`: Granular parser feedback if JSON schema fails.
*   `progress_pct` & `hints`: Gamified workflow progression tracking.

---

## Tasks
The environment currently ships with 3 incrementally difficult tasks:

### 1. `task_easy` (Software License Audit)
**Max Steps:** 20
**Description:** Auditing a deliberately broken software license agreement. The agent must find standard missing confidentiality clauses, ambiguous payment terms, weak termination clauses, and overbroad liability exclusions.

### 2. `task_medium` (MSA Contradiction Detection)
**Max Steps:** 30
**Description:** Audit a Master Services Agreement riddled with direct contradictions in payment terms, IP ownership, SLA guarantees, and governing law. Also masks a GDPR/CCPA compliance risk.

### 3. `task_hard` (M&A NDA Full Audit)
**Max Steps:** 40
**Description:** Extreme-scale audit of a complex Merger & Acquisition NDA. Requires cross-referencing undefined Effective Dates, conflicting confidentiality schedules, and structurally missing residuals clause analysis.

---

## Setup Instructions
1. Clone the repository and navigate to the directory:
   ```bash
   cd RL-Depoly
   ```
2. Set up a Python Virtual Environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your `.env` variables or export them securely directly in terminal:
   ```bash
   export HF_TOKEN="your_valid_api_key_here"
   export MODEL_NAME="gemini-2.0-flash" 
   export API_BASE_URL="https://generativelanguage.googleapis.com/v1beta/openai/"
   ```

## Run Instructions
Begin the evaluation inference script. The environment logic is embedded statically so there is no need to boot up a separate generic API server for testing evaluation:
```bash
python inference.py
```
> The script evaluates all tasks simultaneously and emits strict `[START]`, `[STEP]`, and `[END]` stdout arrays securely compatible with the standard Hackathon evaluators.

## Docker Instructions
You can containerize the server infrastructure seamlessly to expose the natively compliant REST endpoints (`POST /reset`, `POST /step`, `GET /state`) required by the Hugging Face Space deployments:

```bash
docker build -t legal-contract-auditor .

docker run -p 7860:7860 legal-contract-auditor
```

---

## Baseline Results
The deterministic grading system caps scores dynamically between `0.0` and `1.0`. When tested natively using the default **gemini-2.0-flash** agent logic, the model systematically identifies the legal contradictions and securely applies valid fixes, resolving at a highly positive baseline score:

*   **task_easy:** `0.7232` 
*   **task_medium:** `0.6841` 
*   **task_hard:** `0.6526` 
*   **AVERAGE SCORE:** `0.6866`
