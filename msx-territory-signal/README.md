# msx-territory-signal

> **Copilot CLI Skill** | Microsoft field SE territory outreach

Turns MSX performance exports into **actionable SSP outreach signals**. The skill ranks accounts by chatter, momentum, and untapped potential, then drafts HTML emails your SSP can use for Apps, AI, Infra, Data, or GitHub follow-up.

---

## What it does

1. Prompts for the **local file paths** or workspace folder for your exports
2. Explains where to get the files if you do not have them yet
3. Analyzes your MSX **Performance Summary / Account Report** export
4. Joins it with a **seller mapping file** to connect accounts to SSP / AE / DSE ownership
5. Produces per-SSP outreach recommendations and HTML-ready email content

---

## Required inputs

### 1. MSX performance export
Export from:

**MSX → Earnings → Performance Summary → Account Report**

Recommended: export the current fiscal year so the skill can compute current-quarter signals and year-over-year ACR context.

### 2. Seller mapping / account alignment file
Preferred source for new sellers or different territories:

**Seller Success Dashboard → relevant Sales Team tab**

`https://msxinsights.microsoft.com/User/report/058a8810-081f-4e06-b43b-60d3b983ae3e?reportTab=ReportSection410832002b044d169c9a&bookmark=d1ccaaa51a0d446b5a07`

This export should include, where available:
- account / customer name
- TPID
- territory / sales territory
- SSP / DSS ownership
- AE / DAE ownership
- DSE / CE / CSA ownership

---

## Environment dependencies

The skill now calls these out before processing starts:

- **Python 3.8+**
- **MSX MCP** access for opportunity / milestone context
- **WorkIQ MCP** for email and Teams grounding
- **Corporate VPN / network** if required
- **Excel on Windows** for some XLSX exports, or a CSV version of the seller-mapping file
- **Outlook / Mail permissions** if you want drafts created automatically

If those dependencies are missing, the skill falls back to local-file analysis or HTML-only output where possible.

---

## Quick start

Invoke the skill naturally in Copilot CLI:

```text
I need SSP outreach signals for my Apps and AI territory
```

or

```text
Which accounts should my SSP call this quarter based on my MSX performance data?
```

The skill will ask whether you already have the local files. If not, it will walk you to the right MSX and Seller Success Dashboard exports first.

---

## Files in this skill

```text
msx-territory-signal/
├── README.md
├── SKILL.md
├── references/
│   ├── data-preparation.md
│   └── email-format.md
├── scripts/
│   ├── analyze_territory.py
│   └── read_account_xlsx.py
└── evals/
    └── evals.json
```

---

## Notes

- `analyze_territory.py` now handles MSX CSV `sep=` headers and more robust XLSX reading on Windows.
- If the account mapping workbook is problematic, export it as CSV from Excel and point the skill to that file instead.
