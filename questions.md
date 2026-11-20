# Init questions

**Upgrade mode:** skip every question already answered in `docs/standards/profile.md` (or in the rebuilt profile); ask only for missing, changed or open dimensions, then confirm the whole profile once. The rounds and "always asked" rules below apply to first runs.

Ask with the AskUserQuestion tool in **two rounds**. The tool allows at most 4 questions per call, 2 to 4 options per question and a header of at most 12 characters; it adds an "Other" free-text option automatically. Keep within those limits so no option is silently dropped. If the tool is not available, ask the same questions as a short numbered list in one message.
Skip a question whose answer was detected with clear evidence; that value is shown on the confirmation screen instead. Mark the suggested option by adding "(Recommended)" to its label and listing it first.

## Round 1 · always asked (4 questions)

### Q1 · Stage (D1) · header "Stage"
"What stage is this project aiming for in the next few months?"
- MVP: real users soon, solid but lean (Recommended)
- Prototype: exploring an idea, may be thrown away
- Production: live or business-critical

### Q2 · Data (D5) · header "Data"
"What data will it store or process?"
- None: no stored data
- Stored, but no personal data
- Personal data (names, emails, accounts, IPs...)
- Special-category data (health, biometrics, religion...) or children's data

Never infer this answer; "Other" answers are mapped to the closest value and confirmed in Step 3.

### Q4 · Growth (D12, sets D6) · header "Growth"
"Where do you expect this project in 12–24 months?"
- Stays small: same scope, same people (sets scale=low)
- Grows within one team: more features and users (sets scale=moderate)
- Splits: several teams and/or services (sets scale=moderate)
- High scale: large or spiky traffic (sets scale=high)

### Q5 · Regulation (D9) · header "Regulation" · multi-select
"Which of these regulations apply? (Use Other for 'not sure' or anything not listed.)"
Show 4 options, chosen before asking:
1. None of these apply
2. GDPR (personal data of people in the EU)
3. and 4. the first two that fit, in this priority: EU AI Act (if ai!=none was detected) · European Accessibility Act (if web-ui was detected) · Cyber Resilience Act (if the software is distributed: CLI, library, installed product, app) · NIS2
"None of these apply" together with another option counts as that other option. Regulations not shown can be named in Other.
If the user is not sure about a regulation that was offered, leave it out of the profile, show it on the confirmation screen as "<name>: not sure (open)", and offer its practice as an opt-in suggestion with one line on how to decide. Record any other regulation named in Other (e.g. PCI DSS) as an open question.

## Round 2 · up to 4 questions, in this priority order

### Q7 · Context (D14, D17, D18) · header "Context" · multi-select, always asked
"Which of these apply?"
- None of these → shared=no, tenancy=single, platform=no
- Shares a database or infrastructure with other apps, clients or teams → shared=yes
- Serves several customers from one deployment (multi-tenant) → tenancy=multi
- A platform others build on (plugins, components, extension APIs) → platform=yes
Unselected options keep their defaults. "None of these" together with another option counts as that other option.

### Q10 · Hosting (D7) · header "Hosting" · only if deployment was not detected
"Where will it run for real users?"
- Only on my machine for now → local
- Managed platform (Streamlit Cloud, Heroku, Render, Vercel...) → paas
- Cloud infrastructure we run (AWS, Azure, GCP, Kubernetes...) → cloud
- Customers' or our own data centre → on-prem

### Q7b · Openness (D16) · header "Openness" · only if not detected (a missing licence file counts as detected closed)
"Will the source code be public?"
- No, closed source (Recommended unless an OSI licence was found)
- Yes, public (open source)
- Yes, and we accept outside contributions

### Q3 · Interfaces (D4) · header "Interfaces" · multi-select, only if not detected
"How will people or systems use it? (CLI or other: use Other.)"
- Web UI
- API used by our own apps
- Public API for third parties
- Events / messaging

### Q6 · Team (D2) · header "Team" · only if not detected
"Who will work on it?"
- Just me
- Small team (2 to 8)
- Several teams

### Q9 · Tracker (D15) · header "Tracker" · only if team>=small and not detected
"Where is the work tracked?"
- Jira
- GitHub Issues / Projects
- Azure Boards
- None

Round-2 priority: Q7, Q10, Q7b, Q3, Q6, Q9. If more than 4 remain, keep the first 4 in that order; use defaults for the rest and list them as open questions in the summary.

## Follow-up · Q8 · Releases (D11) · header "Releases" · conditional, one question
Ask only if deployment is `on-prem` or `regulated-env` (detected, or chosen in Q10) and the release model was not detected.
"How will releases reach users?"
- Continuously, whenever main is green
- On a schedule or after formal approval (release windows, CAB)
- Several versions supported in production at the same time

## Not asked (detected or recommended, shown on the confirmation screen)
- Repo (D13): detected, otherwise `single`.
- Architecture (D3): detected, otherwise "modular monolith (recommended, 04.1)".
- Deployment (D7): detected or from Q10.
- AI (D8): detected from dependencies, otherwise `none`.

## Confirmation screen (Step 3) · example values only

```
PROJECT PROFILE · please confirm or correct

| Dimension    | Value               | Source                          |
|--------------|---------------------|---------------------------------|
| Mode         | existing            | detected: 42 commits, src/      |
| Stack        | Python · Streamlit  | detected: pyproject.toml        |
| Stage        | MVP                 | your answer                     |
| Data         | personal            | your answer                     |
| Interfaces   | web-ui              | detected: streamlit dependency  |
| Horizon      | grows               | your answer                     |
| Scale        | moderate            | from horizon                    |
| Release      | continuous          | default                         |
| Repo         | single              | detected: no workspace files    |
| Regulation   | GDPR                | your answer                     |
| Team         | solo                | detected: 1 author in 90 days   |
| Tracker      | none                | detected: no issue keys         |
| Milestones   | M1 (current), M2-M3 | detected: CLAUDE.md roadmap     |
| Open         | AI Act: not sure    | your answer                     |
| Shared       | yes                 | your answer                     |
| Tenancy      | single              | your answer                     |
| Platform     | no                  | your answer                     |
| Openness     | closed              | default (no OSI licence found)  |
| Architecture | modular monolith    | recommended (04.1)              |
| Deployment   | paas                | your answer (Q10)               |
| AI           | uses-llm            | detected: anthropic dependency  |

This selects N of M practices across G groups.
Reply "ok" or name what to change.
```
