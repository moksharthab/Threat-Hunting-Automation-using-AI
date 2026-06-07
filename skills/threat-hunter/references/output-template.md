# Threat Hunter Output Template

Use this section order when returning results.

If the user requests a PDF report, preserve this exact section order and content model. Render the final report to PDF when a local PDF toolchain is available. Do not write a Markdown source file unless the user explicitly requests one. If PDF generation is blocked and the user did not ask for Markdown, report the blocker instead of creating an unrequested Markdown deliverable.

## 1. Report Summary

Include:

- Report title
- Source or publisher
- Threat actor or campaign
- Target industries
- Target regions
- Malware, tooling, infrastructure, or notable procedures

## 2. ATT&CK Extraction

Use this table:

```markdown
| Technique Name | ATT&CK ID | Tactic | Source | Confidence | ATT&CK Link |
|----------------|-----------|--------|--------|------------|-------------|
```

Rules:

- Use `Source = Explicit` when the article names the technique or provides an ATT&CK mapping table.
- Use `Source = Inferred` when the technique is derived from the procedure text.
- Use `Source = Generalized hunt hypothesis` when the technique extends coverage beyond the article but remains operationally relevant.

## 3. Detection Data Sources

Use the required telemetry table from [secops-log-types.md](./secops-log-types.md).

## 4. Chronicle YARAL Hunts

Default behavior:

- Write 2-3 generic, reusable hunts per extracted TTP.
- Make each hunt for a given TTP materially distinct, ideally by telemetry source, event focus, or analytic strategy.
- If only 2 strong hunts are supportable for a TTP, return 2 and briefly note why a third would be low-confidence.
- Do not make source-specific IOCs part of the hunt logic.
- Group the hunts into `High-Fidelity`, `Medium-Fidelity`, and `Needs Validation`.

For each hunt under a TTP, provide:

1. Technique ID and technique name
2. Hunt name
3. Fidelity
4. Best primary log source
5. Secondary log sources if useful
6. Goal of the hunt
7. Known or assumed event types and fields
8. False-positive or tuning notes
9. Gaps or validation notes
10. YARAL query block

Use this style:

```text
// ATT&CK T1059.001 - PowerShell - WINEVTLOG
// Draft - validate fields and event types if needed

$e.metadata.log_type = "WINEVTLOG"
...

condition:
$e
```

If a query is not fully grounded, label it `Draft - validate fields and event types`.

After the hunt blocks, include this prioritization table. Multiple rows per TTP are expected because each TTP should have 2-3 hunts:

```markdown
| TTP | Hunt Name | Fidelity | Why It Belongs Here | Best Primary Log Source |
|-----|-----------|----------|---------------------|-------------------------|
```

## 5. Defensive Playbook

Structure the playbook with these sections:

- `Detection Goal`
- `Blind Spots`
- `False Positives`
- `Investigation Steps`
- `Recommended Follow-up Hunts`

Rules:

- Keep the playbook tied to what the telemetry can actually observe.
- Make investigation steps sequential and practical.
- Use the follow-up hunt section to capture the broader, holistic search ideas that extend beyond the source article.
- When the user primarily wants hunts, keep the playbook concise and focus on false positives, tuning guidance, and triage value.
- In PDF mode, do not replace tables with prose or collapse hunt metadata fields; keep the report operational and presentation-ready.
