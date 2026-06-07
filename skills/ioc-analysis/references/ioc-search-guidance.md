# IOC Search Guidance

Use this file when the request requires meaningful IOC classification, exact-match strategy, or a more structured analyst output.

## IOC type checklist

- `IPv4`: dotted-quad address. Reject values outside `0-255` octet bounds.
- `IPv6`: colon-delimited address. Keep the original formatting visible in the report.
- `Domain`: bare hostname without scheme or path.
- `URL`: any value with a scheme, path, query, or obvious URL structure.
- `MD5`: 32 hex characters.
- `SHA1`: 40 hex characters.
- `SHA256`: 64 hex characters.

If a value contains a scheme such as `http://` or `https://`, treat it as a URL rather than a domain. If a value is wrapped in brackets, quotes, commas, or trailing punctuation, strip only the wrapper and preserve the core indicator.

## Search strategy

1. Prefer a Google SecOps MCP tool that directly supports IOC or entity lookup.
2. If no dedicated IOC tool is exposed, use the narrowest generic search or query capability on `google_secops`.
3. Search the exact IOC first.
4. Only after a hit, suggest nearby pivots that are naturally implied by the evidence.
5. Keep domains and URLs distinct.
   Search a URL as the full URL first. Pivot to the hostname only as a follow-on step.
6. Keep hashes exact.
   Never partial-match or shorten MD5, SHA1, or SHA256 values.
7. Keep IP context explicit.
   If the tool exposes source versus destination semantics, call out which side matched.

## Default time window

If the user does not specify a time window, use a recent operational window and state it explicitly. A 30-day default is usually reasonable for IOC triage unless the tool or environment suggests a better built-in default.

## Suggested pivots after a hit

- `IP`: related hostnames, communicating assets, users, destination ports, peer IPs
- `Domain`: resolved IPs, DNS clients, HTTP host sightings, related URLs
- `URL`: parent domain, requesting asset, user, user agent, adjacent paths
- `Hash`: hostname, file path, parent process, signer, user, execution evidence

## Reporting template

Use a compact table first:

```markdown
| IOC | Type | Status | Window | Key Finding | Next Pivot |
```

Then add short sections in this order when useful:

1. `Hits`
2. `No-hit or invalid indicators`
3. `Notes`

## Failure handling

- If the `google_secops` MCP server is unavailable, say so directly and stop instead of pretending the lookup succeeded.
- If the tool response is incomplete, quote the limitation briefly and continue with only the supported fields.
- If the server exposes several possible tools but none are clearly documented, inspect the available schema or help and choose the most exact-match option.
- If the search syntax for a fallback query tool is unclear, say what needs validation instead of guessing.
