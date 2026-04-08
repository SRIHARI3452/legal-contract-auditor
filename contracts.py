CONTRACTS: dict = {
    "contract_easy": {
        "title": "Software License Agreement (Broken)",
        "difficulty": "easy",
        "text": """SOFTWARE LICENSE AGREEMENT

This Software License Agreement ("Agreement") is entered into as of January 1, 2024.

PARTIES
Licensor: TechCorp Inc., a Delaware corporation ("Licensor").
Licensee: ClientCo LLC ("Licensee").

1. LICENSE GRANT
Licensor hereby grants Licensee a non-exclusive, non-transferable license to use the Software
solely for Licensee's internal business purposes.

2. PAYMENT TERMS
Licensee shall pay Licensor the license fee within a reasonable time of receiving an invoice.
Invoices shall be issued monthly.

3. INTELLECTUAL PROPERTY
All intellectual property rights in the Software shall remain with the Licensor forever and ever
without limitation of any kind whatsoever.

4. TERMINATION
Either party may terminate this Agreement at any time for any reason or no reason.

5. LIMITATION OF LIABILITY
IN NO EVENT SHALL LICENSOR BE LIABLE FOR ANY DAMAGES WHATSOEVER ARISING OUT OF
THIS AGREEMENT, INCLUDING BUT NOT LIMITED TO DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES.

6. GOVERNING LAW
This Agreement shall be governed by and construed in accordance with the laws of California.

[END OF AGREEMENT — NO SIGNATURES]
""",
        "ground_truth_issues": [
            {
                "issue_id": "easy_001",
                "category": "ambiguous_term",
                "severity": "high",
                "description": "Payment terms state 'reasonable time' which is legally ambiguous. A specific NET term (e.g., NET 30 days) is required to be enforceable.",
                "section_reference": "Section 2",
                "keywords": ["reasonable time", "net 30", "payment", "days", "specific"],
            },
            {
                "issue_id": "easy_002",
                "category": "missing_clause",
                "severity": "critical",
                "description": "No confidentiality or NDA clause. A software license must protect trade secrets and proprietary source code.",
                "section_reference": "Missing",
                "keywords": ["confidentiality", "nda", "confidential", "proprietary", "trade secret"],
            },
            {
                "issue_id": "easy_003",
                "category": "risky_language",
                "severity": "medium",
                "description": "Termination clause has no notice period or cause requirement — any party can terminate instantly without reason, causing operational disruption.",
                "section_reference": "Section 4",
                "keywords": ["notice", "termination", "cause", "days notice", "written"],
            },
            {
                "issue_id": "easy_004",
                "category": "risky_language",
                "severity": "high",
                "description": "Limitation of liability excludes ALL damages with zero carve-outs. Courts routinely void such absolute blanket exclusions, especially for gross negligence or wilful misconduct.",
                "section_reference": "Section 5",
                "keywords": ["carve-out", "gross negligence", "wilful", "limitation", "void"],
            },
            {
                "issue_id": "easy_005",
                "category": "missing_clause",
                "severity": "medium",
                "description": "No dispute resolution clause. The contract lacks any arbitration, mediation, or venue provision for resolving disagreements.",
                "section_reference": "Missing",
                "keywords": ["dispute", "arbitration", "mediation", "resolution", "venue"],
            },
        ],
    },

    "contract_medium": {
        "title": "Master Services Agreement with Contradictions",
        "difficulty": "medium",
        "text": """MASTER SERVICES AGREEMENT

This Master Services Agreement ("MSA") is made between Vendora Solutions ("Vendor")
and EnterpriseCo ("Client") effective March 15, 2024.

1. SERVICES
Vendor shall provide the services described in Schedule A, which is attached hereto
and incorporated by reference. [Note: Schedule A is not attached to this Agreement.]

2. PAYMENT TERMS
2.1 Client shall pay Vendor within NET 30 days of invoice receipt.
2.2 Client shall pay Vendor within NET 60 days of invoice receipt.
2.3 Late payments shall accrue interest at 18% per annum.
2.4 Late payments shall accrue interest at 12% per annum.

3. INTELLECTUAL PROPERTY
3.1 All work product created by Vendor under this Agreement shall be owned by Vendor.
3.2 All work product created by Vendor under this Agreement shall be owned by Client.

4. INDEMNIFICATION
Client shall indemnify Vendor against all third-party claims arising from Client's use
of the deliverables. Vendor shall indemnify Client against all third-party IP infringement
claims only.

5. TERM
This Agreement shall commence on March 15, 2024 and continue for one (1) year,
renewing automatically for additional one-year terms unless terminated with 30-day notice.

6. DATA PRIVACY
Vendor may use Client data for any purpose including sharing with third parties for
commercial gain without restriction or limitation.

7. SERVICE LEVEL AGREEMENT
Vendor guarantees 99.99% uptime for all services.
Vendor is not responsible for any downtime or service interruptions of any kind.

8. CONFIDENTIALITY
Each party agrees to keep confidential information of the other party strictly confidential
for a period of 2 years following termination of this Agreement.

9. GOVERNING LAW
This Agreement is governed by the laws of New York.
All disputes shall be resolved exclusively in the courts of California.

[SIGNATURES PAGE INTENTIONALLY LEFT BLANK]
""",
        "ground_truth_issues": [
            {
                "issue_id": "med_001",
                "category": "undefined_reference",
                "severity": "critical",
                "description": "Section 1 references Schedule A for service scope but explicitly notes it is not attached. The entire scope of services is undefined.",
                "section_reference": "Section 1",
                "keywords": ["schedule a", "not attached", "scope", "services", "undefined"],
            },
            {
                "issue_id": "med_002",
                "category": "contradiction",
                "severity": "critical",
                "description": "Sections 2.1 and 2.2 directly contradict each other — payment is simultaneously NET 30 and NET 60.",
                "section_reference": "Section 2.1 / 2.2",
                "keywords": ["net 30", "net 60", "contradiction", "payment"],
            },
            {
                "issue_id": "med_003",
                "category": "contradiction",
                "severity": "high",
                "description": "Sections 2.3 and 2.4 contradict each other — late interest rate is simultaneously 18% and 12% per annum.",
                "section_reference": "Section 2.3 / 2.4",
                "keywords": ["18%", "12%", "interest", "contradiction"],
            },
            {
                "issue_id": "med_004",
                "category": "contradiction",
                "severity": "critical",
                "description": "Sections 3.1 and 3.2 directly contradict each other — IP ownership is simultaneously assigned to Vendor and to Client.",
                "section_reference": "Section 3.1 / 3.2",
                "keywords": ["ip ownership", "vendor", "client", "contradiction", "work product"],
            },
            {
                "issue_id": "med_005",
                "category": "compliance_risk",
                "severity": "critical",
                "description": "Section 6 permits Vendor to share Client data with third parties for commercial gain — this violates GDPR Article 6, CCPA, and standard DPA requirements.",
                "section_reference": "Section 6",
                "keywords": ["gdpr", "ccpa", "data", "third parties", "commercial", "privacy", "dpa"],
            },
            {
                "issue_id": "med_006",
                "category": "contradiction",
                "severity": "high",
                "description": "Section 7 guarantees 99.99% uptime but immediately disclaims all responsibility for downtime — a direct logical and legal contradiction.",
                "section_reference": "Section 7",
                "keywords": ["uptime", "downtime", "sla", "guarantee", "contradiction"],
            },
            {
                "issue_id": "med_007",
                "category": "contradiction",
                "severity": "high",
                "description": "Governing law is New York (Section 9, line 1) but dispute venue is California (Section 9, line 2) — these conflict and create forum uncertainty.",
                "section_reference": "Section 9",
                "keywords": ["new york", "california", "governing law", "venue", "contradiction"],
            },
            {
                "issue_id": "med_008",
                "category": "missing_clause",
                "severity": "medium",
                "description": "Signatures page is blank — the contract is not executed and therefore not legally binding.",
                "section_reference": "Signatures",
                "keywords": ["signature", "executed", "binding", "signed"],
            },
        ],
    },

    "contract_hard": {
        "title": "M&A NDA — Full Due Diligence Audit",
        "difficulty": "hard",
        "text": """MUTUAL NON-DISCLOSURE AGREEMENT
FOR MERGER & ACQUISITION DUE DILIGENCE

This Mutual Non-Disclosure Agreement ("Agreement") is entered into as of the Effective Date
between the parties identified below in connection with a potential acquisition transaction
(the "Transaction").

PARTIES
Disclosing Party: Acquiror Holdings Inc. ("Acquiror")
Receiving Party: TargetCo International Ltd. ("Target")

1. DEFINITION OF CONFIDENTIAL INFORMATION
"Confidential Information" means any information disclosed by either party that is marked
"confidential" at the time of disclosure, or if disclosed orally, is identified as confidential
within a reasonable period after disclosure.

2. OBLIGATIONS OF RECEIVING PARTY
Each Receiving Party shall:
(a) hold Confidential Information in strict confidence;
(b) not disclose Confidential Information to third parties without prior written consent;
(c) use Confidential Information solely for evaluating the Transaction;
(d) protect Confidential Information using the same degree of care it uses for its own
    confidential information, but not less than reasonable care.

3. EXCLUSIONS FROM CONFIDENTIAL INFORMATION
Confidential Information shall not include information that:
(a) is or becomes publicly available through no fault of the Receiving Party;
(b) was known to the Receiving Party prior to disclosure;
(c) is independently developed by the Receiving Party without use of Confidential Information;
(d) is received from a third party without restriction.

4. PERMITTED DISCLOSURES
Each party may disclose Confidential Information to its employees, agents, advisors,
and contractors who need to know such information for the Transaction, provided such
persons are bound by confidentiality obligations.

5. TERM AND SURVIVAL
This Agreement shall remain in effect for two (2) years from the Effective Date.
All obligations of confidentiality shall survive expiration or termination.

6. RETURN OR DESTRUCTION
Upon written request or termination, the Receiving Party shall promptly return or destroy
all Confidential Information and certify such destruction in writing.

7. NO LICENSE
Nothing in this Agreement shall be construed to grant any license or right in the
Confidential Information beyond the limited purpose of evaluating the Transaction.

8. INJUNCTIVE RELIEF
The parties acknowledge that breach may cause irreparable harm for which monetary damages
may be inadequate, and injunctive or other equitable relief may be appropriate without bond.

9. STANDSTILL PROVISION
For a period of 12 months from the Effective Date, Acquiror agrees not to acquire any
securities or assets of Target without Target's prior written consent.

10. NON-SOLICITATION
For a period of 1 year from the Effective Date, neither party shall directly solicit
or hire any employee of the other party who was introduced during the Transaction process.

11. GOVERNING LAW
This Agreement shall be governed by the laws of Delaware. Disputes shall be resolved by
binding arbitration under AAA rules in Delaware.

12. ENTIRE AGREEMENT
This Agreement constitutes the entire agreement of the parties with respect to
confidentiality of the Transaction and supersedes all prior agreements.

---
ADDENDUM (appended via email, unsigned):
Notwithstanding Section 5, the confidentiality period for any financial projections,
revenue data, or customer lists shared during due diligence is extended to five (5) years.

---
SCHEDULE 1 — PERMITTED ADVISORS LIST:
[Referenced in Section 4 but Schedule 1 is not attached to this Agreement.]

EXHIBIT A — TRANSACTION OVERVIEW:
[Referenced in the recitals but Exhibit A is not included.]

---
[Agreement is undated. Effective Date is not defined anywhere in this document.]
[No signature blocks present.]
""",
        "ground_truth_issues": [
            {
                "issue_id": "hard_001",
                "category": "missing_clause",
                "severity": "critical",
                "description": "The Effective Date is referenced throughout the Agreement but is never defined anywhere. All time-bound obligations (standstill, non-solicitation, term) are unenforceable without it.",
                "section_reference": "Throughout / Missing",
                "keywords": ["effective date", "undefined", "not defined", "date", "missing"],
            },
            {
                "issue_id": "hard_002",
                "category": "ambiguous_term",
                "severity": "high",
                "description": "Section 1: oral disclosures must be designated 'within a reasonable period' — this is legally ambiguous. A specific window (e.g., 5 business days) must be specified.",
                "section_reference": "Section 1",
                "keywords": ["reasonable period", "oral", "5 business days", "timeframe", "oral disclosure"],
            },
            {
                "issue_id": "hard_003",
                "category": "risky_language",
                "severity": "critical",
                "description": "Section 2(d) sets protection standard at only 'reasonable care' — for M&A due diligence involving financial projections and trade secrets, this is dangerously low. Should require the same care as the party's most sensitive proprietary information.",
                "section_reference": "Section 2(d)",
                "keywords": ["reasonable care", "protection standard", "sensitive", "highest", "financial projections"],
            },
            {
                "issue_id": "hard_004",
                "category": "risky_language",
                "severity": "high",
                "description": "Section 3(b) excludes information 'known prior to disclosure' without requiring documented proof. This exclusion is routinely abused — the burden of proof of prior knowledge must be explicitly placed on the Receiving Party with written records.",
                "section_reference": "Section 3(b)",
                "keywords": ["prior knowledge", "documented", "burden of proof", "written records", "exclusion"],
            },
            {
                "issue_id": "hard_005",
                "category": "risky_language",
                "severity": "high",
                "description": "Section 4 permits disclosure to 'contractors' but does not require them to be parties to a formal written NDA equivalent to this Agreement. Subcontractors could receive highly sensitive M&A data without binding obligations.",
                "section_reference": "Section 4",
                "keywords": ["contractors", "written nda", "subcontractors", "binding obligations", "third party"],
            },
            {
                "issue_id": "hard_006",
                "category": "contradiction",
                "severity": "critical",
                "description": "Section 5 sets a 2-year confidentiality term, but the unsigned email Addendum extends it to 5 years for financial data. These directly conflict. The Addendum is also unsigned and its enforceability is legally questionable.",
                "section_reference": "Section 5 / Addendum",
                "keywords": ["2 years", "5 years", "addendum", "unsigned", "contradiction", "financial"],
            },
            {
                "issue_id": "hard_007",
                "category": "ambiguous_term",
                "severity": "high",
                "description": "Section 6 requires return or destruction 'promptly' — this is legally ambiguous. A specific timeframe (e.g., within 10 business days) is required, particularly in M&A contexts.",
                "section_reference": "Section 6",
                "keywords": ["promptly", "10 business days", "timeframe", "specific", "return"],
            },
            {
                "issue_id": "hard_008",
                "category": "undefined_reference",
                "severity": "high",
                "description": "Schedule 1 (Permitted Advisors List) is referenced in Section 4 but is not attached. Without it, Acquiror has unlimited discretion over who qualifies as a 'permitted advisor.'",
                "section_reference": "Section 4 / Schedule 1",
                "keywords": ["schedule 1", "not attached", "advisors", "undefined", "missing schedule"],
            },
            {
                "issue_id": "hard_009",
                "category": "undefined_reference",
                "severity": "medium",
                "description": "Exhibit A (Transaction Overview) is referenced in the recitals but is not included. The defined scope of the 'Transaction' is therefore ambiguous.",
                "section_reference": "Recitals / Exhibit A",
                "keywords": ["exhibit a", "not included", "transaction", "undefined", "recital"],
            },
            {
                "issue_id": "hard_010",
                "category": "missing_clause",
                "severity": "critical",
                "description": "No signature blocks are present. The Agreement is not executed and therefore not legally binding on either party.",
                "section_reference": "Missing",
                "keywords": ["signature", "no signature", "not executed", "binding", "signed"],
            },
        ],
    },
}

TASKS: dict = {
    "task_easy": {
        "contract_id": "contract_easy",
        "description": (
            "You are a junior legal analyst. Review the Software License Agreement provided. "
            "Identify ALL legal issues — missing clauses, ambiguous terms, risky language, and missing elements. "
            "For each issue, propose a specific legally valid fix. Submit your audit when complete."
        ),
        "max_steps": 20,
        "difficulty": "easy",
        "num_issues": 5,
    },
    "task_medium": {
        "contract_id": "contract_medium",
        "description": (
            "You are a senior legal analyst. Review this Master Services Agreement carefully. "
            "It contains direct contradictions, compliance risks, and structural problems. "
            "Identify every issue with its section reference and severity. Propose fixes for all issues. "
            "Pay close attention to contradictions between subsections."
        ),
        "max_steps": 30,
        "difficulty": "medium",
        "num_issues": 8,
    },
    "task_hard": {
        "contract_id": "contract_hard",
        "description": (
            "You are a lead M&A legal counsel. Conduct a full due-diligence audit of this Mutual NDA. "
            "This is a complex document with subtle issues including undefined terms that cascade through "
            "the entire agreement, conflicting addenda of questionable enforceability, missing schedules, "
            "and dangerously low protection standards for sensitive financial data. "
            "Find ALL 10 issues, propose specific enforceable fixes for each, and submit a complete audit."
        ),
        "max_steps": 40,
        "difficulty": "hard",
        "num_issues": 10,
    },
}