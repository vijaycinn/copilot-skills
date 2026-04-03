# Data Preparation Guide

How to get the two required input files from MSX, and what their column structures look like.

---

## File 1: MSX Performance Summary CSV

### How to Export

1. Go to **MSX** → **Earning** tab (top navigation)
2. Select **Performance Summary** → **Account Report**
3. Filter by:
   - **Fiscal Year**: current FY (e.g., FY26)
   - **Solution Area / Bucket**: your area (see bucket names below)
   - **Territory**: your ATU territories (e.g., 0807, 0808, 0909, 0910, 0911)
4. Set date range to cover the full fiscal year (or at minimum the current quarter + same quarter prior year for YoY)
5. Click **Export to CSV**

> **Note:** Export the full fiscal year, not just the current quarter. The analysis script needs prior-year months to compute ACR YoY.

### Bucket Names by Solution Area

| Role | Bucket Name in CSV |
|---|---|
| Apps & AI SE | `AI Platform & Apps` |
| Azure Core / Infra SE | `Total ACR` |
| Data SE | `Data & AI` |
| GitHub SE | look for `Developer Platform & GitHub Copilot` metric within `AI Platform & Apps` |

### Column Structure

| Column | Description |
|---|---|
| `Account Name` | Customer account name (Top Parent) |
| `TPID` | Top Parent ID — unique account identifier in MSX |
| `Metric Name` | Specific metric (e.g., `Azure AI`, `Azure Build Apps & Modernize Apps`, `Developer Platform & GitHub Copilot`, `ACR - Core`) |
| `Bucket Name` | Solution area bucket (e.g., `AI Platform & Apps`, `Total ACR`) |
| `Credit Month` | Format: `January, 2026` |
| `Fiscal Year` | e.g., `2026` |
| `Actuals` | Current period actuals (USD) |
| `Total Actuals` | May differ from Actuals when adjustments apply — use `Actuals` for quota attainment |
| `Total Quota` | Quota for this account/metric/month |
| `Unit` | Usually `USD` |

### Metric Breakdown within "AI Platform & Apps"

Understanding what's driving attainment is important — these are the key metrics within the bucket:

| Metric Name | What It Means |
|---|---|
| `Azure AI` | Azure OpenAI, AI Search, Cognitive Services consumption |
| `Azure Build Apps & Modernize Apps` | App Service, Container Apps, AKS, API Management, Service Bus |
| `Developer Platform & GitHub Copilot` | GitHub Copilot, GitHub Advanced Security seat consumption |
| `Azure Data & Analytics` | Fabric, Synapse, ADX (sometimes in this bucket) |

> **Important:** An account at 1841% attainment with all actuals in `Azure Build Apps & Modernize Apps` and zero `Azure AI` is a **Build Apps customer** — not an AI breakout. Always check the metric breakdown before writing the narrative.

---

## File 2: Account Alignment XLSX / CSV

### What This File Is

A spreadsheet mapping each account (by name or TPID) to:
- Territory ID (e.g., `0807`, `0909`)
- SSP alias/name for each solution area role
- often **AE / DSE / CE / CSA** ownership as well

This file is typically maintained by your ATU or STU admin. In Vijay's territory, this is `Account Sales Team ACR.xlsx`.

> **Territory-first rule:** this file should include a territory / ATU field. If it does not, the skill should stop and ask the user which territory IDs to scope to before any account analysis begins.

### How to Get It

**Preferred source for a new SE or a different territory:**

1. Open the **Seller Success Dashboard** and go to the relevant **Sales Team** tab for your business / territory:  
   `https://msxinsights.microsoft.com/User/report/058a8810-081f-4e06-b43b-60d3b983ae3e?reportTab=ReportSection410832002b044d169c9a&bookmark=d1ccaaa51a0d446b5a07`
2. Filter to your segment / territory
3. Export the sales team roster so you have the account mapping for **SSP, AE, DSE, CE**, and related sellers

Fallback options:
1. **ATU Admin / STU lead**: request the current account-to-seller alignment workbook
2. **MSX Account Management**: export from the MSX account team page if available in your view
3. **Manual**: build a CSV from your own territory knowledge (TPID, Account Name, Territory, SSP / AE / DSE aliases)

### Column Structure (Vijay's File Example)

| Column Name | Example | Notes |
|---|---|---|
| `Account Name` | `TX-CITY OF FORT WORTH` | May need normalization to match CSV |
| `TPID` | `670570` | Use for joining when names don't match exactly |
| `ATU Group` | `USA.SC.SLG.TX-01` | Territory hierarchy |
| `Territory ID` | `0807` | The 4-digit territory number |
| `Primary Cloud & AI DSS` | `KASSIECRUTE` or `OWALKERII` | SSP alias for Apps/AI DSS role |
| `Primary Cloud & AI-Acq DSS` | `MIA` | SSP alias for acquisition DSS role |
| `Primary DAE` | `SIRITHORSTAD` | AE / DAE ownership |
| `Primary CE` | `NICOLEPIERCE, JRUMORE, AMDEVI` | CE team / specialist ownership |

> **For other SEs:** Column names may differ by dashboard export or segment. Look for headers containing `DSS`, `SSP`, `AE`, `DAE`, `DSE`, `CE`, `CSA`, or segment-specific role labels.

If the export does not include a clear territory field, fix that first or tell the skill the explicit territory IDs up front. Do **not** run a broad all-account analysis and narrow later.

### Reading XLSX on Windows

Standard Python libraries (openpyxl, pandas) often fail on MSX-exported XLSX files due to format quirks. Use Excel COM automation via `scripts/read_account_xlsx.py`:

```python
# The script uses win32com.client to open the file in Excel and read values
python scripts/read_account_xlsx.py --path "Account Sales Team ACR.xlsx" --output account_alignment.json
```

This requires Windows + Excel installed. If on Mac/Linux, ask the user to re-save as CSV from Excel first, then use standard CSV reading.

---

## Joining the Two Files

The analysis script joins on either `TPID` (preferred, exact) or `Account Name` (fuzzy — normalize to uppercase and strip punctuation). TPID is more reliable since account names vary between MSX exports.

After joining, filter to the target territories and group by SSP column to produce the per-SSP account lists.
