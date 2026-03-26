# se-activity

> **Copilot CLI Skill** | v1.0.0 | Domain: Microsoft Field SE — MSX Activity Logging

Drafts and classifies **MSX SE Activity entries** from meeting notes, emails, or Teams conversations. Automatically maps your work to the correct FY26 SE Task Category and MSX scope — eliminating the manual lookup and formatting overhead of logging.

---

## Quick Start

Paste or describe what you did, and the skill produces a ready-to-paste MSX entry:

```
se-activity
```

Then either:
- **Paste** meeting notes / email content directly into the conversation, or
- **Pull from WorkIQ** — the skill will fetch recent emails or meeting notes for a specific account and date

---

## What It Does

| Step | Action |
|------|--------|
| **1. Gather input** | Paste notes or pull via WorkIQ by account + date |
| **2. Extract activities** | Identifies each discrete SE activity, date, account, contacts, and duration |
| **3. Classify** | Maps each activity to the correct FY26 SE Task Category |
| **4. Determine scope** | Picks Account / Opportunity / Milestone (most specific available) |
| **5. Draft entry** | Produces a formatted, ready-to-paste MSX SE Activity entry |
| **6. Review & confirm** | Iterates until you confirm accuracy before final output |

---

## FY26 SE Task Categories

| Category | Use When |
|----------|----------|
| **Architecture Design Session (ADS)** | Deep technical design, whiteboarding, solution architecture review |
| **Consumption Plan** | Azure consumption growth, MACC/ECIF planning, capacity alignment |
| **Customer Engagement** | Calls, check-ins, monthly reviews, technical briefings |
| **Demo** | Product/solution demonstrations, POC walkthroughs, feature showcases |
| **POC / Pilot** | Proof of concept design, execution, support, or readout |
| **Security Posture Review** | Zero Trust, compliance, identity, or security posture discussions |
| **Workshop** | Structured sessions, hackathons, immersion days, hands-on labs |
| **Tech Support** | Troubleshooting, escalation support, break-fix, reactive assistance |
| **Internal** | Internal Microsoft meetings, partner calls, readiness sessions |

> **Default:** `Customer Engagement` for any customer-facing touchpoint; `Internal` for Microsoft-only meetings.

---

## MSX Entry Format

Every drafted entry includes:

| Field | Notes |
|-------|-------|
| Subject | Always `SE Activity` |
| Task Category | From FY26 glossary above |
| Scope | Account / Opportunity / Milestone |
| Account | Customer name |
| Opportunity / Milestone | If applicable |
| Due Date | Date the activity occurred (not when logged) |
| Duration | Estimated or stated |
| Priority | Normal / High |
| Status | Completed |
| Description | 2–4 sentence impact-oriented summary |

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| GitHub Copilot CLI | `gh extension install github/gh-copilot` |
| MSX MCP Server | Microsoft internal — for looking up accounts/opportunities/milestones |
| WorkIQ MCP Server | Microsoft internal — optional, for pulling meeting notes from M365 |

> WorkIQ is optional but highly recommended. Without it, paste your meeting notes directly.

---

## Installation

```powershell
# Windows
git clone https://github.com/vijaycinn/copilot-skills.git
Copy-Item -Recurse .\copilot-skills\se-activity "$env:USERPROFILE\.copilot\skills\se-activity"
```

```bash
# macOS / Linux
git clone https://github.com/vijaycinn/copilot-skills.git
cp -r copilot-skills/se-activity ~/.copilot/skills/
```

Verify: open a new Copilot CLI session → type `skills` → `se-activity` should appear.

---

## Why Log SE Activities?

> SE Activity logging in MSX is how your technical contributions become **visible in KPI dashboards**, **justify headcount**, and **demonstrate SE influence on revenue**. Every ADS, demo, and POC you log ties your work directly to business outcomes — pipeline acceleration, consumption growth, and customer technical conviction. **Unlogged work is invisible work.**

Key rules:
- **One entry per activity type per session** — if a meeting covered both a Demo and an ADS, log two separate entries
- **Duration always required** — estimate if not stated (30 min for quick calls, 1 hr for standard meetings, 2+ hrs for workshops/ADS)
- **Account scope is your safety net** — if no Opportunity or Milestone exists, always log at Account level

---

## File Structure

```
se-activity/
├── README.md    ← this file
└── SKILL.md     ← skill definition (Copilot CLI reads this)
```
