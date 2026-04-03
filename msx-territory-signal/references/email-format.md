# Email Format: HTML Template

Full HTML template for SSP outreach emails. Copy this structure and populate the sections.

---

## CSS (include in `<head>`)

```css
body {
  font-family: Segoe UI, Arial, sans-serif;
  font-size: 14px;
  color: #1a1a1a;
  max-width: 900px;
  margin: 0 auto;
}
h2 { color: #005a9e; border-bottom: 2px solid #005a9e; padding-bottom: 6px; }
h3 { color: #333; margin-top: 24px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0 20px; font-size: 13px; }
th { background: #005a9e; color: white; padding: 8px 10px; text-align: left; }
td { padding: 7px 10px; border-bottom: 1px solid #e0e0e0; vertical-align: top; }
tr:nth-child(even) { background: #f5f8fc; }
.up   { color: #2e7d32; font-weight: bold; }   /* green — positive trend */
.down { color: #c62828; }                        /* red — declining */
.flat { color: #555; }                           /* gray — neutral / zero */
.signal-box {
  background: #fffbf0;
  border-left: 4px solid #c8860a;
  padding: 10px 14px;
  margin: 14px 0;
  font-size: 13px;
}
```

---

## Section Header Colors

| Section | Background Color | Hex |
|---|---|---|
| ★ Chatter-Highlighted | Amber | `#c8860a` |
| 🚀 Active AI Momentum | Blue | `#1565c0` |
| 🎯 Untapped Potential | Green | `#2e7d32` |

---

## Full Template

```html
<html>
<head>
<meta charset="UTF-8">
<style>
body{font-family:Segoe UI,Arial,sans-serif;font-size:14px;color:#1a1a1a;max-width:900px;margin:0 auto}
h2{color:#005a9e;border-bottom:2px solid #005a9e;padding-bottom:6px}
h3{color:#333;margin-top:24px}
table{border-collapse:collapse;width:100%;margin:12px 0 20px;font-size:13px}
th{background:#005a9e;color:white;padding:8px 10px;text-align:left}
td{padding:7px 10px;border-bottom:1px solid #e0e0e0;vertical-align:top}
tr:nth-child(even){background:#f5f8fc}
.up{color:#2e7d32;font-weight:bold}
.down{color:#c62828}
.flat{color:#555}
.signal-box{background:#fffbf0;border-left:4px solid #c8860a;padding:10px 14px;margin:14px 0;font-size:13px}
</style>
</head>
<body>

<h2>&#128202; [SOLUTION_AREA] Outreach Opportunities &#8212; Your Territory [QUARTER] Signal</h2>

<p>Hi [SSP_NAME],</p>

<p>[1-2 sentence intro: what this is, which territories, what the goal is — surface accounts 
for [workload] conversations, either existing momentum to build on or untapped prospects.]</p>

<div class="signal-box">
  <strong>&#128273; [Territory theme or cross-account signal]:</strong> 
  [1-2 sentences on the dominant pattern or workload trend across the territory this quarter.]
</div>


<!-- ====================== SECTION 1: CHATTER ====================== -->

<h3>
  <span style="font-size:12px;font-weight:bold;color:white;padding:4px 12px;border-radius:3px;background:#c8860a">
    &#9733; Chatter-Highlighted Accounts
  </span> &#8212; Active Engagement, Go Deeper
</h3>

<table>
<tr>
  <th>Account</th>
  <th>Territory</th>
  <th>AI Q3 Attainment</th>
  <th>ACR YoY</th>
  <th>Workload Focus</th>
  <th>Engagement Signal</th>
</tr>
<tr>
  <td><strong>&#9733; [State-AccountName]</strong></td>
  <td>[TERR]</td>
  <td><span class="up">[X]%</span></td>      <!-- or .down or .flat -->
  <td><span class="up">+[Y]%</span></td>
  <td>[GitHub Copilot / Azure AI Foundry / etc.]</td>
  <td>[WorkIQ-grounded narrative: what's being discussed, specific use case, next step]</td>
</tr>
<!-- repeat for each chatter account -->
</table>


<!-- ====================== SECTION 2: MOMENTUM ====================== -->

<h3>
  <span style="font-size:12px;font-weight:bold;color:white;padding:4px 12px;border-radius:3px;background:#1565c0">
    &#128640; Active [Solution Area] Momentum
  </span> &#8212; High Attainment, Layer In Next Workload
</h3>

<table>
<tr>
  <th>Account</th>
  <th>Territory</th>
  <th>AI Q3 Attainment</th>
  <th>ACR YoY</th>
  <th>Suggested Next Motion</th>
</tr>
<tr>
  <td><strong>[State-AccountName]</strong></td>
  <td>[TERR]</td>
  <td><span class="up">[X]%</span></td>
  <td><span class="up">+[Y]%</span></td>
  <td>[What's currently active (metric_breakdown) + what to add next]</td>
</tr>
<!-- repeat -->
</table>


<!-- ====================== SECTION 3: UNTAPPED ====================== -->

<h3>
  <span style="font-size:12px;font-weight:bold;color:white;padding:4px 12px;border-radius:3px;background:#2e7d32">
    &#127919; Untapped Potential
  </span> &#8212; High Azure ACR, No [Solution Area] Activation Yet
</h3>

<p>Active Azure customers with zero [solution area] attainment &#8212; 
strong outreach candidates to start the conversation.</p>

<table>
<tr>
  <th>Account</th>
  <th>Territory</th>
  <th>AI Attainment</th>
  <th>ACR YoY</th>
  <th>Outreach Angle</th>
</tr>
<tr>
  <td><strong>[State-AccountName]</strong></td>
  <td>[TERR]</td>
  <td><span class="flat">0%</span></td>
  <td><span class="up">+[Y]%</span></td>
  <td>[Why this account, what's the door-opener, what sector/use case]</td>
</tr>
<!-- repeat -->
</table>

<p>Happy to support with [relevant offer: demo, architecture session, EA renewal briefing, 
GitHub Copilot workshop]. Just say the word.</p>

<p>&#8212; [SE_NAME]</p>

</body>
</html>
```

---

## Attainment Color Coding

Apply CSS classes to attainment and YoY values based on direction:

| Value | Class | Color |
|---|---|---|
| > 0% growth or > 80% attainment | `.up` | Green |
| Declining / negative YoY | `.down` | Red |
| 0% or flat / neutral | `.flat` | Gray |

---

## Special Character Reference

Use HTML numeric entities for special characters to avoid encoding issues:

| Character | Entity | Use |
|---|---|---|
| 📊 | `&#128202;` | Email heading icon |
| ★ | `&#9733;` | Chatter section marker |
| 🚀 | `&#128640;` | Momentum section |
| 🎯 | `&#127919;` | Untapped section |
| 🔑 | `&#128273;` | Signal box key icon |
| — | `&#8212;` | Em dash in text |
| & | `&amp;` | Ampersand in body text |

---

## Critical: Avoiding the Double-Encoding Bug

When passing HTML to `WorkIQ-Mail-MCP-Server-CreateDraftMessage`:

```python
# ✅ CORRECT — raw HTML with actual angle brackets
body = "<html><head>...</head><body><h2>Apps &amp; AI</h2></body></html>"

# ❌ WRONG — pre-encoded entities get double-encoded by the MCP tool
body = "&lt;html&gt;&lt;head&gt;...&lt;/head&gt;&lt;body&gt;"
# This renders as literal tag text in the email, not HTML
```

The MCP tool's `contentType: "HTML"` parameter handles the rendering — you just need to pass clean HTML.

Verify success: check `bodyPreview` in the API response — it should show readable text like `"📊 Apps & AI Outreach Opportunities — Your Territory..."` not `"&lt;html&gt;"`.
