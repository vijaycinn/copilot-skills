# territory-insights

> **Copilot CLI Skill** | v2.0.0 | Domain: Microsoft Field SE — Territory Intelligence

Generates a **fully-grounded quarterly territory leadership update** for any Microsoft field SE by orchestrating **MSX MCP** + **WorkIQ MCP** + optional local CSV analysis. Auto-detects your identity and territory — no manual config required.

**Output:** An 8-section HTML report (paste directly into Outlook) covering GitHub Copilot, App Dev Modernization, Azure AI/Foundry, competitive intelligence, macro themes, account spotlights, and prescriptive next-quarter recommendations — all cited from actual customer emails, meetings, and MSX pipeline data.

---

## Quick Start

```
territory-insights
```

That's it. The skill will:
1. Ask whether you want a **live-only** run or a **CSV-enhanced** run, and prompt for file paths if applicable
2. Detect your name, segment, and account list from MSX + M365
3. Ask you to confirm (or correct) before pulling data
4. Pull pipeline, milestones, HoK activities, and customer communications in parallel
5. Generate and save an HTML report to your chosen output folder
6. Auto-open in your browser — copy-paste into Outlook

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| GitHub Copilot CLI | latest | `gh extension install github/gh-copilot` |
| MSX MCP Server | — | Microsoft internal — required for pipeline/milestone data |
| WorkIQ MCP Server | — | Microsoft internal — required for customer email/meeting data |
| Python | 3.8+ | Optional — only needed for CSV ACR validation |

> **Network:** Must be on Microsoft corporate network or VPN for MSX and WorkIQ MCP access.
>
> **Optional local files for deeper validation:**  
> - Seller mapping / sales team export from the **Seller Success Dashboard** relevant Sales Team tab  
> - Performance exports from **MSX → Earnings → Performance Summary → Account Report**

---

## Installation

### Option A — From this repo

```powershell
# Windows
git clone https://github.com/vijaycinn/copilot-skills.git
Copy-Item -Recurse .\copilot-skills\territory-insights "$env:USERPROFILE\.copilot\skills\territory-insights"
```

```bash
# macOS / Linux
git clone https://github.com/vijaycinn/copilot-skills.git
cp -r copilot-skills/territory-insights ~/.copilot/skills/
```

### Option B — Download the folder directly

Download and unzip to `~/.copilot/skills/territory-insights/`.

### Verify

Open a new Copilot CLI session → type `skills`. You should see:

```
territory-insights   Generates quarterly territory leadership updates...
```

---

## What You Get

| Section | Source | Key Output |
|---------|--------|-----------|
| 📊 SE Activity Snapshot | MSX HoK | Activity count by type, stale milestone alert (🚨 if >80% stale), top accounts |
| 🐙 GitHub Copilot Insights | WorkIQ + MSX | Customer wins, blockers, competitive signals (code seats only — not M365 Copilot) |
| 🏗️ App Dev Modernization | WorkIQ + MSX | Active workloads, contacts, blockers, cloud-native SLG patterns |
| 🤖 Azure AI & Foundry | WorkIQ + MSX | Per-account: services, architecture, POC/pilot status, next steps |
| ⚔️ Competitive Intelligence | WorkIQ | AWS/Google/GitLab/legacy IVR signals and counters |
| 🌐 Macro / Industry Themes | Synthesized | GCC moat, citizen portal convergence, fiscal procurement windows |
| 🏆 Account Spotlights | CSV + MSX | ACR actuals vs. milestone projections — clearly separated |
| ✅ Recommendations | All sources | Tiered: POC→milestone, opp creation, milestone hygiene, DUAL-MISS calls |

---

## Optional: Personal Config

Create `my-config.md` in this folder (it's `.gitignore`-d so it won't be committed) to speed up corrections during Step 1 auto-detection. Use the template below:

```markdown
## Identity
| Field | Value |
|-------|-------|
| Name | Your Full Name |
| Email | alias@microsoft.com |
| Role | Sr. Digital Solutions Engineer |
| Alias | alias |

## Territory
| Field | Value |
|-------|-------|
| Segment | SMECC / ENT / SMC |
| Sub-segment | e.g., US Public Sector SLG / Commercial / Healthcare |
| ATU Codes | e.g., Industry.SMECC.USPS.0807 |

## Workspace Path (CSV exports)
C:\your\workspace\path\
```

---

## Optional: msx-perf-analyzer Complement

`territory-insights` handles inline ACR validation and DUAL-MISS analysis on its own. For a deeper **quota-weighted scorecard** with dual-miss prioritization tables and a full call sheet, run `msx-perf-analyzer` as a separate skill. The two work great together.

---

## Example Output

Generate your first report by invoking the skill with `territory-insights`. The output is an HTML file saved to your chosen folder that you can open in a browser and paste directly into Outlook.

---

## File Structure

```
territory-insights/
├── README.md                            ← this file
├── SKILL.md                             ← skill definition (Copilot CLI reads this)
├── territory_insights_instructions.md   ← full user guide (prerequisites, FAQ, troubleshooting)
├── .gitignore                           ← excludes my-config.md, my-accounts.md
└── references/
    ├── account-spotlight-format.md      ← Section 7 format guide + ACR validation checklist
    ├── html-template.md                 ← full HTML output template + PowerShell export
    └── ai-foundry-accounts.md           ← blank template for account AI engagement notes
```

---

## Full Documentation

See [`territory_insights_instructions.md`](./territory_insights_instructions.md) for:
- Prerequisites and MCP server setup
- Detailed step-by-step walkthrough
- CSV analysis and ACR validation guide
- Personalizing for your segment (ENT, SMC, Public Sector)
- Troubleshooting (WorkIQ auth, large account lists, MSX TPID lookup)
- FAQ

---

## Segment Coverage

The skill ships with generic defaults that work for any segment. Section 6 macro themes are tuned for **US Public Sector / SLG** out of the box — update them in `SKILL.md` if your territory differs:

| Segment | Adaptation needed |
|---------|------------------|
| SMECC USPS (SLG/SLED) | Ready to use as-is — GCC patterns and SLG macro themes built in |
| ENT / Large Enterprise | Update Section 6 macro themes; remove GCC requirement if not applicable |
| SMC | Same as ENT; Section 7 spotlights may need threshold adjustments |
| Healthcare | SLG patterns carry over; add HIPAA compliance notes to macro themes |

The Step 0 setup gate plus Step 1 auto-detection adapt to your segment automatically. Only the Section 6 default themes need manual tuning.
