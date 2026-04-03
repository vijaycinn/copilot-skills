"""
MSX Territory Signal Analyzer

Reads MSX Performance Summary CSV + Account Alignment XLSX and produces
per-SSP account metrics for outreach email generation.

Usage:
    python analyze_territory.py \
        --csv path/to/PerformanceSummary.csv \
        --xlsx path/to/AccountAlignment.xlsx \
        --bucket "AI Platform & Apps" \
        --territories 0807 0808 0909 0910 0911 \
        --output ssp_account_analysis.json

    # For Infra SEs:
    python analyze_territory.py --bucket "Total ACR" ...

    # If XLSX already converted to CSV:
    python analyze_territory.py --account-csv path/to/accounts.csv ...
"""

import argparse
import csv
import io
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Quarter definitions (Microsoft FY)
# ---------------------------------------------------------------------------

FY_QUARTER_MAP = {
    "Q1": ["July", "August", "September"],
    "Q2": ["October", "November", "December"],
    "Q3": ["January", "February", "March"],
    "Q4": ["April", "May", "June"],
}


def detect_quarter_from_months(months_present: List[str]) -> Tuple[str, int]:
    """
    Detect the most recent quarter and fiscal year from the months in the CSV.
    Returns (quarter_name, calendar_year) e.g. ("Q3", 2026).
    """
    # Parse "January, 2026" → (month_name, year)
    parsed = []
    for m in months_present:
        parts = m.split(",")
        if len(parts) == 2:
            parsed.append((parts[0].strip(), int(parts[1].strip())))

    if not parsed:
        raise ValueError("Could not detect quarter from Credit Month values in CSV")

    # Find the latest year
    max_year = max(y for _, y in parsed)
    latest_months = {m for m, y in parsed if y == max_year}

    for q_name, q_months in FY_QUARTER_MAP.items():
        if latest_months & set(q_months):
            return q_name, max_year

    raise ValueError(f"Could not map months {latest_months} to a fiscal quarter")


def get_quarter_months(quarter: str, year: int) -> List[str]:
    """Return full month strings for a quarter, e.g. ['January, 2026', ...]"""
    month_names = FY_QUARTER_MAP[quarter]
    # Q3 months are Jan/Feb/Mar of the calendar year matching the FY end
    return [f"{m}, {year}" for m in month_names]


def get_prior_year_months(quarter_months: List[str]) -> List[str]:
    """Same months but one year earlier, for YoY comparison."""
    result = []
    for m in quarter_months:
        parts = m.split(",")
        result.append(f"{parts[0].strip()}, {int(parts[1].strip()) - 1}")
    return result


# ---------------------------------------------------------------------------
# CSV loading
# ---------------------------------------------------------------------------

def load_csv_rows(path: str) -> List[Dict]:
    """
    Load CSV rows while handling MSX exports that prepend a `sep=,` header line.
    """
    with open(path, encoding="utf-8-sig", newline="") as f:
        content = f.read()

    lines = [
        line for line in content.splitlines()
        if line.strip() and not line.lower().startswith("sep=")
    ]
    reader = csv.DictReader(io.StringIO("\n".join(lines)))

    rows = []
    for row in reader:
        cleaned = {
            (k or "").strip(): v.strip() if isinstance(v, str) else v
            for k, v in row.items()
        }
        if any(cleaned.values()):
            rows.append(cleaned)
    return rows


def load_performance_csv(path: str) -> List[Dict]:
    return load_csv_rows(path)


def load_account_csv(path: str) -> List[Dict]:
    """Load account alignment data from a plain CSV (fallback if no XLSX)."""
    return load_csv_rows(path)


# ---------------------------------------------------------------------------
# XLSX loading via Excel COM (Windows only)
# ---------------------------------------------------------------------------

def _cell_to_text(value) -> str:
    return "" if value is None else str(value).strip()


def _matrix_to_rows(matrix) -> List[Dict]:
    """Convert Excel UsedRange.Value / Value2 output into a list of row dicts."""
    if matrix is None:
        return []

    if not isinstance(matrix, tuple):
        matrix = ((matrix,),)
    elif matrix and not isinstance(matrix[0], tuple):
        matrix = (matrix,)

    if not matrix:
        return []

    headers = []
    for idx, value in enumerate(matrix[0], start=1):
        header = _cell_to_text(value) or f"Col{idx}"
        headers.append(header)

    rows = []
    for raw_row in matrix[1:]:
        row = {}
        has_value = False
        for idx, header in enumerate(headers):
            value = raw_row[idx] if idx < len(raw_row) else ""
            text = _cell_to_text(value)
            row[header] = text
            if text:
                has_value = True
        if has_value:
            rows.append(row)
    return rows


def load_account_xlsx_via_powershell(path: str) -> List[Dict]:
    """
    Fallback reader that uses PowerShell + Excel COM when pywin32 is unavailable.
    This keeps the skill usable out-of-the-box on managed Windows machines.
    """
    ps_script = r"""
$WorkbookPath = $env:MSX_WORKBOOK_PATH
$ErrorActionPreference = 'Stop'
$excel = $null
$workbook = $null
$sheet = $null
$usedRange = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $workbook = $excel.Workbooks.Open($WorkbookPath, $false, $true)
    $sheet = $workbook.Sheets.Item(1)
    $values = $sheet.UsedRange.Value2

    if ($null -eq $values) {
        '[]'
        exit 0
    }

    if ($values -isnot [System.Array]) {
        $values = @(@($values))
    }
    elseif ($values.Rank -eq 1) {
        $values = ,$values
    }

    $rowCount = $values.GetLength(0)
    $colCount = $values.GetLength(1)

    $headers = @()
    for ($c = 1; $c -le $colCount; $c++) {
        $header = $values[1, $c]
        if ($null -eq $header -or [string]::IsNullOrWhiteSpace([string]$header)) {
            $headers += "Col$c"
        } else {
            $headers += ([string]$header).Trim()
        }
    }

    $rows = New-Object System.Collections.Generic.List[object]
    for ($r = 2; $r -le $rowCount; $r++) {
        $row = [ordered]@{}
        $hasValue = $false
        for ($c = 1; $c -le $colCount; $c++) {
            $value = $values[$r, $c]
            $text = if ($null -eq $value) { '' } else { ([string]$value).Trim() }
            $row[$headers[$c - 1]] = $text
            if (-not [string]::IsNullOrWhiteSpace($text)) {
                $hasValue = $true
            }
        }
        if ($hasValue) {
            $rows.Add([pscustomobject]$row)
        }
    }

    $rows | ConvertTo-Json -Depth 4 -Compress
}
finally {
    if ($workbook -ne $null) { $workbook.Close($false) }
    if ($excel -ne $null) { $excel.Quit() }
    foreach ($comObject in @($usedRange, $sheet, $workbook, $excel)) {
        if ($comObject -ne $null -and [System.Runtime.InteropServices.Marshal]::IsComObject($comObject)) {
            [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($comObject)
        }
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
"""

    completed = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            ps_script,
        ],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "MSX_WORKBOOK_PATH": path},
    )

    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "Unknown PowerShell error"
        print(
            "ERROR: Could not read the account alignment workbook via Excel automation.\n"
            f"Details: {message}\n"
            "If Excel is unavailable on this machine, export the workbook as CSV and re-run with --account-csv.",
            file=sys.stderr,
        )
        sys.exit(1)

    payload = completed.stdout.strip() or "[]"
    rows = json.loads(payload)
    if isinstance(rows, dict):
        rows = [rows]
    return rows


def load_account_xlsx(path: str) -> List[Dict]:
    """
    Read XLSX via Excel COM automation. Required for MSX-exported XLSX files
    that openpyxl/pandas cannot parse due to format quirks.
    Only works on Windows with Excel installed.
    """
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        print(f"ERROR: File not found: {abs_path}", file=sys.stderr)
        sys.exit(1)

    try:
        import win32com.client
    except ImportError:
        return load_account_xlsx_via_powershell(abs_path)

    excel = None
    workbook = None
    try:
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(abs_path, False, True)
        sheet = workbook.Sheets(1)
        used = sheet.UsedRange
        return _matrix_to_rows(used.Value)
    finally:
        if workbook is not None:
            try:
                workbook.Close(SaveChanges=False)
            except Exception:
                pass
        if excel is not None:
            try:
                excel.Quit()
            except Exception:
                pass


def parse_float(value) -> float:
    """Best-effort numeric parsing for MSX exports."""
    if value in (None, ""):
        return 0.0
    text = str(value).strip().replace(",", "")
    if text in {"-", "--"}:
        return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


# ---------------------------------------------------------------------------
# Account alignment parsing
# ---------------------------------------------------------------------------

def normalize_name(name: str) -> str:
    """Normalize account names for fuzzy matching."""
    return re.sub(r"[^a-z0-9 ]", "", name.lower()).strip()


def extract_territory_code(raw_territory: str) -> str:
    """
    Normalize territory values like `0808` or `Industry.SMECC.USPS.0808` to the
    4-digit territory code used in the skill prompts.
    """
    text = (raw_territory or "").strip()
    matches = re.findall(r"(\d{4})", text)
    return matches[-1] if matches else text


def build_account_map(account_rows: List[Dict], territories: List[str]) -> Dict[str, Dict]:
    """
    Build a map of TPID → account metadata, filtering to the target territories.
    Tries to auto-detect the territory and SSP columns.
    """
    if not account_rows:
        return {}

    headers = list(account_rows[0].keys())

    # Auto-detect territory column
    territory_col = next(
        (h for h in headers if "territory" in h.lower() and "id" in h.lower()), None
    ) or next((h for h in headers if "territory" in h.lower()), None)

    # Auto-detect TPID column
    tpid_col = next((h for h in headers if "tpid" in h.lower()), None)

    # Auto-detect account name column
    name_col = next(
        (h for h in headers if "account name" in h.lower() or "account" in h.lower()), None
    )
    if not name_col:
        name_col = next((h for h in headers if "customer name" in h.lower()), None)

    # Auto-detect SSP columns (look for DSS, SSP, CSA keywords)
    ssp_cols = [h for h in headers if any(kw in h.lower() for kw in ["dss", "ssp", "csa", "stu"])]

    account_map: Dict[str, Dict] = {}  # keyed by TPID or normalized name
    name_to_tpid: Dict[str, str] = {}

    for row in account_rows:
        territory = row.get(territory_col, "").strip() if territory_col else ""
        territory_code = extract_territory_code(territory)
        tpid = str(row.get(tpid_col, "")).strip() if tpid_col else ""
        name = row.get(name_col, "").strip() if name_col else ""

        # Filter to target territories, supporting both raw 4-digit codes and
        # strings like `Industry.SMECC.USPS.0808`.
        terr_code = territory_code.lstrip("0") if territory_code else ""
        match = any(
            t.lstrip("0") == terr_code
            or t == territory
            or t == territory_code
            for t in territories
        )
        if territories and not match:
            continue

        ssp_data = {col: row.get(col, "").strip() for col in ssp_cols}

        entry = {
            "account_name": name,
            "tpid": tpid,
            "territory": territory_code or territory,
            "ssp": ssp_data,
            "normalized_name": normalize_name(name),
        }

        key = tpid if tpid else normalize_name(name)
        account_map[key] = entry
        if name:
            name_to_tpid[normalize_name(name)] = key

    return account_map


def find_account_in_map(account_name: str, tpid: str, account_map: Dict) -> Optional[Dict]:
    """Try TPID first, then normalized name match."""
    if tpid and tpid in account_map:
        return account_map[tpid]
    norm = normalize_name(account_name)
    if norm in account_map:
        return account_map[norm]
    # Partial match fallback
    for key, entry in account_map.items():
        if entry.get("normalized_name") and norm in entry["normalized_name"]:
            return entry
    return None


# ---------------------------------------------------------------------------
# Metric computation
# ---------------------------------------------------------------------------

def compute_metrics(
    rows: List[Dict],
    bucket: str,
    q3_months: List[str],
    prior_months: List[str],
    account_map: Dict,
) -> List[Dict]:
    """
    Aggregate per-account metrics from the performance CSV.
    Returns list of account dicts with computed attainment, YoY, and breakdown.
    """
    # Aggregate raw values
    data: Dict[str, Dict] = defaultdict(lambda: {
        "ai_actuals": 0.0,
        "ai_quota": 0.0,
        "acr_q3": 0.0,
        "acr_prior": 0.0,
        "metric_breakdown": defaultdict(float),
        "tpid": "",
        "account_name": "",
    })

    for row in rows:
        acct_name = row.get("Account Name", "").strip()
        tpid = str(row.get("TPID", "")).strip()
        metric = row.get("Metric Name", "").strip()
        bkt = row.get("Bucket Name", "").strip()
        month = row.get("Credit Month", "").strip()
        actuals = parse_float(row.get("Actuals", 0))
        quota = parse_float(row.get("Total Quota", 0))

        key = tpid if tpid else normalize_name(acct_name)
        data[key]["account_name"] = acct_name
        data[key]["tpid"] = tpid

        # Target bucket — Q3
        if bkt == bucket and month in q3_months:
            data[key]["ai_actuals"] += actuals
            data[key]["ai_quota"] += quota
            data[key]["metric_breakdown"][metric] += actuals

        # Total ACR — Q3 (for untapped detection even when bucket != Total ACR)
        if bkt == "Total ACR" and month in q3_months:
            data[key]["acr_q3"] += actuals

        # Total ACR — prior year Q3 (for YoY)
        if bkt == "Total ACR" and month in prior_months:
            data[key]["acr_prior"] += actuals

    # Build result list
    results = []
    for key, d in data.items():
        ai_quota = d["ai_quota"]
        prior_acr = d["acr_prior"]
        q3_acr = d["acr_q3"]

        attain_pct = round(d["ai_actuals"] / ai_quota * 100, 1) if ai_quota > 0 else 0.0
        yoy_pct = round((q3_acr - prior_acr) / prior_acr * 100, 1) if prior_acr > 0 else None

        # Lookup alignment data
        align = find_account_in_map(d["account_name"], d["tpid"], account_map)

        results.append({
            "account_name": d["account_name"],
            "tpid": d["tpid"],
            "territory": align["territory"] if align else "",
            "ssp": align["ssp"] if align else {},
            "ai_actuals": round(d["ai_actuals"], 2),
            "ai_quota": round(ai_quota, 2),
            "ai_attain_pct": attain_pct,
            "ai_gap": round(d["ai_actuals"] - ai_quota, 2),
            "acr_q3": round(q3_acr, 2),
            "acr_yoy_pct": yoy_pct,
            "metric_breakdown": {
                k: round(v, 2) for k, v in d["metric_breakdown"].items() if v > 0
            },
        })

    # Sort by AI attainment descending
    results.sort(key=lambda x: x["ai_attain_pct"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="MSX Territory Signal Analyzer")
    parser.add_argument("--csv", required=True, help="Path to MSX Performance Summary CSV")
    parser.add_argument("--xlsx", help="Path to Account Alignment XLSX (Windows + Excel required)")
    parser.add_argument("--account-csv", help="Path to Account Alignment CSV (alternative to --xlsx)")
    parser.add_argument(
        "--bucket",
        default="AI Platform & Apps",
        help='MSX bucket name (default: "AI Platform & Apps")',
    )
    parser.add_argument(
        "--territories",
        nargs="+",
        default=[],
        help="Territory IDs to filter to (e.g., 0807 0808 0909)",
    )
    parser.add_argument("--output", default="ssp_account_analysis.json", help="Output JSON path")
    args = parser.parse_args()

    # Load performance data
    print(f"Loading performance CSV: {args.csv}")
    perf_rows = load_performance_csv(args.csv)
    print(f"  {len(perf_rows)} rows loaded")

    # Detect quarter
    all_months = list({r.get("Credit Month", "").strip() for r in perf_rows if r.get("Credit Month")})
    quarter, year = detect_quarter_from_months(all_months)
    q3_months = get_quarter_months(quarter, year)
    prior_months = get_prior_year_months(q3_months)
    print(f"  Detected quarter: {quarter} FY{year} — months: {q3_months}")

    # Load account alignment
    account_rows = []
    if args.xlsx:
        print(f"Loading account alignment XLSX: {args.xlsx}")
        account_rows = load_account_xlsx(args.xlsx)
    elif args.account_csv:
        print(f"Loading account alignment CSV: {args.account_csv}")
        account_rows = load_account_csv(args.account_csv)
    else:
        print("WARNING: No account alignment file provided. Territory/SSP fields will be empty.")

    account_map = build_account_map(account_rows, args.territories)
    print(f"  {len(account_map)} accounts in alignment map (territories: {args.territories})")

    # Compute metrics
    print(f"Computing metrics for bucket: {args.bucket}")
    results = compute_metrics(perf_rows, args.bucket, q3_months, prior_months, account_map)

    # Filter to aligned territories if we have alignment data
    if account_map and args.territories:
        results = [r for r in results if r["territory"]]
        print(f"  {len(results)} accounts after territory filter")

    # Output
    output = {
        "quarter": quarter,
        "fiscal_year": year,
        "bucket": args.bucket,
        "territories": args.territories,
        "q3_months": q3_months,
        "accounts": results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\nOutput written to: {args.output}")
    print(f"Total accounts: {len(results)}")
    print(f"  With AI actuals > 0: {sum(1 for r in results if r['ai_actuals'] > 0)}")
    print(f"  With AI actuals = 0: {sum(1 for r in results if r['ai_actuals'] == 0)}")


if __name__ == "__main__":
    main()
