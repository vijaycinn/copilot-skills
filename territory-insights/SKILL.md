---
name: territory-insights
description: "Generates quarterly territory leadership updates for Microsoft field SEs by orchestrating MSX MCP and WorkIQ MCP data sources with optional local CSV analysis. Auto-detects the invoking SE's identity and territory from MSX + M365. Produces insights covering GitHub Copilot, App Dev Modernization, Azure AI/Foundry, competitive intelligence, account spotlights, and prescriptive next-quarter recommendations — all grounded in actual customer emails, meetings, and MSX pipeline data. Use when user asks for territory insights, leadership update, quarterly review, customer insights, Q3/Q4 update, what are customers saying, GitHub App Dev Azure AI insights, accounts to call, SE activity insights, or to validate ACR milestone claims."
metadata:
  version: "2.0.0"
  author: community
  domain: Microsoft Field SE — Territory Intelligence
user-invocable: true
---

# Territory Insights - Quarterly Leadership Update Generator

Orchestrates MSX MCP + WorkIQ MCP + optional local CSV analysis to generate a fully-grounded quarterly territory leadership update for any Microsoft field SE. Auto-detects the SE's identity, segment, and accounts from live MSX and M365 data. Covers GitHub Copilot, App Dev Modernization, Azure AI/Foundry, competitive intelligence, macro themes, and prescriptive call recommendations — all cited from actual customer emails, meetings, and MSX pipeline data.

---

## Step 0: Environment, Dependencies, and Optional File Setup (Always Run First)

Before any auto-detection or MCP calls, **start with a setup gate** so the skill works for a new SE, a different territory, or a fresh machine.

**Ask the user one concise setup question first:**

> "Do you want a live-only territory update from MSX + WorkIQ, or a CSV-enhanced run with local export files? If you already have the files, send the folder path or exact file paths. If not, I’ll show you where to get them first."

### Tell the user where optional local files come from

If the user wants CSV-enhanced analysis, account spotlights, or seller mapping and they do **not** already have the files, explain:

1. **Account-to-seller mapping (SSP / AE / DSE / CE)**  
   Get this from the **Seller Success Dashboard** → relevant **Sales Team** tab for the territory:  
   `https://msxinsights.microsoft.com/User/report/058a8810-081f-4e06-b43b-60d3b983ae3e?reportTab=ReportSection410832002b044d169c9a&bookmark=d1ccaaa51a0d446b5a07`

2. **Performance CSVs / attainment exports**  
   Export from **MSX → Earnings → Performance Summary → Account Report** (and optionally Product Details if deeper metric validation is needed).

3. **Workspace folder path**  
   Ask the user for the local folder containing the exports if they want inline CSV validation or HTML output saved to a specific location.

### Dependencies that may vary by user environment — call these out before proceeding

| Dependency | Why it matters | Fallback |
|------------|----------------|----------|
| **MSX MCP access** | Needed for account team, deals, milestones, HoK | Use local exports only if MSX access is missing |
| **WorkIQ MCP access + accepted EULA** | Needed for customer email / Teams / meeting grounding | Skip customer-voice sections if unavailable |
| **Corporate network / VPN** | Often required for Microsoft internal data sources | Reconnect before continuing |
| **Python 3.8+** | Needed for optional CSV/ACR validation | Run live-only mode if unavailable |
| **Excel installed or CSV export available** | Some XLSX exports need Excel automation on Windows | Ask the user to re-save/export as CSV |
| **Outlook / Mail permissions** | Needed only if drafting the final update email | Save HTML locally instead |

Do **not** assume a default workspace path or existing exports for a new seller. If files are missing, stop and explain the setup path before you start processing.

## Step 1: Identity and Territory Auto-Detection

Run BOTH calls in parallel before doing anything else:

```
1. WorkIQ-Me-MCP-Server-GetMyDetails    → Captures: displayName, mail, jobTitle
2. msx-mcp-get_account_team(limit=250)  → Captures: accounts list, role, solution area, ATU group
```

> **Note:** The default limit is 50. Always pass `limit=250` (the tool maximum) to capture the full account team. If you have more than 250 accounts, page with a second call.

**Compose user context from results:**

| Variable | Source | Example |
|----------|--------|---------|
| `$SELLER_NAME` | GetMyDetails → displayName | "Jane Smith" |
| `$SELLER_EMAIL` | GetMyDetails → mail | "jsmith@microsoft.com" |
| `$SELLER_ALIAS` | Derived: `$SELLER_EMAIL` split on `@`, take first part | "jsmith" |
| `$SELLER_ROLE` | GetMyDetails → jobTitle | "Sr. Digital Solutions Engineer" |
| `$SEGMENT` | get_account_team → solution area / segment pattern | "SMECC", "ENT", "SMC" |
| `$ACCOUNTS_LIST` | get_account_team → account name list (all assigned accounts) | ["Contoso", "Fabrikam", ...] |
| `$FISCAL_QUARTER` | Derived from current date using Microsoft FY calendar below | "Q3" |
| `$FISCAL_YEAR` | Derived from current date using Microsoft FY calendar below | "FY26" |
| `$NEXT_QUARTER` | Derived: quarter after `$FISCAL_QUARTER`, wrapping FY if needed | "Q4" |

**Microsoft Fiscal Year Calendar (use to derive `$FISCAL_QUARTER` and `$FISCAL_YEAR`):**

| Calendar months | Fiscal Quarter | FY rule |
|----------------|----------------|---------|
| July – September | Q1 | FY = calendar year + 1 (e.g., Jul–Sep 2025 = Q1 FY26) |
| October – December | Q2 | FY = calendar year + 1 (e.g., Oct–Dec 2025 = Q2 FY26) |
| January – March | Q3 | FY = calendar year (e.g., Jan–Mar 2026 = Q3 FY26) |
| April – June | Q4 | FY = calendar year (e.g., Apr–Jun 2026 = Q4 FY26) |

**Quarter months** (used in Section 7 ACR tables):

| Fiscal Quarter | Month 1 | Month 2 | Month 3 (partial) |
|---------------|---------|---------|-------------------|
| Q1 | July | August | September |
| Q2 | October | November | December |
| Q3 | January | February | March |
| Q4 | April | May | June |

**Confirm with user (one message):**

> "I'll generate a territory update for **$SELLER_NAME** ($SELLER_EMAIL) covering **N accounts** in **$SEGMENT**. Current quarter: **$FISCAL_QUARTER**. Proceed — or correct anything above?"

**If detection fails or user provides corrections:**

Ask the user:
> "Please provide: your name, email, Microsoft segment (e.g., SMECC, ENT, SMC), territory ATU codes or names, fiscal quarter (e.g., Q3 FY26), and segment type (e.g., US Public Sector State/Local/Healthcare)."

Store all resolved values as `$SELLER_NAME`, `$SELLER_EMAIL`, `$SELLER_ALIAS`, `$SELLER_ROLE`, `$SEGMENT`, `$ACCOUNTS_LIST`, `$FISCAL_QUARTER`, `$FISCAL_YEAR`, `$NEXT_QUARTER` for use throughout the rest of this skill.

---

## Territory Context (Populated at Runtime)

Values below are populated from Step 1 auto-detection:

- **Seller:** `$SELLER_NAME` (`$SELLER_EMAIL`) — `$SELLER_ROLE`
- **Segment:** `$SEGMENT`
- **Accounts:** `$ACCOUNTS_LIST` (from MSX account team)
- **Current quarter:** `$FISCAL_QUARTER`

**Quota Buckets** (confirm with user if different from defaults below):

| Bucket | Default Weight | Key Metrics |
|--------|----------------|-------------|
| AI Platform and Apps | 70% | Azure AI, Build/Modernize Apps, GitHub Copilot (code) |
| Total ACR | 30% | ACR-Core, Partner Reported ACR, MBS Co-Sell |

**GCC requirement (US Public Sector):** Every AI conversation must be scoped to GCC compliance first. Confirm with user if this applies to their segment.

**M365 Copilot scope:** By default treated as OUT OF SCOPE for SE quota (Business Solutions team). GitHub Copilot (code seats) is IN scope. Confirm with user if their segment differs.

---

## When to Use This Skill

**Triggers - activate this skill when:**
- User asks for "territory update", "leadership update", "quarterly insights", "Q3/Q4 update"
- User asks "what are customers saying about GitHub / App Dev / AI?"
- User asks "which accounts should I focus on?" or "who should I call this week?"
- User asks to "summarize SE activities" or "summarize MSX milestones"
- User asks to validate an ACR claim, milestone value, or attainment figure
- User shares CSV files (optionally use alongside msx-perf-analyzer for detailed scorecard)
- User asks about specific accounts in their territory (accounts list discovered from MSX in Step 1)

**Anti-triggers - do NOT use this skill when:**
- User wants to LOG activities into MSX (use se-activity skill instead)
- User asks about M365 Copilot for productivity (Business Solutions team, not SE quota)

---

## Data Sources and MCP Tools

### Step 2: Run all pulls IN PARALLEL

```
1. MSX Pipeline:       msx-mcp-get_my_deals             - open opportunities
2. MSX Milestones:     msx-mcp-get_my_milestones        - consumption milestone pipeline
3. MSX SE Activities:  msx-mcp-get_my_hok_activities    - HoK activity log current quarter
4. WorkIQ Customer:    workiq-ask_work_iq               - external customer emails/meetings/Teams
```

### Step 3: Optional CSV Analysis (when files available)

CSV files from MSX exports provide actual billed ACR and quota attainment data that MSX pipeline data alone cannot supply.

**Option A — Inline analysis (default):** Use the Python validation snippet in the [ACR and Claim Validation Workflow](#acr-and-claim-validation-workflow) section below. Ask the user for their workspace folder path and run the snippet directly. No external skill dependency.

**Option B — Full scorecard (recommended if available):** If the user has the `msx-perf-analyzer` skill installed and wants detailed quota-weighted tables, dual-miss rankings, and a full call sheet, suggest it as a complement:

> "I can pull attainment numbers inline from your CSV files. If you also want a full quota scorecard with weighted tables and prioritized call sheet, run the `msx-perf-analyzer` skill separately — it provides deeper analysis. Shall I proceed with inline ACR validation, or would you prefer to run `msx-perf-analyzer` first?"

**If the user hasn't run msx-perf-analyzer or declines:** proceed with inline CSV analysis for ACR validation and derive DUAL-MISS prioritization from MSX milestone/pipeline data directly.

Expected CSV file naming (standard MSX export format):
```
AttainmentReport__YYYY_NNN.csv
PerformanceSummary_AccountReport_YYYY_NNN.csv
ProductDetails_[ALIAS]_YYYY_NNN.csv
```

CSV encoding note: MSX exports use UTF-8-sig with a `sep=` header row. The validation snippet below handles both automatically.

### WorkIQ Query Strategy (send two queries in parallel)

**Account filtering — always apply before building WorkIQ queries:**

With large account lists (>20 accounts), passing all names to WorkIQ produces poor results. Filter first:

1. Use `$DEALS` (from `msx-mcp-get_my_deals`) to identify accounts with open opportunities
2. Rank by estimated deal value (descending)
3. Take the **top 8–10 accounts** — these are the active accounts most likely to appear in your emails and calendar
4. Use only these filtered accounts as `$ACTIVE_ACCOUNTS` in the WorkIQ queries below

If `get_my_deals` returns no results, fall back to the most recently modified 8–10 accounts from `$ACCOUNTS_LIST`.

**Query 1 - GitHub and App Dev:**
```
"Find emails, Teams messages, and meeting transcripts with external customers (non-microsoft.com)
about GitHub, GitHub Copilot, App Dev modernization, Azure App Service, AKS, Functions.
Accounts: [INSERT $ACTIVE_ACCOUNTS].
Return: key customer quotes, blockers, wins, next steps, competitive signals."
```

**Query 2 - Azure AI and Foundry:**
```
"Find emails, Teams messages, and meeting transcripts with external customers about
Azure AI, Azure AI Foundry, Content Understanding, voice agents, IVR, ACS, Copilot Studio,
citizen portals, speech-to-text, document intelligence.
Accounts: [INSERT $ACTIVE_ACCOUNTS].
Return: architecture discussions, POC status, stakeholder names, next steps."
```

---

## 8-Section Leadership Update Structure

### Section 1 - SE Activity Snapshot

From msx-mcp-get_my_hok_activities:
- Total HoK activities this quarter (count by type: ADS / Workshop / POC / Technical Close)
- Stale milestones count — flag as **URGENT** if >80% of your milestones are stale
- Total pipeline count and open opportunities
- Top 5 most-engaged accounts this quarter

### Section 2 - GitHub Copilot (Code) - Customer Insights

IMPORTANT: GitHub Copilot = code seats only. NOT M365 Copilot.

From WorkIQ + MSX:
- Wins: accounts above quota, seat expansion signals
- Blockers: ADO vs GitHub Actions migration inertia, GitLab compete, per-seat budget scrutiny
- Competitive signals: GitLab, bundling confusion (GitHub vs M365)
- Territory pattern: GitHub Copilot upsell follows naturally from App Service / Build Modernize adoption

### Section 3 - App Dev Modernization - Customer Insights

From WorkIQ + MSX opportunities with Sales Play = Build/Modernize:
- Active modernization engagements (list account + workload + stage)
- Key external contacts surfaced from WorkIQ (name, title, org email domain)
- Blockers: compliance requirements (segment-appropriate — e.g., FedRAMP/GCC for Public Sector; SOC2/ISO27001 for commercial), security approval chains, fiscal year cycles
- Macro pattern for SLG: moving from lift-and-shift to cloud-native (Bicep IaC, microservices, event-driven); adapt this pattern for your segment's dominant workload

### Section 4 - Azure AI and Foundry - Engagement Highlights

Populate from WorkIQ Query 2 + MSX milestones. For each account with an active AI/Foundry engagement surfaced in WorkIQ or MSX:

**Document per account:**
- Azure services scoped (e.g., AI Foundry, Content Understanding, ACS, Speech, AI Translation)
- Use case description (citizen portal, document AI, IVR modernization, etc.)
- Architecture approach — cloud-only vs. hybrid; GCC compliance status
- Key customer contacts (surfaced from WorkIQ emails/meetings: name + title)
- Current status (POC, architecture session, pilot, production)
- Next steps (committed actions from last meeting)

**Common SLG AI patterns to surface when found in WorkIQ:**

| Pattern | Signal to look for | Azure services |
|---------|-------------------|----------------|
| Content Understanding | "document indexing", "records management", "30-40TB unstructured" | AI Foundry + Content Understanding + Cosmos DB |
| Voice Agent / IVR | "IVR modernization", "citizen routing", "replace Mitel/Genesys/Avaya" | ACS + Speech + AI NLU |
| AI Translation | "multilingual", "accessibility", "citizen communications" | AI Translation + Speech (TTS/STT) |
| RAG / Knowledge Base | "search across documents", "citizen Q&A portal", "internal knowledge" | AI Foundry + AI Search + GPT-4.x |

**GCC COMPLIANCE NOTE:**
Every AI recommendation in US Public Sector must be scoped to GCC first.
Azure AI Foundry FedRAMP High + GCC High is the consistent differentiator vs. AWS Bedrock and Google Vertex AI.
Always confirm GCC availability for every service being proposed.

**Macro Insight (include in every update):**
Surface the dominant AI pattern across your territory accounts this quarter.
Format: "[N] independent accounts in your territory converged on [pattern] as the operational-grade AI use case for [segment]. [One-sentence business implication]."

> **For reference examples** of how to document specific account AI engagements, see `references/ai-foundry-accounts.md` — it contains a template covering Content Understanding, Voice Agent, and Translation patterns. Populate `my-accounts.md` in the skill folder with your own territory's account notes using that template.

### Section 5 - Competitive Intelligence

From WorkIQ customer discussions:
- AWS (SageMaker/Bedrock): Surfacing on AI/ML in large SLG accounts.
  Counter: Azure AI Foundry GCC + Microsoft national security credentials (DoD, CISA)
- Google Workspace: Competitive at smaller municipalities on productivity; weak on Azure AI workloads
- GitLab: Open-source preference at developer-led accounts.
  Counter: GitHub native Azure integration + GCC compliance + Copilot code seats
- Mitel/Genesys/Avaya: Legacy IVR at renewal cycles - ACS is the displacement play
- OpenAI direct: Not surfacing in SLG; customers default to Azure OpenAI for data residency

### Section 6 - Macro / Industry Themes

> **Segment guidance:** The default themes below are tuned for **US Public Sector / SLG (State, Local Government, Healthcare)**. If your segment is ENT, SMC, or another, replace with the dominant macro themes relevant to your customers. The structure (4 themes, business implication each) stays the same.

**Default themes for US Public Sector / SLG:**

1. **GCC compliance as competitive moat:** Every AI conversation requires GCC scoping.
   Azure AI Foundry FedRAMP High + GCC High is consistent differentiator vs. AWS Bedrock and Google Vertex AI.
2. **Cloud-first, low-migration appetite:** SLG wants AI ON TOP of existing on-prem infra
   (OnBase, Mitel, legacy DMS) — hybrid architecture is the resonant model.
3. **Citizen portal convergence:** multilingual + voice-capable + document-aware portal.
   2–3 year transformation; we are at foundation-setting stage now.
4. **Q-next procurement window:** Q4 (Apr–Jun) is peak SLG fiscal close.
   MACC draws and EA renewals are primary vehicles.

### Section 7 - Account Spotlights

For each spotlight account include: actual ACR from CSV (if available), MSX pipeline, and next action.
Use the format template in `references/account-spotlight-format.md`.

ACR VALIDATION RULE — ALWAYS APPLY:
MSX milestone "Est. Monthly Use" = forward projection, NOT current consumption.
Validate every ACR claim against the account performance CSV before publishing.

**Spotlights to include (prioritized from MSX + WorkIQ data):**

1. **Highest ACR accounts** — from CSV if available, otherwise from MSX Consumed Recurring
2. **DUAL-MISS accounts** — accounts missing both AI and ACR quota buckets (highest leverage)
3. **Active POC accounts** — accounts with in-flight technical engagements this quarter
4. **Milestone-close accounts** — committed milestones due within 30 days

Use `msx-perf-analyzer` skill output (if run) to populate the DUAL-MISS prioritization — otherwise derive from MSX milestones: accounts missing both an active AI milestone and an ACR milestone are DUAL-MISS.

> **For example spotlights** showing the correct actual-vs-projection format, see `references/account-spotlight-format.md`.

### Section 8 - Recommendations and Next-Quarter Focus

Tiered action list (always include these categories):
1. POC to Milestone conversion (e.g., active POC account close to production — create the MSX milestone)
2. Post-meeting to Opportunity creation (e.g., informal architecture session with no MSX opp yet)
3. Demo to advance (e.g., account with strong AI signal but no committed action after last meeting)
4. EA Milestone close — check due dates for committed milestones expiring this quarter
5. Milestone hygiene — count stale milestones; flag as URGENT if >80% are stale
6. Top weighted gap account — priority call derived from DUAL-MISS analysis (use msx-perf-analyzer output if available, otherwise derive from MSX milestone gaps directly)

---

## ACR and Claim Validation Workflow

Use when user asks to verify a specific ACR or milestone claim.

Ask user: "Please provide the account name you want to validate and the path to your workspace folder with the MSX CSV exports."

Python validation snippet (replace `TARGET_ACCOUNT` with the actual account name):
```python
import csv, io

workspace_path = r'[USER_PROVIDED_PATH]'
accounts_csv = '[PerformanceSummary_AccountReport_YYYY_NNN.csv]'

with open(f'{workspace_path}\\{accounts_csv}',
          newline='', encoding='utf-8-sig') as f:
    content = f.read()

lines = [l for l in content.splitlines() if not l.startswith('sep=')]
reader = csv.DictReader(io.StringIO('\n'.join(lines)))
rows = [{k.strip(): v.strip() for k,v in r.items()} for r in reader]

account_filter = 'TARGET_ACCOUNT'  # e.g., 'City of Springfield' or 'County of Anytown'
account_rows = [r for r in rows if account_filter.upper() in r.get('Account Name','').upper()]
for r in account_rows:
    print(r.get('Account Name') + ' | ' + r.get('Metric Name') + ' | ' +
          r.get('Credit Month') + ' | Actuals=' + r.get('Total Actuals') +
          ' | Quota=' + r.get('Total Quota'))
```

Run via: `$env:PYTHONIOENCODING = "utf-8"; python -c "...inline script..."`

Validation table:
| Claim type | Source of truth | Correction pattern |
|------------|----------------|-------------------|
| "$X/mo ACR" | CSV Total Actuals column | Avg of Jan+Feb (Mar is partial) |
| "$X committed" | MSX milestone Est. Monthly Use | Correct but qualify as Q-next projection |
| "Growing account" | CSV Q2 vs Q3 actuals | Compare quarter averages |
| "$X Consumed Recurring" | MSX opportunity field | Total opportunity lifetime, not monthly |

---

## Output Generation

### Primary: HTML File (always use - never fails)

Ask user: "Where should I save the HTML report? (provide full folder path, or press Enter to use the current directory)"

Use `$OUTPUT_PATH` as the resolved output folder.

```powershell
$env:PYTHONIOENCODING = "utf-8"

# Set output filename
$quarter = "$FISCAL_QUARTER"      # e.g., "Q3"
$fy = "$FISCAL_YEAR"              # e.g., "FY26"
$alias = "$SELLER_ALIAS"          # e.g., "jsmith"
$version = "v1"
$outputPath = "$OUTPUT_PATH\$quarter-$fy-Leadership-Update-$alias-$version.html"

# Write HTML
$html | Out-File -FilePath $outputPath -Encoding UTF8

# Verify
$size = (Get-Item $outputPath).Length / 1KB
Write-Host "Saved: $outputPath ($([math]::Round($size, 1)) KB)"

# Auto-open in browser for copy-paste
Invoke-Item $outputPath
Write-Host "Opened in browser. Use Ctrl+A → Ctrl+C → paste into Outlook."
```

File opens in browser immediately. User can Ctrl+A, Ctrl+C and paste into Outlook or Word.

### Secondary: Outlook Draft (attempt after HTML, may fail)

```
Tool: WorkIQ-Mail-MCP-Server-CreateDraftMessage
Parameters:
  to: ["$SELLER_EMAIL"]  (always send to self first for review)
  subject: "$FISCAL_QUARTER $FISCAL_YEAR Territory Insights — Leadership Update | $SEGMENT | $SELLER_NAME"
  contentType: "HTML"
  body: [full HTML content]
```

Known issue: WorkIQ-Mail-MCP-Server returns AADSTS900144 auth error when M365 OAuth token expires.
Workaround: Use HTML file fallback. Retry mail after 5-10 minutes. Never block on mail auth failure.

---

## Key Accounts Quick Reference

This table is built dynamically at runtime from MSX `get_account_team` data (Step 1) and WorkIQ findings.

| Account | State | AI Theme | MSX Opp | Stage | Priority |
|---------|-------|----------|---------|-------|----------|
| [Populated from $ACCOUNTS_LIST] | | | | | |

To pre-populate this table for your territory, see `references/account-spotlight-format.md` for the format guide, and create your own `my-accounts.md` file in the skill's folder following the template in `references/ai-foundry-accounts.md`.

---

## Decision Framework

| User request | Actions |
|-------------|---------|
| "Full quarterly update" | Step 0 setup gate → Step 1 auto-detect → Run all 4 MCP pulls in parallel + 2 WorkIQ queries → generate all 8 sections + HTML output |
| "What are customers saying about AI?" | WorkIQ AI query only → Section 4 expanded |
| "Which accounts should I call?" | MSX DUAL-MISS analysis (from milestones + pipeline) → Section 7 spotlights; suggest msx-perf-analyzer for quota-weighted call sheet |
| "Validate this ACR claim for [account]" | Ask for workspace path → Python CSV query → compare to MSX milestones → provide corrected statement |
| "Add [account] to the AI section" | WorkIQ query for that account AI discussions → expand Section 4 |
| "Update the email draft" | Ask for output path → Regenerate HTML → open in browser → user copies |
| "Who am I?" / "What's my territory?" | Run the Step 0 setup check and Step 1 auto-detection, then display results |

---

## Error Handling

### WorkIQ Mail Auth Failure (AADSTS900144)
Cause: M365 OAuth token expired mid-session
Fix: Generate HTML file instead; retry mail 5-10 min later; use workiq-ask_work_iq as stub fallback

### CSV KeyError or encoding issue
Cause: sep= header row or UTF-8 BOM in MSX export files
Fix:
```python
lines = [l for l in content.splitlines() if not l.startswith('sep=')]
rows = [{k.strip('\ufeff').strip(): v for k,v in r.items()} for r in reader]
```

### MSX "No opportunities found" for an account
Cause: Account name ambiguity (multiple orgs match)
Fix: Use `tpid` parameter instead of `account_name` for exact matching
Get TPID: run `msx-mcp-search_accounts(account_name="[partial name]")` to find the TPID
Example: `msx-mcp-get_account_opportunities(tpid=1234567)` for exact match

### msx_analyze.py "file not found"
Cause: This skill does not call msx_analyze.py directly. Inline ACR validation uses the Python snippet in the ACR Validation section, which only requires a workspace folder path.
Fix: Provide your workspace folder path when prompted. If you want the full scorecard script, run the optional `msx-perf-analyzer` skill separately.

### WorkIQ returns no results for an account
Cause: Account name doesn't match how it appears in your M365 emails/calendar
Fix: Try alternate name formats:
- Short name: `"Springfield"` instead of `"City of Springfield"`
- With state prefix: `"IL-City of Springfield"`
- Topic-first: `"cloud migration meeting"` instead of account-first queries

### Step 1 auto-detection returns wrong identity
Cause: Multiple MSX profiles or shared machine
Fix: User provides corrections directly in response to the confirmation prompt
     All downstream queries use the corrected values from that point forward

---

## Limitations

CAN:
- Auto-detect SE identity, segment, and account list from MSX + M365
- Pull live MSX pipeline, milestones, and SE activities via MCP
- Surface customer emails, Teams messages, and meeting transcripts via WorkIQ
- Validate ACR claims against CSV performance data (when user provides path)
- Generate HTML report (always works, no auth dependency)
- Draft Outlook email when M365 auth is active

CANNOT:
- Push to SharePoint or OneDrive directly (auth issues in current session pattern)
- Log new SE activities (use se-activity skill)
- Access M365 Copilot data (Business Solutions quota)
- Get real-time ACR from Azure portal (use CSV export from MSX instead)
- Access MSX accounts the invoking user is not on the account team for

---

## References

- `references/account-spotlight-format.md` — Format guide for Section 7 account spotlights (ACR actual vs projection pattern)
- `references/html-template.md` — HTML email template for leadership updates
- `references/ai-foundry-accounts.md` — Template for documenting account AI engagements (Content Understanding, Voice Agent, Translation patterns)
- `msx-perf-analyzer` skill — **Optional complement** for detailed quota scorecard with dual-miss prioritization tables
