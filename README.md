# Threat-Hunting-Automation-using-AI

**Overview**

The objective is to leverage external threat intelligence, including security blogs and known threat actor profiles, to proactively hunt for potential compromises within our environment. This approach will focus on identifying Indicators of Compromise (IOCs) and adversary Tactics, Techniques, and Procedures (TTPs).

The goal is to transition from a reactive security posture to a proactive threat-hunting model capable of detecting potential or ongoing threats. This process will be automated through a purpose-built, multi-component system.

The intelligence-based hunting will be run by a coordinated architecture involving "Cursor Skills" (for high-level management), specialized Subagents (for intelligence breakdown and analysis), and custom Python scripts on Cursor Cloud Agent.

**Requirements**

Required tools: Cursor
Required Integrations: Slack, Google SecOps SIEM MCP, Google SecOps SOAR MCP, GTI MCP, Email MCP

**Input for the Hunt**

**Security Blogs/Articles**: We'll feed it the links or content from security reports that describe new threats, vulnerabilities, or attack campaigns.

**Threat Actor Collection Report/Name from GTI**: We can enter the name of a known attack group (e.g., APT28, Lazarus Group) to have the system search for their associated attack methods and indicators.
(Note: To keep the results accurate and avoid false positives, we will limit the system to specific, trusted RSS feeds or user-provided inputs. The hunt can also be scheduled to run regularly.)

**System Structure and Flow**

The intelligence-based hunting will be run by a coordinated architecture involving "Cursor Skills" (for high-level management), specialized Subagents (for intelligence breakdown and analysis), and custom Python scripts on Cursor Cloud Agent.

## Cursor Skills

These skills handle the overall management of the process.

| Skill | What It Does |
|---|---|
| IOC Analysis | Analyze indicators of compromise in Google SecOps / Chronicle using the configured `google_secops` MCP server. Use when Codex is given one or more IP addresses, domains, URLs, or file hashes (`MD5`, `SHA1`, `SHA256`) and needs to normalize them, classify IOC types, search for sightings, summarize hits and no-hit results, and recommend next pivots. |
| TTP IOC Hunter | Convert threat intelligence into structured defensive outputs for Google SecOps. Extract explicit campaign details and attacker behaviors, including built-in and inferred behaviors via NLP extraction, map them to MITRE ATT&CK, identify detection opportunities from the available telemetry, and write campaign-specific YARAL queries. |
| Threat Hunter | Convert a threat report into a hunt package for Google SecOps. Extract explicit and inferred attacker behaviors via NLP extraction, map them to MITRE ATT&CK, identify which available log types can observe them, and write defensible Chronicle hunts that are primarily technique-based rather than campaign-specific. |

## Subagents

This agent is crucial for taking the raw intelligence and preparing it for execution in our infrastructure.

| Component | Function |
|---|---|
| Dissection Agent | IOC extraction specialist for cybersecurity articles, blogs, and web pages. Use proactively when the user provides a URL, article text, or blog post and wants to extract Indicators of Compromise (IOCs) such as IP addresses, domains, URLs, and file hashes. |
| IOC Analyzer Agent | IOC analysis specialist for investigating indicators of compromise, including IPs, domains, hashes, URLs, and email addresses, using Google SecOps Chronicle SIEM. Produces a PDF investigation report. Use proactively when the user provides IOCs to investigate, needs threat hunting on specific indicators, or wants a comprehensive IOC analysis report. |
| Threat Hunter Agent | Threat hunting specialist that processes threat intelligence reports through two parallel analysis pipelines: the `threat-hunter` skill for behavior-based Chronicle hunts and the `ttp-ioc-hunter` skill for YARAL detections and defensive playbooks. After both produce searches, it executes every generated query against Google SecOps Chronicle SIEM via MCP, then delivers two comprehensive PDF reports with live SIEM findings. Use proactively when the user provides a threat report, vendor blog, campaign writeup, or intelligence article and wants actionable hunt results backed by real environment data. |
| Report Emailer Agent (& Slack)| Sends PDF reports via email using an E-mail MCP server. Use proactively after generating a PDF report that needs to be emailed to SOC Mailbox and sends a message to a Slack channel with PDF attachments. |
