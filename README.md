# copilot-skills

A collection of [GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli) agent skills for Microsoft field engineers. Each skill orchestrates MCP servers (MSX, WorkIQ, Azure tools) to automate common SE workflows — pipeline analysis, territory reporting, activity logging, and more.

---

## Available Skills

| Skill | Description | Audience |
|-------|-------------|----------|
| [`territory-insights`](./territory-insights/) | Generates a fully-grounded quarterly territory leadership update using live MSX pipeline, milestones, HoK activities, and WorkIQ customer emails/meetings. Outputs an 8-section HTML report ready to paste into Outlook. | Field SEs / DSEs |
| [`msx-territory-signal`](./msx-territory-signal/) | Generates SSP-ready outreach signal briefs from MSX performance exports plus seller-mapping files. Identifies chatter, momentum, and untapped accounts and can draft HTML outreach emails for Apps, AI, Infra, Data, or GitHub motions. | Field SEs / DSEs |
| [`se-activity`](./se-activity/) | Drafts and classifies MSX SE Activity entries from meeting notes, emails, or Teams conversations. Maps work to the correct FY26 SE Task Category and MSX scope (Account / Opportunity / Milestone). | Field SEs / DSEs |

_More skills coming. PRs welcome._

---

## Prerequisites

All skills in this repo require:

| Requirement | Notes |
|-------------|-------|
| [GitHub Copilot CLI](https://github.com/github/gh-copilot) | `gh extension install github/gh-copilot` |
| MSX MCP Server | Microsoft internal — contact your CSA/DSE lead for setup |
| WorkIQ MCP Server | Microsoft internal — connects to Microsoft 365 Copilot |
| Python 3.8+ | For inline CSV analysis (ACR validation) |

> **Microsoft-internal only:** These skills use MSX (Microsoft Sales Experience) and WorkIQ (M365 Copilot) MCP servers that are only available inside the Microsoft corporate network. They are not usable externally.

---

## Installation

1. **Clone or download this repo**

   ```bash
   git clone https://github.com/vijaycinn/copilot-skills.git
   ```

2. **Copy the skill(s) you want to `~/.copilot/skills/`**

   ```powershell
   # Windows
   Copy-Item -Recurse .\territory-insights "$env:USERPROFILE\.copilot\skills\territory-insights"
   ```

   ```bash
   # macOS / Linux
   cp -r territory-insights ~/.copilot/skills/
   ```

3. **Verify the skill is loaded**

   Open a new Copilot CLI session and type `skills` — you should see `territory-insights` listed.

4. **Invoke the skill**

   ```
   territory-insights
   ```

   The skill auto-detects your identity and territory from MSX/M365. No config required for the first run.

---

## Personalizing a Skill (Optional)

Each skill supports a personal config file that you can create locally and will never be committed (it's in `.gitignore`):

| File | Purpose |
|------|---------|
| `my-config.md` | Your territory config: name, email, segment, ATU codes, workspace path |
| `my-accounts.md` | Your account engagement notes (use `references/ai-foundry-accounts.md` as template) |

To create your personal config:

1. Copy the template from each skill's README into a `my-config.md` file in the skill folder
2. Fill in your name, email, segment, ATU codes, and workspace path
3. Reference it when the skill prompts for corrections in Step 0

> `my-config.md` and `my-accounts.md` are in `.gitignore` — your personal config will never be committed.

---

## Repo Structure

```
copilot-skills/
├── README.md                          ← you are here
├── msx-territory-signal/
│   ├── README.md                      ← quick start + data prep guidance
│   ├── SKILL.md                       ← skill definition (read by Copilot CLI)
│   ├── references/
│   │   ├── data-preparation.md        ← where to export performance + seller mapping files
│   │   └── email-format.md            ← HTML outreach email template
│   ├── scripts/
│   │   ├── analyze_territory.py       ← CSV/XLSX → SSP account analysis JSON
│   │   └── read_account_xlsx.py       ← Excel automation helper for account mapping
│   └── evals/
│       └── evals.json                 ← example prompts / expected outcomes
├── territory-insights/
│   ├── README.md                      ← quick start + install
│   ├── SKILL.md                       ← skill definition (read by Copilot CLI)
│   ├── territory_insights_instructions.md  ← full user guide
│   ├── .gitignore
│   └── references/
│       ├── account-spotlight-format.md    ← Section 7 format guide
│       ├── html-template.md               ← HTML output template
│       └── ai-foundry-accounts.md         ← blank account engagement template
└── se-activity/
    ├── README.md                      ← quick start + install
    ├── SKILL.md                       ← skill definition (read by Copilot CLI)
    └── .gitignore
```

---

## Contributing

1. Fork this repo
2. Add your skill as a new directory under `skills/`
3. Include a `SKILL.md` (the Copilot CLI skill definition) and a `README.md`
4. Submit a PR with a description of what the skill does and what MCP tools it requires

Skill naming convention: `kebab-case`, verb-noun preferred (e.g., `log-activity`, `validate-acr`).

---

## License

MIT — see [LICENSE](../LICENSE) for details.

> Skills connect to Microsoft-internal services. The skill code itself is MIT-licensed; the MCP server connections require internal Microsoft access.
