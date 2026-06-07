---
name: threat-hunter
description: Build threat-hunt outputs for Google SecOps / Google Chronicle from threat intelligence reports, copied articles, vendor blogs, or campaign writeups. Use when Codex needs to extract TTPs with explicit plus NLP-inferred ATT&CK mapping, cross-reference strong public detection corpora, identify required Google SecOps log sources, and produce 2-3 distinct Chronicle hunts per extracted ATT&CK technique, grouped by fidelity and best log source.
---

# Threat Hunter

Convert a threat report into a hunt package for Google SecOps. Extract explicit and inferred attacker behaviors, map them to MITRE ATT&CK, identify which available log types can observe them, and write defensible Chronicle hunts that are primarily technique-based rather than campaign-specific.

Default output mode:

- Produce 2-3 distinct, behavior-based hunts per extracted TTP.
- Prefer hunt variants that cover different telemetry angles for the same TTP, such as endpoint/process, network/proxy, file/registry, or light correlation when the telemetry supports it.
- Do not generate near-duplicate hunts just to satisfy the count; if only 2 strong hunts are supportable, return 2 and note the telemetry gap.
- Make those hunts reusable beyond the specific source material.
- Do not turn report-specific domains, IPs, filenames, hashes, registry values, or unique paths into hunt pivots. Use article evidence only to understand and map the underlying ATT&CK behavior.
- Group hunts into `High-Fidelity`, `Medium-Fidelity`, and `Needs Validation`.
- Name the best primary `metadata.log_type` for each hunt and list secondary sources only when they add clear value.
- When relevant and available, synthesize the strongest ATT&CK-aligned hunt ideas from the external detection references listed in [external-hunt-sources.md](./references/external-hunt-sources.md) before drafting the Chronicle hunts.

PDF output mode:

- If the user asks for a PDF report, keep the exact same section order and hunt content as the default output.
- First generate the full report content in Markdown internally using the required tables and hunt blocks.
- Then render that Markdown to a PDF file when a local PDF-capable toolchain is available.
- Prefer a local renderer already present in the environment, such as `pandoc`, a `reportlab`-backed Python renderer, or another installed Markdown-to-PDF workflow.
- If no PDF renderer is available, say so clearly and do not create a Markdown file unless the user explicitly asked for one.
- By default, do not write a Markdown source file when the user only asked for a PDF or report output. Only save Markdown when the user explicitly requests a Markdown deliverable.
- In either case, tell the user where the requested output file or files were written.

## Follow this workflow

1. Read the full source material.
   Capture the report title, publisher, threat actor or campaign, target industries, target regions, malware or tooling, infrastructure, and notable procedures.
2. Prefer explicit ATT&CK mappings first.
   If the article includes an ATT&CK table or directly cites `Txxxx` or `Txxxx.xxx` IDs, extract those before inferring anything.
3. Extract additional TTPs from prose using NLP-style reasoning.
   Focus on verbs, objects, tools, APIs, command lines, protocols, execution chains, persistence actions, credential access steps, lateral movement paths, collection actions, and exfiltration methods.
4. Map inferred behaviors to MITRE ATT&CK.
   Prefer the most specific supported sub-technique. Keep a confidence rating for every inferred mapping.
5. Normalize the output into reusable TTP hunts.
   For each extracted ATT&CK technique, write 2-3 generic behavior-based hunts that would still be useful even if all report-specific indicators were removed. Make the hunts meaningfully distinct, ideally across different data sources or different observable stages of the same technique.
6. Expand into a holistic hunt view.
   Do not stay confined to only the exact procedures named in the article. Add closely related ATT&CK techniques, precursor behaviors, follow-on actions, or alternate implementations that a hunter should also search for, but label them as generalized hunt hypotheses when they are not directly evidenced by the source.
7. Map each technique to Google SecOps telemetry.
   Use only the allowlisted `metadata.log_type` values in [secops-log-types.md](./references/secops-log-types.md). If a technique depends on telemetry outside that list, call out the gap instead of inventing support.
8. Write YARAL hunt queries cautiously.
   Use only fields and event types that are reasonably supportable. If an exact `metadata.product_event_type`, `EventCode`, or UDM field is uncertain, say so and mark the hunt as a draft. Prefer one hunt block per TTP over broad multi-technique bundles unless the behavior genuinely cannot be separated.
9. Cross-reference strong public detection content.
   Use [external-hunt-sources.md](./references/external-hunt-sources.md) to mine ATT&CK-aligned behaviors, telemetry ideas, and alternate implementations for the extracted TTPs. Prioritize sources with explicit ATT&CK mappings, raw detection logic, or authoritative event semantics. Treat aggregator sites as discovery aids rather than primary truth.
10. Produce the final hunt package.
   Follow the response structure in [output-template.md](./references/output-template.md).
11. When the user requests a file deliverable.
   Preserve the exact response structure from the template, write the content only to the file format or formats the user explicitly requested when tooling allows, and avoid changing the ATT&CK-driven scope just because the output is being rendered.

## Use external detection references deliberately

Read [external-hunt-sources.md](./references/external-hunt-sources.md) when the user wants the best possible hunt quality, when they provide detection-library URLs, or when a source report leaves gaps in how to operationalize a technique.

Use those references to:

- confirm whether a TTP already has a well-known analytic pattern across community and vendor content
- identify better telemetry angles, event names, API operations, parent-child process chains, or control-plane actions for the same ATT&CK technique
- generate materially distinct hunt variants for the same TTP across endpoint, network, cloud audit, identity, email, and SaaS telemetry
- discover alternate tooling paths for the same ATT&CK technique, such as LOLBAS or GTFOBins implementations, without turning the output into a binary catalog
- improve Chronicle query quality by translating proven behavioral ideas into UDM-compatible logic

Do not use those references to:

- paste vendor query logic directly into the output without normalization
- import IOC-heavy or threat-family-specific logic as a reusable hunt
- treat a summarized aggregator page as more authoritative than the underlying rule source
- explode one ATT&CK technique into many near-duplicate hunts just because several vendors detect the same pattern

## Source prioritization and trust model

When multiple sources cover the same TTP, prefer them in roughly this order:

1. ATT&CK-native and ATT&CK-adjacent analytic sources with strong behavioral rationale, such as MITRE ATT&CK Analytics, MITRE CAR, and EQL analytics.
2. Native Google SecOps and Chronicle sources when writing YARA-L, especially Chronicle detection-rules and official YARA-L or UDM documentation.
3. Raw community or vendor rule repositories with explicit logic and ATT&CK mapping, such as Sigma, Elastic, Splunk, Azure Sentinel, Panther, Anvilogic Forge, FalconFriday, Veramine, and Sublime Security.
4. Cloud attack and event references that explain audit semantics and API patterns, such as TrailDiscover, Datadog Cloud Security Atlas, Datadog default rules, and Stratus Red Team.
5. Procedure catalogs for alternate tooling and abuse paths, such as LOLBAS and GTFOBins.
6. Discovery and aggregation layers, such as detections.ai, Rulehound, and Litmus Test.

When sources disagree:

- prefer the source with clearer ATT&CK grounding and stronger telemetry justification
- prefer the source that exposes raw logic over summaries about logic
- prefer behavior patterns that can be expressed cleanly in Chronicle over platform-specific constructs that do not translate well
- call out validation needs instead of forcing a weak translation

## Normalize external detections into Chronicle hunts

For each candidate analytic idea found in an external source:

1. Extract the ATT&CK technique, tactic, and behavior statement.
2. Identify the real observable behind the rule, such as a process chain, registry action, cloud API call, DNS pattern, or email property.
3. Strip source-specific fields, parser assumptions, environment names, and IOC lists unless they are essential to the behavior.
4. Decide whether the idea belongs in `High-Fidelity`, `Medium-Fidelity`, or `Needs Validation`.
5. Translate the idea into an allowlisted Google SecOps `metadata.log_type`.
6. Rewrite the logic in Chronicle-friendly YARA-L using supportable UDM fields only.

Good translations:

- Sigma or Elastic process rules become Chronicle hunts centered on normalized process ancestry, command-line traits, or file paths.
- Splunk, Sentinel, Panther, and Anvilogic cloud detections become Chronicle hunts centered on normalized control-plane actions and principal context.
- TrailDiscover, Datadog Cloud Security Atlas, and Stratus Red Team become cloud hunt inspirations for API abuse, privilege changes, service enablement, and exposed metadata access.
- LOLBAS and GTFOBins become alternate implementation ideas for execution, transfer, proxying, persistence, defense evasion, and privilege abuse.
- Sublime rules become email-centric ATT&CK hunts only when the source report or extracted TTP genuinely includes email delivery, credential phishing, or attachment abuse.

## Best-output synthesis rules

If the user asks for the best output, do not stop at the source article alone. Build the hunt package by combining:

- directly evidenced ATT&CK techniques from the source
- NLP-inferred ATT&CK techniques from the source procedures
- the strongest cross-source analytic ideas from the external detection references
- alternate but still relevant implementations of the same ATT&CK techniques

Then deduplicate aggressively:

- merge overlapping detections into one stronger hunt when the observable is the same
- keep separate hunts only when they represent genuinely distinct telemetry, detection strategy, or stage of the behavior
- do not let the output turn into a bibliography, platform comparison, or bulk rule conversion exercise
- optimize for the best final Chronicle hunts, not the largest number of borrowed ideas

## Extract behaviors with NLP-style reasoning

Use lightweight extraction heuristics rather than generic summarization:

- Identify action phrases such as credential dumping, scheduled task creation, remote service usage, OAuth abuse, mailbox rule creation, cloud role assignment, or service principal modification.
- Tie each action to concrete evidence when available: command lines, registry paths, API names, process names, event IDs, object names, protocols, ports, scripts, or tooling.
- Group repeated phrases into a normalized behavior before mapping to ATT&CK.
- Separate directly evidenced behaviors from analyst expansions.

Use this confidence model for inferred mappings:

- High: The technique is explicitly named, or the procedure is described with concrete command, API, tool, or artifact detail.
- Medium: The behavior clearly maps to a technique even without a direct ATT&CK mention.
- Low: The behavior is broad and could fit several techniques.

## Map to MITRE ATT&CK carefully

- Map behavior, not vague attacker intent.
- Prefer a sub-technique when the evidence supports it.
- Fall back to the parent technique when the article is too broad.
- Keep explicit mappings separate from inferred mappings.
- Include the ATT&CK technique name and the exact ATT&CK URL.
- Include tactic names when known.
- Lead with the primary technique and mention secondary mappings only when they materially improve analyst understanding.

## Build a holistic hunt set

For each directly evidenced or inferred technique, consider whether a hunter should also search for:

- Immediate prerequisites that enable the behavior
- Alternate tooling that implements the same technique
- Common follow-on actions after successful execution
- Parallel telemetry views of the same behavior across endpoint, identity, network, email, SaaS, cloud, or DNS

Only add expansions that are operationally useful and clearly related. Mark them as `Generalized hunt hypothesis` so the user can distinguish source-grounded findings from broader hunt coverage.

## Default to ATT&CK/TTP-only hunts

Detection content should:

- generalize the behavior into a reusable ATT&CK-aligned hunt
- avoid hard-coding campaign-only domains, IPs, filenames, hashes, registry values, or victim-specific artifacts
- avoid using report-specific artifacts as pivots, examples, or supplemental hunt variants
- derive hunts only from ATT&CK techniques explicitly cited in the source or inferred from the procedure text through NLP-style extraction
- prefer 2-3 hunts per extracted TTP so the output covers multiple telemetry views while remaining easy to operationalize, prioritize, and tune
- *Dont mix or combine TTP threat hunt queries.*
- *Even if they are redundant, but please keep queries for each TTP separately*

## Map techniques to Google SecOps data sources

Read [secops-log-types.md](./references/secops-log-types.md) when choosing telemetry. Favor data sources that capture the action directly rather than weak side effects.

When recommending log types:

- Use the exact `metadata.log_type` spelling from the allowlist.
- Prefer endpoint and identity telemetry for user, process, and host actions.
- Prefer SaaS or cloud audit telemetry for administrative and API-driven abuse.
- Prefer DNS, proxy, firewall, and VPC flow data for infrastructure, beaconing, or egress-related hunts.
- If the technique is not well-covered by the available telemetry, say `Telemetry gap`.

## Write YARAL for Chronicle with care

When writing hunt queries:

- Include a short comment header with the ATT&CK ID, technique name, and the data source used.
- Scope each query to the relevant `metadata.log_type`.
- Use technique-specific indicators grounded in the behavior of the ATT&CK technique, not only the source article.
- Exclude known-good behavior only when there is a defensible baseline reason.
- Prefer smaller, reviewable hunt queries over complex correlations unless the behavior genuinely requires correlation.
- Default to 2-3 hunts per extracted TTP.
- Make each hunt variant materially different. Good differences include primary log source, event type focus, stage of execution, or a stronger versus broader analytic strategy.
- For each hunt, name the best primary log source and only add secondary sources when useful.
- Assign each hunt to one of `High-Fidelity`, `Medium-Fidelity`, or `Needs Validation`.
- Use query format like $e.target.process.file.full_path = /lsass\.exe$/. Dont append i like in this query/condition - $e.target.process.file.full_path = /lsass\.exe$/i

Examples of reasonable grounding:

- `T1003.001`: suspicious access to `lsass.exe`, memory access indicators, or confirmed security telemetry fields that reflect credential dumping behavior
- `T1053.005`: scheduled task creation via `schtasks.exe`, `at.exe`, task registration artifacts, or related Windows events
- `T1059.001`: PowerShell command or script indicators in command-line or script content telemetry
- `T1021.002`: SMB-driven remote access or lateral movement artifacts

When exact field or event support is uncertain:

- say which `metadata.log_type` is likely relevant
- state which event type or field must be validated
- label the query `Draft - validate fields and event types`

Do not present speculative field names or event codes as fact.

## Final output requirements

Use the section order and tables in [output-template.md](./references/output-template.md).

Always include:

- report summary, unless the user only wants the hunt package and the report context can be compressed to 1-2 lines
- ATT&CK extraction table with explicit versus inferred source labels
- a second table or clear labels showing which rows are generalized hunt hypotheses
- log-type mapping table using the exact required column names
- 2-3 Chronicle hunts per extracted TTP, with validation notes where needed
- hunt grouping by `High-Fidelity`, `Medium-Fidelity`, and `Needs Validation`
- the best primary log source for each hunt
- a structured defensive playbook with detection goals, blind spots, false positives, triage steps, and follow-up hunt ideas
- when a PDF is requested, the same content should be rendered without collapsing sections, dropping tables, or shortening hunt metadata just to fit the file format
- do not create a Markdown file unless the user explicitly asked for one

## Quality bar

- Use the external detection references to improve hunt quality when they materially strengthen ATT&CK coverage, telemetry selection, or query logic.
- Do not invent telemetry coverage outside the allowlist.
- Do not invent ATT&CK IDs when the behavior is too vague to map.
- Do not copy the article mechanically; translate it into huntable behaviors.
- Do not copy vendor rules mechanically; translate them into normalized ATT&CK/TTP-driven Chronicle hunts.
- Do not overfit to one malware family or campaign when the technique is broader.
- Distinguish clearly between source-grounded findings and broader hunt expansion.
- Default to reusable ATT&CK/TTP hunts only; do not add IOC-driven hunt variants.
- Avoid bundling many ATT&CK techniques into one query when separate per-TTP hunts would be clearer.
- Avoid padding the output with weak duplicates; 2-3 hunts per TTP should represent distinct and defensible hunt ideas.
- If critical details are missing, say what needs validation instead of guessing.
