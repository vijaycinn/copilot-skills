# Account Spotlight Format Guide

Use this format when writing Section 7 Account Spotlights in the territory leadership update.

---

## Required Elements Per Spotlight

Every account spotlight must include:

1. **Account Name + Classification** (e.g., "DUAL-MISS", "AI Leader", "ACR Outperformer")
2. **Actual `$FISCAL_QUARTER` ACR** — from CSV, labeled clearly as actual consumption
3. **MSX Milestone pipeline** — labeled clearly as projections/forward estimates for `$NEXT_QUARTER`
4. **Primary contact** (if available from WorkIQ)
5. **`$NEXT_QUARTER` priority action** — specific, actionable, one sentence

---

## Format Template

```markdown
### [Account Name] — [Classification Tag]

**Actual $FISCAL_QUARTER ACR (from performance CSV):** ~$X,XXX/month average
| Metric | [Month1] | [Month2] | [Month3]* | $FISCAL_QUARTER Avg |
|--------|----------|----------|-----------|---------------------|
| ACR - Core | $X | $X | $X | $X |
| Build/Modernize | $X | $X | $X | $X |
| GitHub Copilot | $X | $X | $X | $X |
| **Total** | **$X** | **$X** | **$X** | **$X** |
*[Month3] = partial month

**MSX Milestone Pipeline ($NEXT_QUARTER $FISCAL_YEAR projections — NOT current consumption):**
- [Milestone 1]: $X,XXX/mo | [Committed/Uncommitted] | Due [Month Year]
- [Milestone 2]: $X,XXX/mo | [Committed/Uncommitted] | Due [Month Year]
- **Total committed: $X,XXX/mo** | **Total upside: $X,XXX/mo**

**Key contacts:** [Names from WorkIQ if available]

**$NEXT_QUARTER action:** [One specific, actionable next step]
```

> **Month names:** Use the actual calendar months for `$FISCAL_QUARTER`. Reference the quarter-months table in `SKILL.md` (Q1=Jul/Aug/Sep, Q2=Oct/Nov/Dec, Q3=Jan/Feb/Mar, Q4=Apr/May/Jun).

---

## Classification Tags

| Tag | Criteria |
|-----|----------|
| DUAL-MISS ⭐ | AI gap >$500 AND ACR gap >$5,000 — every dollar counts in 2 buckets |
| AI Outperformer 🟢 | AI Platform attainment ≥100% |
| ACR Outperformer 🟢 | ACR attainment ≥100% all Q3 months |
| At Risk ⚠️ | Either bucket <75% attainment with large gap |
| New Logo Q3 | $0 in Q2, >$500 actuals in Q3 |
| Retention Risk | Q2 AI >$10K, dropped >20% in Q3 |
| Milestone-Heavy 📋 | Large MSX milestone pipeline vs. actual consumption |

---

## ACR Validation Checklist

Before publishing any account spotlight, verify:
- [ ] `$FISCAL_QUARTER` ACR figures pulled directly from `PerformanceSummary_AccountReport*.csv`
- [ ] MSX milestone numbers pulled from `msx-mcp-get_opportunity_details`
- [ ] The two figures are clearly labeled separately (actual vs. projection)
- [ ] "Consumed Recurring" MSX field is NOT used as a monthly consumption figure
- [ ] Final month of the quarter is labeled as partial month with asterisk

---

## Example: Good vs. Bad Spotlight

### ❌ Bad (conflates actual + projection)
> "Acme County has $15,000/mo in ACR for the CJS App Platform engagement."

**Why it's wrong:** $15K was derived from MSX milestones (projections). Actual Q3 FY26 ACR is ~$9,900/mo.

### ✅ Good (clearly separates actual vs. projection)
> "Acme County: actual Q3 FY26 ACR averages ~$9,900/mo (ACR-Core dominant at $7,082/mo). MSX committed milestones project $16,000/mo when realized in Q4 FY26 (App Platform $10K + App Scale $3K + App Sec $3K, all due May 2026), with total milestone upside of $26,000/mo including uncommitted Sentinel + Apps & AI."

> **Note:** The example above illustrates the correct pattern — clearly separate actual consumption figures from MSX milestone projections. Apply the same structure with your own `$FISCAL_QUARTER` and `$NEXT_QUARTER` values.
