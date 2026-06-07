https://www.microsoft.com/en-us/security/blog/2026/04/01/mitigating-the-axios-npm-supply-chain-compromise/

For this article - do the following in order:

First use *dissection-agent*
then pass the output to *ioc-analyzer* sub-agent
and finally use the *threat-hunter* agent 

If auth fails, repair ADC first using the existing SecOps service account at /home/ubuntu/.config/gcloud/secops-sa.json if present, then retry. 
Check this file as well - /home/ubuntu/.config/gcloud/application_default_credentials.json

if you dont find secops-sa.json file, only then only try to use application default credentials file.

If not found here as well, check in /root.

If the credential file is absent, tell me what is missing instead of continuing.

Use the **exact instructions** mentioned in 3 subagents and skills they will be referencing - 

*ioc-analyzer* - which is a subagent which should then use the integrated google secops siem server to run the searches and provide a very comprehensive report of the findings. Use the reference searches mentioned in the skill referenced in the sub-agent. Run the searches for time period of last 30 days. Retry the searches if they fail. Keep the max iterations to 3.

*threat-hunter* - which is a sub-agent. For this sub-agent - use both skills - *threat-hunter* and *ttp-ioc-hunter*.
1. Use IOC based TTP hunts ONLY which you found from the article for **ttp-ioc-hunter** skill and run the searches through the integrated google secops siem server to run the searches and provide a very comprehensive report of the findings. Run the searches for time period of last 30 days. Keep the max iterations to 3.

2. Use the Holistic view and give TTP based hunts for *threat-hunter* skill and run the searches through the integrated google secops siem server to run the searches and provide a very comprehensive report of the findings. Run the searches for time period of last 30 days. Keep the max iterations to 3.
*Dont mix or combine TTP threat hunt queries.*
**Even if they are redundant, but please keep queries for each TTP separately**

I need 3 PDF Reports of the observed findings - 1 each for *ioc-analyzer*, *threat-hunter* skill and *ttp-ioc-hunter* skill.

**For the TTP Threat Hunting queries and TTP IOC queries, very strictly keep the query in a box**.

For all the 3 reports - Use the **Company logo** as the header image for all the PDFs. I want both the header to like Company and also i want the Company logo in the 3 PDF reports you are going to produce. The look and feel of the report can be taken from the reference report mentioned in the location below and logo from the referenced location HAS to be used.

For reference - please check the report in 
/workspace/.cursor/agents/IOC_Report_Axios_Sapphire_Sleet_2026-04-11.pdf

logo can be found at - /workspace/.cursor/agents/Screenshot 2026-04-11 at 3.09.24 PM.png

Give me downloadable links of the PDF reports, so i can download.

GIVE ME YOUR BEST OUTPUT. I WILL REWARD YOU WITH A LOT OF GOODIES and TOKENS.
