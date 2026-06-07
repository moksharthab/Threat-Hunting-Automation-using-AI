---
name: ttp-ioc-hunter
description: Build Chronicle YARAL detections and defensive playbooks from threat intelligence reports for Google SecOps / Google Chronicle, and deliver the result as a PDF report. Use when given a threat report, vendor blog, intrusion writeup, or campaign summary and asked to extract TTPs, map them to MITRE ATT&CK, find Atomic Red Team coverage, identify relevant Google SecOps log types and data sources, or draft YARAL detections grounded in known telemetry.
---

# TTP IOC Hunter

Convert threat intelligence into structured defensive outputs for Google SecOps. Extract campaign details and attacker behaviors, map them to MITRE ATT&CK, identify detection opportunities from the available telemetry, and write YARAL only when the fields and event types are reasonably supportable.

The final deliverable for this skill is a PDF report, not a Markdown file. Keep the same report structure defined below, render it to PDF, and return the absolute PDF path to the user.

## PDF output mode

- If the user asks for a PDF report, keep the exact same section order and hunt content as the default output.
- First generate the full report content in Markdown internally using the required tables and hunt blocks.
- Then render that Markdown to a PDF file when a local PDF-capable toolchain is available.
- Use [`scripts/render_report_pdf.py`](scripts/render_report_pdf.py) first. It accepts Markdown from stdin or a file path and avoids leaving a `.md` artifact behind.
- Prefer a local renderer already present in the environment, such as `reportlab`, `pandoc`, or another installed Markdown-to-PDF workflow supported by the renderer script.
- If no PDF renderer is available, say so clearly and do not create a Markdown file unless the user explicitly asked for one.
- By default, do not write a Markdown source file when the user only asked for a PDF or report output. Only save Markdown when the user explicitly requests a Markdown deliverable.
- In either case, tell the user where the requested output file or files were written.

## Follow this workflow

1. Read the full report.
   Capture the report title, publisher, threat actor or campaign name, target industries, target regions, malware families, infrastructure, and notable procedures.
2. Prefer explicit ATT&CK mappings first.
   If the article includes an ATT&CK table, extract technique IDs, names, and tactics directly before inferring anything.
3. Extract additional TTPs from prose using NLP-style reasoning.
   Focus on verbs, objects, tools, APIs, command lines, protocols, execution chains, persistence actions, credential access steps, lateral movement paths, collection actions, and exfiltration methods.
4. Map each behavior to MITRE ATT&CK.
   Prefer the most specific supported sub-technique. Add a confidence rating for inferred mappings.
5. Look for Atomic Red Team coverage.
   Link to the relevant technique or atomic folder if coverage exists.
6. Map each technique to detection data sources.
   Use only the available `metadata.log_type` values and note gaps explicitly. Read [`references/google_secops_log_types.md`](references/google_secops_log_types.md) before recommending log sources.
7. Draft YARAL detections.
   Build queries only where the telemetry and fields are defensible. If an event type or field is unknown, say so instead of guessing.
8. Produce a structured defensive playbook.
   Summarize the actor, behaviors, ATT&CK coverage, detections, gaps, and recommended next steps.
9. Render the finished report to PDF.
   Use [`scripts/render_report_pdf.py`](scripts/render_report_pdf.py) and provide the user with the absolute output path. Do not leave a `.md` report artifact behind unless the user explicitly asked for Markdown too.

## Extract TTPs from the report

Extract these report-level fields when available:

- Report title
- Source or publisher
- Threat actor or campaign name
- Target industries
- Target regions
- Malware, tools, or infrastructure
- Directly referenced ATT&CK IDs in `Txxxx` or `Txxxx.xxx` form

When the report does not provide a complete ATT&CK table, infer TTPs from the described procedures.

Use this confidence model for inferred mappings:

- High: The technique is explicitly named, or the procedure is described with concrete tool, API, or command detail.
- Medium: The behavior clearly aligns to a technique even without a direct ATT&CK mention.
- Low: The behavior is general and could map to multiple techniques.

Keep explicit ATT&CK mappings separate from inferred ones.

## Map to MITRE ATT&CK carefully

- Map behavior, not vague intent.
- Prefer a sub-technique when the evidence supports it.
- Fall back to the parent technique when the procedure is too broad.
- Include the ATT&CK technique name and the exact ATT&CK technique URL.
- Lead with the primary technique and mention secondary techniques only when they materially improve analyst understanding.
- Mark uncertain mappings clearly.

## Look for Atomic Red Team coverage

For each ATT&CK technique or sub-technique, check for coverage under:

- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team/tree/master/atomics)

Provide the most relevant technique-level or sub-technique-level Atomic Red Team link when available. If no atomic coverage is obvious, say `No confirmed atomic test found`.

## Use only these Google SecOps log types

Read [`references/google_secops_log_types.md`](references/google_secops_log_types.md) and use that exact allowlist when recommending detection data sources or writing YARAL filters against `metadata.log_type`.

If a technique requires telemetry outside this allowlist, call out the gap instead of inventing a supported source.

## Map techniques to detection data sources

For each technique, determine which of the available log types are most suitable for detection. Favor telemetry that captures the action directly rather than indirect side effects.

Use this output table:

```markdown
| Technique Name | TTP ID | TTP Subtechnique ID | List of Log Types Needed to detect this technique |
|---------------|--------|---------------------|---------------------------------------------------|
| Kerberoasting | T1558 | T1558.003 | WINEVTLOG, ELASTIC_WINLOGBEAT |
```

When a parent technique is used without a specific sub-technique, leave the sub-technique column empty or use `N/A`.

## Write Chronicle YARAL cautiously

Use only field names, `metadata.log_type` values, and event types you are reasonably confident exist. Do not fabricate `metadata.product_event_type`, `EventCode`, or deep UDM field names.

When the report suggests a detection idea but the exact event type is unknown:

- Say which log type is likely relevant.
- Say which event type or field must be confirmed.
- Avoid presenting a speculative query as production-ready.

When you do write YARAL:

- Include a short comment header with the ATT&CK ID, technique name, and log source.
- Scope the rule to the relevant `metadata.log_type`.
- Use technique-specific indicators grounded in known behavior.
- Add exclusions only when there is a defensible baseline reason.
- Prefer readable, single-purpose detections over overly broad correlation logic.

Use examples like these patterns when appropriate:

- `T1003.001`: suspicious access to `lsass.exe`, including known access masks or target image matches
- `T1053.005`: scheduled task creation via `schtasks.exe`, `at.exe`, or equivalent task scheduler artifacts
- `T1059.001`: PowerShell execution indicators in command line or script content
- `T1021.002`: SMB-driven lateral movement patterns

## Use this YARAL response format

For each detection candidate, provide:

1. Technique ID and technique name
2. Goal of the detection
3. Required log types
4. Known or assumed event types and fields
5. Gaps or validation notes
6. YARAL query block

If the query is only partially grounded, label it as `Draft - validate fields and event types`.

## Use this overall output structure

Use this section order when returning results.

If the user requests a PDF report, preserve this exact section order and content model. Render the final report to PDF when a local PDF toolchain is available. Do not write a Markdown source file unless the user explicitly requests one. If PDF generation is blocked and the user did not ask for Markdown, report the blocker instead of creating an unrequested Markdown deliverable.

Use this structure inside the PDF report.

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
```

Rules:

- Use `Source = Explicit` when the article names the technique or provides an ATT&CK mapping table.
- Use `Source = Inferred` when the technique is derived from the procedure text.

## 3. Atomic Red Team coverage

Use a table with these columns:

```markdown
| Technique Name | ATT&CK ID | Atomic Red Team Link | Coverage Notes |
```

## 4. Detection data sources

Use the required log type table exactly as defined earlier.

## 5. Chronicle YARAL detections

Include only detections that are grounded in the available telemetry. Separate production-ready detections from partial drafts.
Use query format like $e.target.process.file.full_path = /lsass\.exe$/. Dont append i like in this query/condition - $e.target.process.file.full_path = /lsass\.exe$/i


Use this style:

```text
// ATT&CK T1059.001 - PowerShell - WINEVTLOG
// Draft - validate fields and event types if needed

$e.metadata.log_type = "WINEVTLOG"
$e.target.process.file.full_path = /lsass\.exe$/
...

condition:
  $e
```

If a query is not fully grounded, label it `Draft - validate fields and event types`.

## 6. Defensive playbook

Include:

- Detection opportunities
- Validation steps
- Known telemetry gaps
- Prioritization guidance
- Suggested follow-on hunts

## Produce PDF output

- Extract all the data and findings into a downloadable PDF report.

## Quality rules

- Do not claim ATT&CK mappings without evidence.
- Do not invent Chronicle event types or fields.
- Do not recommend unsupported log types.
- Prefer saying `unknown` or `needs validation` over guessing.
- Preserve direct evidence from the report before summarizing.
- Keep explicit mappings and inferred mappings visibly distinct.
- The durable output must be a PDF report, not a Markdown file.
- When a PDF is requested, render the same content without collapsing sections, dropping tables, or shortening hunt metadata just to fit the file format.
