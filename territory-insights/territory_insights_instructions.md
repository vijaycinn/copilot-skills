# Territory Insights Skill — User Guide

> **Skill:** `territory-insights`  
> **Version:** 2.1.0  
> **Author:** community  
> **Audience:** Microsoft field SEs and DSEs who need to generate quarterly territory leadership updates

---

## Table of Contents

1. [What This Skill Does](#what-this-skill-does)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start — Your First Run](#quick-start)
5. [How Auto-Detection Works](#how-auto-detection-works)
6. [The 8-Section Output](#the-8-section-output)
7. [Optional CSV Analysis](#optional-csv-analysis)
8. [Personalizing the Skill](#personalizing-the-skill)
9. [Decision Framework — What to Ask](#decision-framework)
10. [Output Files](#output-files)
11. [Troubleshooting](#troubleshooting)
12. [File Structure Reference](#file-structure-reference)
13. [Team Sharing and GitHub Repo](#team-sharing)
14. [FAQ](#faq)

---

## 1. What This Skill Does

`territory-insights` generates a **quarterly territory leadership update** for Microsoft field SEs. It works by:

1. **Checking your environment and optional file setup** (live-only vs. CSV-enhanced run)
2. **Auto-detecting your identity** from MSX and M365
3. **Pulling live data** from MSX (pipeline, milestones, HoK activities) via MSX MCP
4. **Surfacing customer voice** from your emails, Teams messages, and meeting transcripts via WorkIQ
5. **Optionally analyzing CSV exports** from MSX for ACR actuals and quota attainment
6. **Producing an 8-section HTML report** ready to paste into Outlook for leadership

### What it covers

| Section | Data source | What you get |
|---------|-------------|--------------|
| SE Activity Snapshot | MSX HoK activities | HoK count by type, stale milestone alert, top engaged accounts |
| GitHub Copilot Insights | WorkIQ + MSX | Customer wins, blockers, competitive signals (code seats only) |
| App Dev Modernization | WorkIQ + MSX opps | Active workloads, contacts, blockers, SLG patterns |
| Azure AI & Foundry | WorkIQ + MSX | Per-account engagement: services, architecture, status, next steps |
| Competitive Intelligence | WorkIQ | AWS/Google/legacy IVR threats and counters |
| Macro / Industry Themes | Synthesized | GCC moat, citizen portal convergence, SLG procurement cycles |
| Account Spotlights | CSV + MSX | ACR actuals vs. milestone projections — clearly separated |
| Recommendations | All sources | Tiered action list: POC→milestone, opp creation, hygiene |

### What it is NOT for

- ❌ Logging SE activities into MSX → use the `se-activity` skill
- ❌ M365 Copilot productivity insights → Business Solutions team, not SE quota
- ℹ️ Detailed quota scorecard with weighted tables → `msx-perf-analyzer` is an **optional complement** — but this skill can perform inline ACR validation and DUAL-MISS analysis on its own

---

## 2. Prerequisites

### Required — MCP Servers

You need two MCP servers configured and authenticated in your GitHub Copilot CLI:

| MCP Server | Purpose | How to check |
|-----------|---------|--------------|
| **MSX MCP** (`msx-mcp`) | Pulls your pipeline, milestones, HoK activities, account team | Run `/mcp` and look for `msx` in the list |
| **WorkIQ MCP** (`WorkIQ`) | Queries your M365 emails, Teams, meetings, calendar | Run `/mcp` and look for `WorkIQ` in the list |
| **Sales Home MCP** (`sales-home`) | Optional: territory-scoped Apps + AI ACR trend signal from Sales Home / MSXi | Run `/mcp` and look for `sales-home` in the list |

If either is missing, run `/mcp` in Copilot CLI and add the server. Contact your team admin for the server URL/config if needed.

### Optional — Python + CSV Analysis

For ACR validation and detailed attainment analysis:

- **Python 3.8+** installed and on PATH
- **MSX CSV exports** downloaded from the MSX reporting portal (see [Optional CSV Analysis](#optional-csv-analysis))
- **Optional seller mapping export** from the **Seller Success Dashboard** Sales Team tab when you want SSP / AE / DSE ownership called out in the report

### First-run setup note for new SEs / new territories

If this is a brand-new setup, the skill should stop and ask whether you want:

1. a **live-only run** using MSX MCP + WorkIQ, or  
2. a **CSV-enhanced run** where you also provide local file paths.

If you do not yet have the files, use these sources:

- **Seller mapping / sales team roster:** Seller Success Dashboard → Sales Team tab  
  `https://msxinsights.microsoft.com/User/report/058a8810-081f-4e06-b43b-60d3b983ae3e?reportTab=ReportSection410832002b044d169c9a&bookmark=d1ccaaa51a0d446b5a07`
- **Performance exports:** MSX → Earnings → Performance Summary → Account Report
- **Optional product detail export:** MSX → Earnings → Product Details

**Important guardrail:** if the provided account data does **not** already include a territory / ATU field, stop and ask the user which territories to scope to **before** doing any account analysis. For Vijay's default motion, that working set is `0807`, `0808`, `0909`, `0910`, `0911` unless the user corrects it.

### Supported Segments

This skill works for **any** Microsoft field SE segment. It was originally built for SMECC US Public Sector but the auto-detection, WorkIQ queries, and HTML output are fully generic.

Works with: SMECC, ENT, SMC, Global, Partner, CSU, and others.

---

## 3. Installation

### Option A: Clone from GitHub (Recommended for teams)

```bash
# Navigate to your Copilot skills directory
cd C:\Users\[your-alias]\.copilot\skills

# Clone the skill repo
git clone https://github.com/[org]/territory-insights

# Reload skills in Copilot CLI
# In Copilot CLI, run:
/skills
```

### Option B: Manual copy from a teammate

1. Ask your teammate for a zip of their `territory-insights` folder
2. Extract to: `C:\Users\[your-alias]\.copilot\skills\territory-insights\`
3. In Copilot CLI, run `/skills` to reload

### Option C: Copy from a shared network path

```powershell
# Copy from shared location
Copy-Item -Recurse "\\shared\copilot-skills\territory-insights" `
  "$env:USERPROFILE\.copilot\skills\territory-insights"
```

### Verify Installation

In Copilot CLI, type:
```
/skills
```
You should see `territory-insights` listed. If not, check that the folder contains a `SKILL.md` file at the root.

---

## 4. Quick Start — Your First Run

Once installed, just ask naturally:

```
Generate my territory update for this quarter
```

or

```
What are customers saying about GitHub Copilot and AI in my territory?
```

or

```
Which accounts should I call this week?
```

The skill will:
1. **Ask about setup first** — live-only vs. CSV-enhanced, plus optional local file paths
2. **Confirm territory scope first** — if it is not already present in the account data
3. **Auto-detect you** — calls MSX and M365 to find your name, email, accounts, and segment
4. **Confirm before running** — shows you what it detected and asks if you want to proceed
5. **Pull all data** — runs MSX and WorkIQ queries in parallel
6. **Generate the report** — produces the 8-section update
7. **Save as HTML** — asks where to save, then opens in your browser
8. **Draft the email** — optionally creates a draft in your Outlook (requires M365 auth)

**First run takes ~2–3 minutes** (parallel MCP calls). Subsequent runs are similar if you're pulling fresh data.

---

## 5. How Auto-Detection Works

The skill runs two lookups in parallel before doing anything else:

```
1. WorkIQ-Me-MCP-Server-GetMyDetails
   → Your name, email, job title from your M365 profile

2. msx-mcp-get_account_team
   → Your assigned accounts, roles, solution areas from MSX
```

It then:
- Infers your **segment** from account team patterns (e.g., "SMECC", "ENT", "SMC")
- Builds your **accounts list** from all accounts you're assigned to in MSX
- Determines the **current fiscal quarter** from today's date

You'll see a confirmation message like:
> "I'll generate a territory update for **Jane Smith** (jsmith@microsoft.com) covering **47 accounts** in **SMECC US Public Sector**. Current quarter: **Q3 FY26**. Proceed — or correct anything above?"

### If auto-detection is wrong or fails

Just correct it in your reply. For example:
- "Yes, but use Q4 FY26 instead"
- "Actually I'm Jane Smith, Sr. CSE, SMC West"
- "My segment is ENT, not SMECC"

All downstream queries use your corrected values.

### Territory-first behavior

This skill should never start from **all Microsoft accounts** and then drill down.

Instead:

1. detect or ask for the territory / ATU scope first
2. restrict the account set immediately
3. only then use Sales Home / MSXi, MSX, and WorkIQ to prioritize actions

If a seller mapping file or account list already contains the territory field, reuse it and do not prompt again.

### Persisting your config (optional)

If you want to skip the auto-detection step on every run, create a personal config file:

```
C:\Users\[your-alias]\.copilot\skills\territory-insights\my-config.md
```

Use `references/ai-foundry-accounts.md` as a template. Include your name, email, segment, ATU codes, and default workspace path. The skill checks for this file and skips auto-detection if found.

---

## 6. The 8-Section Output

### Section 1 — SE Activity Snapshot
- Total HoK activities this quarter, broken down by type (ADS / Workshop / POC / Technical Close)
- Stale milestones count — flagged **URGENT** if >40% are stale
- Total pipeline count and open opportunities
- Top 5 most-engaged accounts

### Section 2 — GitHub Copilot (Code) — Customer Insights
> **Important:** This covers GitHub Copilot code seats ONLY — not M365 Copilot for productivity.

- Wins: accounts above quota, seat expansion signals surfaced from WorkIQ
- Blockers: common friction points (ADO vs. GitHub Actions migration, GitLab competition, per-seat budget)
- Competitive signals: GitLab, bundling confusion
- Territory pattern: upsell adjacency to App Service / Build Modernize accounts

### Section 3 — App Dev Modernization — Customer Insights
- Active modernization engagements (account + workload + stage) from MSX + WorkIQ
- Key external contacts surfaced from emails/meetings (name, title, org)
- Blockers: compliance chains, fiscal year cycles, security approvals
- Macro pattern: lift-and-shift → cloud-native (Bicep, microservices, event-driven)

### Optional prioritization signal — Sales Home / MSXi

When `sales-home` is available, use it to create a territory-scoped **“growing ACR”** shortlist before you write recommendations:

- `Account Last Month ACR`
- `Account MOM $`
- `Account MOM %`
- `Strategic Pillar`
- `WorkLoadName`

Recommended output columns:

`Account | TPID | Territory | Bucket (Apps / AI) | Top Workload | Current ACR | Prior ACR | Delta $ | Delta % | Recommended conversation`

This makes the skill much more actionable for the sales team because the result is no longer just “interesting signal” — it becomes “who should we call this week, and about what?”

### Section 4 — Azure AI and Foundry — Engagement Highlights
The most important section for leadership. Built from WorkIQ + MSX.

For each account with an active AI/Foundry engagement:
- Services scoped, use case description, architecture notes
- GCC compliance status (critical for US Public Sector)
- Customer contacts and Microsoft team
- Status and committed next steps

**Common AI patterns the skill surfaces when found:**
- **Content Understanding**: document indexing, records management, large unstructured data
- **Voice Agent (ACS + Speech)**: IVR modernization, multilingual citizen routing
- **AI Translation**: multilingual city/county communications and accessibility
- **Azure AI Foundry + RAG**: citizen knowledge portals, document Q&A

### Section 5 — Competitive Intelligence
- AWS (Bedrock/SageMaker), Google Workspace, GitLab, legacy IVR vendors (Mitel/Genesys/Avaya)
- Counter-positioning per competitor
- Sourced from WorkIQ customer conversation signals

### Section 6 — Macro / Industry Themes
Four recurring themes for SLG/Public Sector (adjust for your segment):
1. GCC compliance as competitive moat
2. Hybrid architecture preference (AI on top of existing on-prem infra)
3. Citizen portal convergence (multilingual + voice + document-aware)
4. Q-next procurement windows (fiscal close alignment)

### Section 7 — Account Spotlights
For each spotlight account:
- **Actual ACR** from CSV (ground truth) — labeled clearly
- **MSX milestone pipeline** — labeled as forward projections
- Key contacts from WorkIQ
- Q-next action

> ⚠️ **Critical:** MSX "Consumed Recurring" ≠ monthly run rate. MSX milestone "Est. Monthly Use" ≠ current consumption. Both are projections. Only the CSV gives you actual billed ACR. The skill enforces this separation automatically.

### Section 8 — Recommendations and Next-Quarter Focus
Tiered action list:
1. POC → Milestone conversion (active pilots close to production)
2. Post-meeting → Opportunity creation (informal engagements ready to formalize)
3. Demo → Advance (accounts with strong AI signal but no committed action)
4. EA Milestone close — committed milestones due within 30 days
5. Milestone hygiene — stale milestone remediation
6. Top weighted gap account — priority call from attainment data

---

## 7. Optional CSV Analysis

For accurate ACR figures and quota attainment, the skill can analyze CSV exports from MSX.

### Downloading your CSVs

1. Log in to [MSX](https://microsoftsalesexperience.microsoft.com)
2. Navigate to **Reports → Attainment** and export:
   - **Attainment Report** → `AttainmentReport__YYYY_NNN.csv`
   - **Account Performance Summary** → `PerformanceSummary_AccountReport_YYYY_NNN.csv`
   - **Product Details** → `ProductDetails_[ALIAS]_YYYY_NNN.csv`

### Using the CSVs with the skill

When you ask for a territory update or ACR validation, the skill will ask:
> "Do you have MSX performance CSV exports? If so, please provide the full path to your workspace folder."

Provide the folder path (e.g., `C:\workspace\myterritory\`) and it will automatically find the right files.

### CSV encoding note

MSX CSV exports use UTF-8-sig encoding and include a `sep=` header row. The skill handles both automatically. If you get a `KeyError` or encoding error, check that you haven't modified the file in Excel (which can corrupt the encoding).

### What the analysis produces
- Quota attainment % per account and metric
- Dual-miss accounts (missing both AI and ACR quotas)
- Month-over-month ACR trend
- Correct separation of actual consumption vs. milestone projections

---

## 8. Personalizing the Skill

### Option A: Personal config file (no-edit approach)

Create `C:\Users\[alias]\.copilot\skills\territory-insights\my-config.md`:

```markdown
# My Territory Config

## Identity
- Name: [Your Full Name]
- Email: [your@microsoft.com]
- Role: [Your Job Title]
- Alias: [youralias]

## Territory
- Segment: [e.g., SMECC, ENT, SMC]
- Sub-segment: [e.g., US Public Sector State/Local Government]
- ATU Codes: [e.g., Industry.SMECC.USPS.0807]

## Quota Buckets
- AI Platform and Apps: [weight%]
- Total ACR: [weight%]

## Default Workspace Path
[C:\path\to\your\csv\exports\]

## Notes
[Any segment-specific rules, e.g., GCC requirement, M365 scope]
```

### Option B: Add your account engagement notes

Create `my-accounts.md` in the skill folder following the template in `references/ai-foundry-accounts.md`. Fill in your own active accounts, architecture notes, and next actions.

### Option C: Adjust the HTML template

Edit `references/html-template.md` to change colors, sections, or branding. The skill uses this template when generating HTML output.

---

## 9. Decision Framework — What to Ask

| What you want | What to say |
|---------------|-------------|
| Full quarterly update | "Generate my territory leadership update for this quarter" |
| Customer AI insights only | "What are customers saying about Azure AI in my territory?" |
| GitHub Copilot customer voice | "What are customers saying about GitHub Copilot?" |
| App Dev customer signals | "What App Dev modernization conversations have I had?" |
| Priority call list | "Which accounts should I call this week?" |
| ACR validation | "Validate the ACR claim for [account name]" |
| Add a specific account | "Add [account] to the AI section of the update" |
| Regenerate/update the HTML | "Update the leadership update HTML" |
| Check your identity/territory | "Who am I? What's my territory?" |

---

## 10. Output Files

### HTML Report (primary output)

The skill asks where to save and generates:
```
[output-folder]\[QUARTER]-[FY]-Leadership-Update-[alias]-v[N].html
```

Example: `C:\workspace\Q3-FY26-Leadership-Update-jsmith-v1.html`

- Opens automatically in your default browser
- Use **Ctrl+A → Ctrl+C** to copy all content
- Paste directly into Outlook (compose new email) — formatting is preserved
- Paste into Word for a document version

### Outlook Draft (secondary output)

If WorkIQ M365 auth is active, the skill creates a draft email sent to yourself for review. Subject format:
```
Q[N] FY[YY] Territory Insights — Leadership Update | [SEGMENT] | [Your Name]
```

**If you get an `AADSTS900144` auth error:** Use the HTML file instead. Retry the email draft 5–10 minutes later when the token refreshes. Never block the full run on email auth failure.

---

## 11. Troubleshooting

### "MSX auth failed" or "No opportunities found"

**Cause:** MSX MCP token expired.  
**Fix:** Run `/mcp` and check the MSX MCP server status. You may need to re-authenticate. Try `msx-mcp-msx_login` to re-auth.

### "No results from WorkIQ for [account]"

**Cause:** The account name doesn't match how it appears in your emails/calendar.  
**Fix:** Try alternate name formats:
- Short name: `"Springfield"` instead of `"City of Springfield"`
- With state prefix: `"IL-City of Springfield"`
- Topic-first: `"IVR modernization meeting"` instead of account-first search

### "CSV file not found" or Python KeyError

**Cause:** Wrong workspace path, or CSV has `sep=` header / UTF-8 BOM.  
**Fix:** Verify the folder path contains the CSV files. The skill strips `sep=` headers and UTF-8 BOM automatically — if the error persists, check that the CSV was not re-saved from Excel (which corrupts encoding).

### "Wrong identity detected in Step 1"

**Cause:** Multiple M365 profiles or wrong MSX account team.  
**Fix:** When the skill shows you the detected identity, simply correct it in your reply. E.g., "Yes, but my segment is ENT not SMECC."

### "msx_analyze.py not found"

**Cause:** This skill does not call `msx_analyze.py` directly. Inline ACR validation uses an embedded Python snippet that only needs a workspace folder path.  
**Fix:** Provide your workspace folder path when prompted. If you want the full quota scorecard script, run the **optional** `msx-perf-analyzer` skill separately.

### HTML output is blank or shows template placeholders

**Cause:** MCP data pulls returned no results.  
**Fix:** Check your MSX and WorkIQ MCP server auth. Run a simple test: ask "show me my open MSX opportunities" — if that works, the issue is in the skill's query construction.

---

## 12. File Structure Reference

```
C:\Users\[alias]\.copilot\skills\territory-insights\
│
├── SKILL.md                          ← Main skill definition (auto-detected, generic)
│
├── territory_insights_instructions.md  ← This file
│
├── references\
│   ├── html-template.md              ← HTML output template (generic placeholders)
│   ├── account-spotlight-format.md   ← Format guide for Section 7 spotlights
│   └── ai-foundry-accounts.md        ← TEMPLATE: blank account profile template
│
└── my-config.md                      ← YOUR personal config (create this; not in repo)
    my-accounts.md                    ← YOUR account notes (create this; not in repo)
```

---

## 13. Team Sharing and GitHub Repo

### Publishing the skill to GitHub

The `territory-insights` folder is designed for GitHub distribution. Before pushing:

1. **Never commit personal data.** Add the following to `.gitignore`:
   ```
   my-config.md
   my-accounts.md
   ```

2. **What gets shared (safe to commit):**
   - `SKILL.md` — generic skill definition
   - `references/` — generic templates and format guides
   - `territory_insights_instructions.md` — this file

3. **What stays personal (never commit):**
   - `my-config.md` and `my-accounts.md` (your personal overrides)

### How teammates install from GitHub

```bash
# Install to skills directory
cd C:\Users\[alias]\.copilot\skills
git clone https://github.com/[org]/territory-insights

# Or if using GitHub Copilot CLI /skills:
# /skills → browse → install from URL
```

### Keeping up to date

```bash
cd C:\Users\[alias]\.copilot\skills\territory-insights
git pull origin main
```

Then run `/skills` in Copilot CLI to reload.

---

## 14. FAQ

**Q: Can I use this skill for Enterprise (ENT) or SMC segments, not just Public Sector?**  
A: Yes. The skill auto-detects your segment from MSX. The GCC requirement and SLG macro themes only apply if you're in Public Sector — the skill confirms with you whether they apply. Everything else works for any segment.

**Q: Do I need the CSV files to run the skill?**  
A: No. The skill works fully from MSX and WorkIQ live data. CSVs are only needed for precise ACR actuals (the skill will note that ACR figures are from MSX projections only if CSVs aren't available).

**Q: What's the difference between this skill and `msx-perf-analyzer`?**  
A: `msx-perf-analyzer` is an **optional complement** — it produces a detailed **scorecard** with quota-weighted tables, gap analysis, dual-miss rankings, and a prioritized call sheet from your CSV exports. `territory-insights` is **self-contained** — it produces a narrative leadership update (customer voice, AI engagement stories, competitive intel, recommendations) and can perform inline ACR validation and DUAL-MISS analysis directly from MSX data. Run `msx-perf-analyzer` first if you want the full quota scorecard; `territory-insights` works fine without it.

**Q: The skill detected my accounts but some are wrong — there are accounts I'm not active on.**  
A: This is normal — MSX `get_account_team` returns all assigned accounts, including inactive ones. When the skill shows you the confirmation, reply with "yes but focus only on accounts with open opportunities" and it will filter accordingly.

**Q: Can I use this skill for a different quarter, not the current one?**  
A: Yes. Just specify: "Generate the territory update for Q2 FY26" and the skill will adjust the date references throughout.

**Q: How do I update Section 4 after a new customer meeting?**  
A: Ask: "Add [account name] to the Azure AI section with these notes: [your meeting notes]" — the skill will integrate it. To make it permanent, add a profile to `my-accounts.md` using the template in `references/ai-foundry-accounts.md`.

**Q: How do I share the generated HTML with my manager?**  
A: Open the HTML file in your browser → Ctrl+A → Ctrl+C → open Outlook → New Email → paste. Formatting is preserved. Or use the Outlook draft option (if auth is working).

**Q: My team uses a shared `workspace` folder. Can I point the skill there?**  
A: Yes. When the skill asks for your workspace path, provide the shared folder path. You can also set this as the default in your `my-config.md`.

---

*Last updated: March 2026 | Skill version 2.0.0 | Community contribution*  
*For issues or improvements: open a GitHub issue on the skill repo*
