---
name: ioc-analysis
description: Analyze indicators of compromise in Google SecOps / Chronicle using the configured google_secops MCP server. Use when Codex is given one or more IP addresses, domains, URLs, or file hashes (MD5, SHA1, SHA256) and needs to normalize them, classify IOC types, search for sightings, summarize hits and no-hit results, and recommend next pivots.
---

## IOC Classification

When you receive IOCs, first classify each one by type:

| Type | Examples | Identification |
|------|----------|----------------|
| IP address | `155.94.200.209`, `10.0.0.5` | IPv4/IPv6 format |
| Domain / Hostname | `evil.com`, `api-app.uppercrafteroom.com` | FQDN or subdomain |
| MD5 hash | `e934ab38f5b4b6cac07b02bd914f08a2` | 32 hex characters |
| SHA256 hash | `47043e4823a6c21a8881de789b4185355330b5804629d23f6b43dd93f5265292` | 64 hex characters |
| SHA1 hash | `da39a3ee5e6b4b0d3255bfef95601890afd80709` | 40 hex characters |
| URL | `https://malicious.example.com/payload` | URI with scheme |
| Email address | `attacker@evil.com` | Standard email format |

# IOC Analysis

Analyze IOC inputs with the configured Google SecOps MCP server. Normalize each indicator first, run exact or near-exact searches through `google_secops`, and return a compact analyst-friendly summary that separates confirmed hits, no-hit results, and follow-on pivots.

Read [references/ioc-search-guidance.md](references/ioc-search-guidance.md) before doing substantial IOC searches. Use it for classification rules, fallback behavior, and the reporting template.

## Follow this workflow

1. Normalize the input set.
   Accept pasted lists, comma-separated values, markdown bullets, tables, or short prose. Split the input into individual candidate indicators, strip surrounding punctuation, preserve the original value, and deduplicate exact duplicates.
2. Classify each IOC before searching.
   Distinguish IPs, domains, URLs, and hashes. Reject malformed values instead of sending noisy searches to SecOps. If a value is ambiguous, use the stricter interpretation and note it.
3. Use the configured `google_secops` MCP server.
   Prefer native indicator lookup, entity lookup, or exact search tools on that server. If several tools could work, choose the most direct one for exact IOC matching instead of broad free-text search.
4. Discover the tool shape when needed.
   If the available Google SecOps MCP tools are not obvious, inspect the server's exposed tools or help first, then choose the narrowest safe search path. Do not guess hidden parameters or unsupported query syntax.
5. Search by IOC type.
   Run exact searches per indicator type. For IPs, keep source and destination semantics in mind if the tool supports them. For domains and URLs, search the full value first before pivoting to related hostnames. For hashes, use exact file-hash matching only.
6. Prefer bounded time windows.
   Use the user-provided time range when given. Otherwise default to a recent operational window and state it explicitly in the output.
7. Keep pivots disciplined.
   After a hit, suggest only a few nearby pivots that follow directly from the result, such as related hosts, users, file paths, processes, resolved IPs, or adjacent URLs. Do not expand into broad hunting unless the user asks.
8. Report no-hit results carefully.
   A no-hit result means no evidence was found in the searched data and time window. Do not imply the IOC is benign or globally absent.

## Output requirements

- Start with a compact table using these columns: `IOC | Type | Status | Window | Key Finding | Next Pivot`
- Separate confirmed hits from no-hit or invalid indicators.
- For each hit, include the strongest available evidence such as first seen, last seen, affected asset, user, log source, rule, or case reference.
- If the MCP response does not expose a field, say `Not returned by tool` instead of inventing it.
- End with a short `Notes` section covering assumptions, default time window, and any tool limitations.

## Quality rules

- Use Google SecOps MCP for the searches. Do not replace the SecOps lookup with web search or local grep.
- Prefer exact matches over fuzzy text search.
- Do not invent Chronicle fields, event types, or query syntax when falling back to a generic search tool.
- Keep original IOC values visible in the final answer even if you normalize them internally.
- Say when an IOC appears malformed, private, local-only, or otherwise low-value for SecOps searching.

## Examples

- `Use $ioc-analysis to search these IOCs in Google SecOps: 8.8.8.8, example.org, https://example.org/a, d41d8cd98f00b204e9800998ecf8427e`
- `Use $ioc-analysis to look up these SHA256 hashes in Chronicle for the last 30 days and tell me which hosts saw them.`
- `Use $ioc-analysis to triage this pasted IOC list and summarize any Google SecOps hits with recommended next pivots.`

These queries are mandatory and must be used as specified.

#### For Domain / Hostname IOCs:

```
Tool: search_udm
Arguments: {
  "query": "target.hostname = \"[DOMAIN]\" OR target.hostname = /.*[ESCAPED_DOMAIN]/ OR network.dns.questions.name = /.*[ESCAPED_DOMAIN]/",
  "hours_back": 336,
  "max_events": 500
}
```

Replace `[DOMAIN]` with the exact domain and `[ESCAPED_DOMAIN]` with the regex-escaped domain (escape dots with `\.`). This covers exact hostname matches, wildcard subdomain matches, and DNS question name matches.

#### For IP IOCs:

```
Tool: search_udm
Arguments: {
  "query": "ip = \"[IP_ADDRESS]\"",
  "hours_back": 336,
  "max_events": 500
}
```

Replace `[IP_ADDRESS]` with the IP under investigation. Start with exact match; widen if the platform stores source and destination fields separately.

#### For Hash IOCs (MD5):

```
Tool: search_udm
Arguments: {
  "query": "principal.file.md5 = \"[HASH]\" OR principal.process.file.md5 = \"[HASH]\" OR target.file.md5 = \"[HASH]\" OR target.process.file.md5 = \"[HASH]\" OR security_result.about.file.md5 = \"[HASH]\" OR src.file.md5 = \"[HASH]\" OR src.process.file.md5 = \"[HASH]\"",
  "hours_back": 336,
  "max_events": 500
}
```

Replace `[HASH]` with the exact MD5 hash value. Search ALL plausible file and process hash fields to avoid missing matches caused by schema variation.

#### For Hash IOCs (SHA256):

```
Tool: search_udm
Arguments: {
  "query": "principal.file.sha256 = \"[HASH]\" OR principal.process.file.sha256 = \"[HASH]\" OR target.file.sha256 = \"[HASH]\" OR target.process.file.sha256 = \"[HASH]\" OR security_result.about.file.sha256 = \"[HASH]\" OR src.file.sha256 = \"[HASH]\" OR src.process.file.sha256 = \"[HASH]\"",
  "hours_back": 336,
  "max_events": 500
}
```

Replace `[HASH]` with the exact SHA256 hash value.

#### For Hash IOCs (SHA1):

```
Tool: search_udm
Arguments: {
  "query": "principal.file.sha1 = \"[HASH]\" OR principal.process.file.sha1 = \"[HASH]\" OR target.file.sha1 = \"[HASH]\" OR target.process.file.sha1 = \"[HASH]\" OR security_result.about.file.sha1 = \"[HASH]\" OR src.file.sha1 = \"[HASH]\" OR src.process.file.sha1 = \"[HASH]\"",
  "hours_back": 336,
  "max_events": 500
}
```

#### For URL IOCs:

```
Tool: search_udm
Arguments: {
  "query": "target.url = \"[URL]\" OR about.url = \"[URL]\"",
  "hours_back": 336,
  "max_events": 500
}
```

#### For Email IOCs:

```
Tool: search_udm
Arguments: {
  "query": "network.email.from = \"[EMAIL]\" OR network.email.to = \"[EMAIL]\" OR principal.user.email_addresses = \"[EMAIL]\" OR target.user.email_addresses = \"[EMAIL]\"",
  "hours_back": 336,
  "max_events": 500
}
```

### Security Alerts Check

Use the `get_security_alerts` tool (MCP server: `user-secops`) to check for any alerts that may be related to the IOCs in the last 14 days.

```
Tool: get_security_alerts
Arguments: { "hours_back": 336, "max_alerts": 50 }
```

Review returned alerts and correlate any that reference the IOCs under investigation.

### Rule-Based Alert Search

Use the `search_rule_alerts` tool (MCP server: `user-secops`) to find detection rule alerts in the 14-day window.

```
Tool: search_rule_alerts
Arguments: {
  "start_time": "[14_DAYS_AGO_ISO8601]",
  "end_time": "[NOW_ISO8601]",
  "max_alerts": 50
}
```

Cross-reference returned rule alerts with the IOCs to identify any detection rules that triggered on the investigated indicators.

### Natural Language Event Search (Supplementary)

Use `search_security_events` tool (MCP server: `user-secops`) to perform supplementary natural-language searches for each IOC to catch anything the structured queries might have missed.

```
Tool: search_security_events
Arguments: {
  "text": "Find any events involving [IOC_VALUE] in the last 14 days",
  "hours_back": 336,
  "max_events": 200
}
```

### Pivot and Expand

From the results gathered in Steps 2–6, extract pivot candidates:
- New IPs, domains, hashes, or users that appear alongside the investigated IOCs.
- For the highest-value pivot candidates, repeat Steps 2–3 to chase the chain.

Use `search_udm` with the same query templates above applied to each new IOC discovered through pivoting.

## Correlation Dimensions

Across all results, correlate findings along these dimensions:

- **Time**: Identify precursor and follow-on activity around each IOC hit. Establish first seen, last seen, recurrence patterns.
- **Identity**: What users, service accounts, or principals interacted with the IOC?
- **Host**: Which hosts, processes, files, or services are involved?
- **Network**: Trace peer communications, DNS resolution chains, egress patterns, and repeated connections.
- **Resource**: Which applications, cloud assets, repositories, mailboxes, or datasets were touched?

## MITRE ATT&CK Mapping

Map observed behaviors to MITRE ATT&CK techniques:
- Map behaviors, not vague suspicions.
- Prefer the most specific technique supported by evidence.
- Explain the evidence that justifies each mapping.
- Note uncertainty when evidence fits multiple techniques.
- Avoid overclaiming objectives or attribution without corroboration.
