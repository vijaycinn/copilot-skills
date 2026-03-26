# HTML Export Template

Full HTML template for the territory leadership update export.
Save as `[QUARTER]-[FY]-Leadership-Update-[ALIAS]-v[N].html` in your chosen output folder.

Ask user for output path before writing. Default to current working directory if not provided.

---

## Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Q[N] FY[YY] Territory Leadership Update</title>
<style>
  body { font-family: Calibri, Arial, sans-serif; font-size: 14px; color: #1a1a1a; 
         max-width: 960px; margin: 40px auto; padding: 0 24px; }
  h1 { color: #0078D4; border-bottom: 3px solid #0078D4; padding-bottom: 10px; }
  h2 { color: #0078D4; border-left: 5px solid #0078D4; padding-left: 12px; margin-top: 32px; }
  h3 { color: #005a9e; margin-top: 20px; }
  table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 13px; }
  th { background: #0078D4; color: white; padding: 10px; text-align: left; }
  td { padding: 8px 10px; border: 1px solid #ccc; }
  tr:nth-child(even) { background: #f0f6ff; }
  .callout { border-left: 4px solid #0078D4; padding: 12px 16px; background: #f0f6ff; 
             font-style: italic; margin: 16px 0; color: #333; }
  .correction { background: #fff3cd; border: 1px solid #ffc107; 
                padding: 10px; border-radius: 4px; margin: 8px 0; }
  .urgent { background: #ffe0e0; border: 1px solid #f44336; 
            padding: 10px; border-radius: 4px; }
  .tag { display: inline-block; background: #0078D4; color: white; 
         padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-left: 6px; }
  .tag-yellow { background: #ff8c00; }
  .tag-green { background: #107c10; }
  hr { border: none; border-top: 1px solid #ddd; margin: 28px 0; }
  ul li { margin-bottom: 6px; }
  .footer { font-size: 11px; color: #888; margin-top: 40px; 
            padding-top: 12px; border-top: 1px solid #ddd; }
</style>
</head>
<body>

<h1>Q[N] FY[YY] Territory Insights — Leadership Update</h1>
<p><strong>[SELLER_NAME]</strong> | [SELLER_ROLE], [SEGMENT] | 
Territories: [TERRITORY_CODES]<br>
<em>v[N] — [brief description of what changed] — [Month Year]</em></p>
<hr>

<!-- SECTION 1: SE Activity Snapshot -->
<h2>📊 SE Activity Snapshot — Q[N] FY[YY]</h2>
[CONTENT]
<hr>

<!-- SECTION 2: GitHub Copilot -->
<h2>🐙 GitHub Copilot (Code) — Customer Insights</h2>
[CONTENT]
<hr>

<!-- SECTION 3: App Dev -->
<h2>🏗️ App Dev Modernization — Customer Insights</h2>
[CONTENT]
<hr>

<!-- SECTION 4: Azure AI/Foundry — MOST IMPORTANT FOR LEADERSHIP -->
<h2>🤖 Azure AI &amp; Foundry — Q[N] FY[YY] Engagement Highlights</h2>
<p><strong>Territory-Wide Theme: [THEME]</strong></p>
[CONTENT]
<hr>

<!-- SECTION 5: Competitive Intelligence -->
<h2>⚔️ Competitive Intelligence — Q[N] FY[YY]</h2>
[CONTENT]
<hr>

<!-- SECTION 6: Macro Themes -->
<h2>🌐 Macro / Industry Themes</h2>
[CONTENT]
<hr>

<!-- SECTION 7: Account Spotlights -->
<h2>🏆 Account Spotlights</h2>
[CONTENT]
<hr>

<!-- SECTION 8: Recommendations -->
<h2>✅ Recommendations &amp; Q[N+1] Focus Areas</h2>
[CONTENT]

<div class="footer">
Generated via GitHub Copilot CLI + MSX MCP + WorkIQ MCP | 
Data: MSX attainment CSV, account performance CSV, MSX pipeline API, 
customer emails/meetings (WorkIQ M365 Copilot) | 
Q[N] FY[YY] data through [Date] | v[N]
</div>
</body>
</html>
```

---

## PowerShell Export Command

```powershell
$env:PYTHONIOENCODING = "utf-8"

# Populated from Step 0 auto-detection + user-provided output path
$quarter   = "[FISCAL_QUARTER]"   # e.g., "Q3"
$fy        = "[FISCAL_YEAR]"      # e.g., "FY26"
$alias     = "[SELLER_ALIAS]"     # e.g., "jsmith"
$version   = "v1"
$outputDir = "[OUTPUT_PATH]"      # user-provided or cwd

$outputPath = "$outputDir\$quarter-$fy-Leadership-Update-$alias-$version.html"

# Write HTML
$html | Out-File -FilePath $outputPath -Encoding UTF8

# Verify
$size = (Get-Item $outputPath).Length / 1KB
Write-Host "Saved: $outputPath ($([math]::Round($size, 1)) KB)"

# Auto-open in browser for copy-paste
Invoke-Item $outputPath
Write-Host "Opened in browser. Use Ctrl+A → Ctrl+C → paste into Outlook."
```

---

## Outlook Draft Command (when auth is working)

```
WorkIQ-Mail-MCP-Server-CreateDraftMessage(
  to: ["[SELLER_EMAIL]"],
  subject: "Q[N] FY[YY] Territory Insights — Leadership Update | [SEGMENT] | [SELLER_NAME]",
  body: <html_content_string>,
  contentType: "HTML"
)
```

**If auth fails (AADSTS900144):** Use HTML file only. Inform user to open file, Ctrl+A, Ctrl+C, paste into Outlook New Email.
