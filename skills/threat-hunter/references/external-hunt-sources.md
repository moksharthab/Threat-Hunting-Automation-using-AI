# External Hunt Sources

Use these sources to strengthen ATT&CK/TTP-driven hunt quality when the user asks for the best output, provides one or more of these URLs, or when the source article does not fully explain how to operationalize the behavior.

Do not treat this list as a requirement to copy rules verbatim. The goal is to synthesize the best Chronicle hunts by normalizing the strongest behavior patterns, telemetry choices, and ATT&CK mappings.

## ATT&CK-native and analytic-framework sources

- [MITRE ATT&CK Analytics](https://attack.mitre.org/analytics/)
  - Best for ATT&CK-aligned analytic strategies and platform-specific implementations.
  - Prefer when you need authoritative ATT&CK-linked behavioral analytics.
- [MITRE CAR](https://car.mitre.org/analytics/)
  - Best for high-signal hypotheses, rationale, and data-model-aware analytics.
  - Use to understand detection theory before translating to Chronicle.
- [EQL Analytics Library](https://eqllib.readthedocs.io/en/latest/analytics.html)
  - Best for event-sequence and behavior-based endpoint analytics.
  - Useful when converting process, registry, file, and sequence logic into Chronicle hunts.

## Google SecOps and Chronicle-native sources

- [Chronicle detection-rules](https://github.com/chronicle/detection-rules/tree/main)
  - Best for YARA-L style, Chronicle-compatible logic, and SecOps-native hunt patterns.
  - Prefer when choosing final Chronicle expression style or correlation structure.

## Cross-platform rule repositories

- [SigmaHQ rules](https://github.com/SigmaHQ/sigma/tree/master/rules)
  - Best for broad ATT&CK-tagged, threat-agnostic and threat-hunting patterns across many log sources.
- [Elastic detection-rules](https://github.com/elastic/detection-rules/tree/main/rules)
  - Best for mature endpoint, cloud, and sequence analytics with explicit detection logic.
- [Splunk Security Content](https://research.splunk.com/detections/?s=03)
  - Best for ATT&CK-mapped analytics, data-source notes, and triage ideas.
- [Azure Sentinel detections](https://github.com/Azure/Azure-Sentinel/tree/b36c1d90eb82264f62255134d34407ccbd126e37/Detections)
  - Best for KQL-driven cloud and identity detections with Microsoft-centric telemetry assumptions.
- [Panther analysis rules](https://github.com/panther-labs/panther-analysis/tree/develop/rules)
  - Best for cloud, SaaS, and audit-log detections expressed with clear event-centric logic.
- [Anvilogic Forge Armory](https://github.com/anvilogic-forge/armory/tree/main/detections)
  - Best for ATT&CK-mapped behavior detections across multiple query ecosystems.
- [FalconFriday](https://github.com/FalconForceTeam/FalconFriday)
  - Best for practitioner-curated detection ideas and current tradecraft coverage.
- [Veramine Detections](https://github.com/veramine/Detections/wiki)
  - Best for additional rule examples and threat-driven detection ideas.

## Cloud attack and cloud telemetry references

- [TrailDiscover](https://traildiscover.cloud/)
  - Best for CloudTrail event semantics, ATT&CK insights, and cloud event discovery.
  - Use to identify the most relevant API operations behind a cloud ATT&CK technique.
- [Datadog Cloud Security Atlas](https://securitylabs.datadoghq.com/cloud-security-atlas/?platform%5B0%5D=gcp)
  - Best for cloud attack paths, log samples, and detection/prevention ideas.
- [Datadog default rules](https://docs.datadoghq.com/security/default_rules/)
  - Best for production detection patterns and cloud security control logic.
- [Stratus Red Team GCP techniques](https://stratus-red-team.cloud/attack-techniques/GCP/)
  - Best for cloud attack simulations and the concrete actions that should be visible in logs.

## Email and message-security detection content

- [Sublime rules](https://github.com/sublime-security/sublime-rules/tree/main)
  - Best for email delivery, phishing, impersonation, attachment, and message-abuse techniques.
  - Only use when the report or inferred TTP set genuinely includes email-centric behaviors.

## Alternate tooling and procedure catalogs

- [LOLBAS](https://lolbas-project.github.io/)
  - Best for Windows living-off-the-land binaries and ATT&CK-linked abuse patterns.
- [GTFOBins](https://gtfobins.github.io/)
  - Best for Unix/Linux alternate implementations of execution, transfer, file access, and shell escape behaviors.

## Discovery and aggregation layers

- [detections.ai](https://detections.ai/landing)
  - Use as a discovery layer for detection ideas, not as the sole authority for final hunt logic.
- [Rulehound](https://rulehound.com/rules)
  - Useful for finding rule summaries, ATT&CK tags, and source pointers.
  - Trace back to the underlying source when possible before relying on a rule summary.
- [Litmus Test](https://github.com/Kirtar22/Litmus_Test/blob/master/README.md)
  - Useful for adversary emulation, validation ideas, and testing-inspired analytic expansion.

## How to use this source list

When mining these references:

1. Start with the extracted ATT&CK techniques from the source material.
2. Search only the references relevant to those techniques and platforms.
3. Prefer sources with explicit ATT&CK mapping, raw logic, and clear telemetry assumptions.
4. Convert the strongest ideas into Chronicle-friendly, ATT&CK/TTP-based hunts.
5. Discard ideas that depend on unavailable telemetry, excessive IOC content, or source-specific environmental assumptions.

## Do not do this

- Do not dump multiple vendor translations for the same observable.
- Do not let source citations replace behavioral reasoning.
- Do not include platform-specific field names in the final Chronicle hunt unless they have a clear UDM counterpart.
- Do not use a source solely because it is popular; use it because it materially improves the final hunt.
