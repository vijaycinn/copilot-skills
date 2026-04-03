---
name: msx-territory-signal
description: Analyzes Microsoft MSX territory performance data to generate per-SSP outreach signal briefs as formatted Outlook email drafts. Use this skill when a Microsoft field SE wants to identify which accounts to prioritize for Apps, AI, Azure Core/Infra, Data, or GitHub Copilot conversations based on consumption trends — and draft actionable outreach emails their SSP partners can run with. Invoke immediately when the user shares MSX performance CSV files (from Earning tab Account Report), account alignment spreadsheets, or asks about territory attainment, SSP outreach, account prioritization, consumption gaps, GitHub Copilot seats, ACR trends, or which customers to call this quarter. Also invoke for "territory signal", "who should I call", "draft SSP emails", "Q3 attainment analysis", or any variation of wanting to turn MSX data into outreach actions.
---

# MSX Territory Signal

Analyzes MSX performance data to surface account-level signals and draft outreach emails for SSP partners. The skill identifies three tiers of accounts — chatter-highlighted (active engagement), momentum (high attainment, layer in next workload), and untapped prospects (strong Azure, no AI activation) — and generates one HTML email per SSP, ready to review and send from Outlook.

## Step 0: Confirm Setup, Dependencies, and File Paths First

Before doing any analysis, **always pause and ask the user for setup details**. Do not assume Vijay's file paths or territory defaults for a new seller.

**Start with this question:**

> "Do you already have your MSX performance export and your account-to-seller mapping file locally? If yes, send me the folder path or the two exact file paths. If the account data does not already include territory / ATU, tell me which territory IDs to scope to before I analyze anything. If not, I’ll show you where to get the files first."

### Required runtime inputs to confirm up front

1. **Performance CSV path** — the MSX export to analyze
2. **Account mapping file path** — XLSX or CSV with account → territory → SSP / AE / DSE alignment
3. **Solution area / bucket** — e.g. `AI Platform & Apps`, `Total ACR`, or `Data & AI`
4. **Territory IDs** — e.g. `0807 0808 0909 0910 0911`
5. **SSP aliases/names** — if not clearly inferable from the mapping file
6. **Chatter accounts** — optional list of accounts the user already knows are active

### If the user does NOT have the files yet, tell them exactly where to get them

1. **Account mapping / seller roster file**  
   Pull this from the **Seller Success Dashboard** → relevant **Sales Team** tab for the territory. This is the preferred source for SSP / AE / DSE mapping for a new SE or a different territory:  
   `https://msxinsights.microsoft.com/User/report/058a8810-081f-4e06-b43b-60d3b983ae3e?reportTab=ReportSection410832002b044d169c9a&bookmark=d1ccaaa51a0d446b5a07`

2. **Performance data CSV**  
   Export from **MSX → Earnings → Performance Summary → Account Report**. The user should export the current FY view (or at least the current quarter plus prior-year same-quarter months for YoY comparison).

3. **Optional Product Details CSV**  
   If the user wants deeper metric weighting or product-level inspection, also export **MSX Earnings → Product Details**.

### Environment dependencies that can vary by user environment

- **MSX MCP access** — optional but recommended for opportunity / milestone context
- **WorkIQ MCP access + EULA** — needed for email / Teams chatter narratives
- **Corporate network / VPN** — often required for MSX and WorkIQ to work reliably
- **Python 3.8+ on PATH** — required for the local CSV/XLSX analysis script
- **Windows + Excel installed** or **mapping file exported as CSV** — needed when the alignment file is an XLSX that requires Excel automation
- **WorkIQ Mail / Outlook draft permissions** — needed only if the user wants drafts created automatically

If any of the above are missing, **call it out before processing starts** and tell the user what fallback exists (for example: live analysis only, or export the mapping file as CSV instead of XLSX).

### Territory-first guardrail

Do **not** analyze all accounts first and only later try to narrow to a seller's patch.

Always:

1. confirm the territory IDs up front if they are not already present in the files
2. filter the account mapping file to the approved territory set immediately
3. only then rank the accounts inside that territory

For Vijay's default motion, use **`0807`, `0808`, `0909`, `0910`, `0911`** unless the user corrects the list.

## What You Need

### Required Files

1. **MSX Performance CSV** — from MSX Earning tab → Performance Summary → Account Report export
   - See `references/data-preparation.md` for exact export steps
   - Key columns: `Account Name`, `TPID`, `Metric Name`, `Bucket Name`, `Credit Month`, `Actuals`, `Total Quota`, `Fiscal Year`

2. **Account Alignment File** — XLSX or CSV mapping accounts → territories → SSP aliases
   - See `references/data-preparation.md` for the column structure and how to get it
   - On Windows, XLSX files from MSX require Excel COM automation (not openpyxl) — use `scripts/read_account_xlsx.py`

### Optional Enrichment (strongly recommended)

- **WorkIQ MCP** (`ask_work_iq`): Pull recent email/Teams engagement signals for chatter-highlighted accounts
- **MSX MCP** (`get_account_opportunities`, `get_opportunity_details`): Pull open pipeline, EA renewal dates, deal team membership

## Configuration

Confirm these parameters at the start (infer from file contents if the user doesn't specify, but always give the user a chance to correct them first):

| Parameter | Example | Notes |
|---|---|---|
| **Solution Area / Bucket** | `AI Platform & Apps` | Match to `Bucket Name` in CSV. For Infra SEs: `Total ACR`. For Data SEs: `Data & AI` |
| **Territory IDs** | `0807, 0808, 0909, 0910, 0911` | From MSX territory hierarchy. Filter account alignment file to these |
| **Fiscal Quarter** | Q3 FY26 (Jan–Mar 2026) | Auto-detect from most recent months in the CSV — see quarter mapping below |
| **SSP List** | Kassie, MIA, Orlando | Names/aliases as they appear in account alignment file |
| **Chatter Accounts** | Fort Worth, Galveston, Sacramento | Accounts mentioned from recent Teams/email context |

**Quarter mapping (FY26):**
- Q1: Jul–Sep 2025 | Q2: Oct–Dec 2025 | Q3: Jan–Mar 2026 | Q4: Apr–Jun 2026

## Analysis Workflow

### Step 1: Read the Files

Use `scripts/analyze_territory.py` to process both files and produce `ssp_account_analysis.json`:

```bash
python scripts/analyze_territory.py \
  --csv "path/to/PerformanceSummary.csv" \
  --xlsx "path/to/AccountAlignment.xlsx" \
  --bucket "AI Platform & Apps" \
  --territories 0807 0808 0909 0910 0911 \
  --output ssp_account_analysis.json
```

The script outputs per-account metrics including **metric breakdown** — critical for correct narrative framing. An account at 1841% attainment driven by `Azure Build Apps & Modernize Apps` only is a very different signal from one driven by `Azure AI`. Always surface what's actually running.

### Step 2: Query WorkIQ for Chatter Accounts

For each account the user flagged from recent conversations, query:

```
ask_work_iq: "What are recent customer conversations, emails, or Teams messages about [Account Name]? 
What workloads are they discussing — AI, GitHub Copilot, Apps modernization?"
```

This produces the engagement narrative for the ★ Chatter-Highlighted section. Ground every claim in actual signal, not inference.

### Step 3: Query MSX for Pipeline Context

For chatter accounts and top momentum accounts, check:
- Open opportunities (`get_account_opportunities`)
- EA renewal dates (look in opportunity details for `estimatedclosedate`)
- Whether you're on the deal team (shows ownership and co-sell angle)

### Step 3B: Optional Sales Home / MSXi ACR growth signal

If the `sales-home` MCP is available, use it only for the already-scoped territory accounts to identify **which accounts are growing in Apps or AI ACR**.

**Best fields to use:**

- `Account Last Month ACR`
- `Account MOM $`
- `Account MOM %`
- `Strategic Pillar`
- `ServiceHierarchy[WorkLoadName]`

**Recommended output columns for each ranked account:**

`Account | TPID | Territory | Bucket | Top workload | Current ACR | Prior ACR | Delta $ | Delta % | Suggested next call`

This turns the skill into a seller-ready “who should my SSP / AE call next?” view instead of a raw export summary.

### Step 4: Categorize Accounts per SSP

For each SSP, build three tiers using the `ssp_account_analysis.json` output:

| Tier | Criteria | Cap |
|---|---|---|
| ★ Chatter-Highlighted | User-flagged from recent conversations | All of them |
| 🚀 Active AI Momentum | `ai_attain_pct > 80%` AND `ai_actuals > 0` | Top 5–8 by attainment |
| 🎯 Untapped Potential | `ai_actuals == 0` AND (`acr_yoy_pct > 20%` OR high absolute ACR) | Top 4–6 by ACR growth |

**For momentum accounts:** look at `metric_breakdown` to suggest the natural *next* workload:
- Only `Azure Build Apps & Modernize Apps` active → suggest GitHub Copilot or Azure AI
- Only `Azure AI` active → suggest GitHub Copilot for dev teams, or Foundry expansion
- Only `GitHub Copilot` active → suggest Azure AI Foundry use cases

### Step 5: Draft Emails

One email per SSP. Full HTML template in `references/email-format.md`.

**Framing rules (from lessons learned):**
- ✅ Use % only — AI Attainment %, ACR YoY %
- ❌ No dollar amounts, no quota figures, no gap columns
- Frame as "who to call and why" — outreach signal, not performance review
- Chatter accounts get WorkIQ-grounded engagement narratives (be specific, cite the actual use case)
- Momentum accounts get "next workload" suggestions based on `metric_breakdown`
- Untapped accounts get "first conversation" angles (what's the door-opener for this account type?)

### Step 6: Post to Outlook as Drafts

Use `WorkIQ-Mail-MCP-Server-CreateDraftMessage` with:
- `contentType: "HTML"`
- `body`: **raw HTML with actual `<` `>` characters** — do NOT pre-encode as `&lt;`/`&gt;` (this causes double-encoding and renders as literal tag text in the email)
- For special characters in content text: use numeric HTML entities (`&#8212;` for —, `&#128202;` for 📊, `&amp;` for & in text strings, `&#9733;` for ★)
- Subject format: `Apps & AI Outreach Opportunities | Q3 FY26 Territory Signal (<territories>)`

Confirm rendering: the API response `bodyPreview` should show readable text like "📊 Apps & AI Outreach..." — if it shows `&lt;html&gt;` the encoding is wrong.

## Output

- N Outlook drafts (one per SSP), properly formatted HTML
- Each email: 3-section structure with color-coded section headers, tabular account data, engagement narrative
- Old broken drafts (if any exist from prior runs) should be deleted from Drafts folder

## Reference Files

- `references/data-preparation.md` — How to export files from MSX + column structure for account alignment XLSX
- `references/email-format.md` — Full HTML email template with CSS
- `scripts/analyze_territory.py` — Full analysis pipeline (CSV + XLSX → JSON)
- `scripts/read_account_xlsx.py` — Windows Excel COM reader for account alignment XLSX
