# Google SecOps Log Types

Use only these `metadata.log_type` values when mapping ATT&CK techniques to telemetry or writing YARAL hunt queries:

```text
ARUBA_WIRELESS
AZURE_ACTIVITY
AZURE_AD
AZURE_RESOURCE_LOGS
CHROME_MANAGEMENT
CISCO_ASA_FIREWALL
CISCO_MERAKI
CISCO_ROUTER
CISCO_SWITCH
CISCO_VPN
CITRIX_NETSCALER
CLOUDFLARE_ACCESS
CLOUDFLARE_AUDIT
CLOUDFLARE_FIREWALL_EVENTS
CLOUDFLARE_WAF
CUSTOM_DNS
EFFICIENTIP_DDI
ELASTIC_WINLOGBEAT (All Windows Event ID's)
FASTLY_CDN
FASTLY_WAF
GCP_CLOUDAUDIT
GCP_DNS
GCP_FIREWALL
GCP_LOADBALANCING
GCP_SECURITYCENTER_CHOKEPOINT
GCP_SECURITYCENTER_ERROR
GCP_SECURITYCENTER_MISCONFIGURATION
GCP_SECURITYCENTER_OBSERVATION
GCP_SECURITYCENTER_THREAT
GCP_SECURITYCENTER_TOXIC_COMBINATION
GCP_SECURITYCENTER_VULNERABILITY
GCP_VPC_FLOW
GITHUB
GLEAN
HUMAN_SECURITY
IBM_NS1
KEYCLOAK
N8N_SECURITY_AUDIT_LOGS
NIX_SYSTEM
OKTA
PAN_FIREWALL
PASSWORDSTATE
PERIMETERX_BOT_PROTECTION
PROOFPOINT_MAIL
SAILPOINT_IAM
SLACK_AUDIT
THREATX_WAF
WINDOWS_DNS
WINEVTLOG (Consider all Event ID's).
WORKDAY_AUDIT
WORKDAY_USER_ACTIVITY
WORKSPACE_ACTIVITY
WORKSPACE_ALERTS
ZSCALER_INTERNET_ACCESS
```

## Selection guidance

- Use `WINEVTLOG`, `ELASTIC_WINLOGBEAT`, `NIX_SYSTEM`, or `UDM` for endpoint execution, persistence, credential access, and local privilege abuse when the fields support it.
- Use `AZURE_ACTIVITY`, `AZURE_AD`, `AZURE_RESOURCE_LOGS`, `GCP_CLOUDAUDIT`, `OKTA`, `KEYCLOAK`, `SAILPOINT_IAM`, `WORKDAY_AUDIT`, `WORKDAY_USER_ACTIVITY`, `WORKSPACE_ACTIVITY`, `WORKSPACE_ALERTS`, `SLACK_AUDIT`, or `GITHUB` for identity, SaaS, and admin/API abuse.
- Use `CUSTOM_DNS`, `WINDOWS_DNS`, `GCP_DNS`, `EFFICIENTIP_DDI`, or `IBM_NS1` for DNS discovery, C2, and infrastructure hunts.
- Use `PAN_FIREWALL`, `CISCO_ASA_FIREWALL`, `CISCO_VPN`, `CISCO_MERAKI`, `CLOUDFLARE_FIREWALL_EVENTS`, `CLOUDFLARE_WAF`, `FASTLY_WAF`, `THREATX_WAF`, `ZSCALER_INTERNET_ACCESS`, `GCP_VPC_FLOW`, `GCP_FIREWALL`, `GCP_LOADBALANCING`, or `CITRIX_NETSCALER` for perimeter, network, remote access, or egress-related hunts.
- Use `PROOFPOINT_MAIL` for phishing or email-based delivery behaviors.
- If the source material points to EDR-specific concepts but the exact field names are not known, say so and mark the hunt query as draft.

## Required output table

Use this exact table shape:

```markdown
| Technique Name | TTP ID | TTP Subtechnique ID | List of Log Types Needed to detect this technique |
|---------------|--------|---------------------|---------------------------------------------------|
| Kerberoasting | T1558 | T1558.003 | WINEVTLOG, ELASTIC_WINLOGBEAT |
```

When a parent technique is used without a specific sub-technique, leave the sub-technique column as `N/A`.
