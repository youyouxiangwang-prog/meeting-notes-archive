# Team Onboarding, PhD Paths, and AI/Data Access Challenges

# Team Onboarding, PhD Paths, and AI/Data Access Challenges

## Summary
The team met to welcome and onboard Qibo, align on upcoming workshops with Global Logic, and discuss practical challenges in bringing generative AI into real engineering workflows. A substantial portion of the conversation focused on data access (especially Polarian), governance and permissions, and the organizational “power” needed to move initiatives forward. The group reviewed workstreams, vendor engagement, and internal tooling (Google Agents PoC, Polaris seats, MCP), with an emphasis on preparing data and resolving access blockers (Bosch ID). The dialogue also touched on PhD experiences and academic pathways, providing context for team members’ backgrounds and capabilities.

## Key Discussion Highlights
- Onboarding and background:
  - Qibo introduced his background: arrived in Germany in 2015, studied automotive engineering in Stuttgart, worked on milling machine calibration and accuracy; transitioned from physical to AI methods.
  - PhD status: thesis written (~120 pages), three papers written (one under review), defense pending; process may take months.
- PhD pathways and perspectives:
  - Differences across countries: high dropout rates in China; US tuition burdens; Germany’s PhD often structured as a paid role.
  - Variants like cumulative theses; practical vs theoretical research relevance for industry roles.
- Project focus and workstreams:
  - Goal is not “rocket science” in generative AI but integrating AI into real workflows and connecting to company data.[idx-63]
  - Three workstreams: requirements management (Michael), testing & verification (Florian), plus Bernhard as third lead; Philip as overall project lead.[idx-106]
- Organizational context and “power”:
  - Booster team role: build a cross-company overview of AI activities and use cases.
  - Business Excellence (BE) perceived to have more influence due to budget and proximity to decision-makers; needed to drive decisions (e.g., Polarian data access).
  - ED is the largest group in GDE; ensuring coverage across development areas is essential to gain approvals.[idx-97]
- Vendor engagement (Global Logic):
  - Workshop planned for Tuesday; scope still unclear—Philip to manage; Bernhard will join.
  - Philip to meet Mariusz (Global Logic) on Friday to clarify scope and deliverables.[idx-113]
  - Another workshop on Wednesday led by A.[idx-119]
  - Global Logic is already a supplier, reportedly focused on testing; the team wants to assess their AI capabilities.[idx-123]
- Tools and integration:
  - A showcased a Google Agents PoC and obtained Polaris seats.[idx-148]
  - MCP server: TTS to own implementation; A can support with code if needed.
  - Data preparation: ingest relevant data into the database ahead of MCP integration.
- Data access and governance:
  - Polarian data access has been debated for a year; need-to-know principle vs. AI-assisted search/use-cases.[idx-85]
  - Bosch ID access remains unresolved and blocks tool deployment.
  - Consider front-end inside Polarian to simplify permission handling; recognize constraints around vectors/similarity search and underlying data scope.
  - Unofficial tools are pulling Polarian APIs and sometimes getting rate-limited/blacklisted—team aims for an official, scalable approach.[idx-180]
- Architecture and deadlines:
  - Ongoing work to separate integrated requirements into layers (e.g., e-system levels), with interns using Bosch Document Intelligence on Word exports.[idx-187]
  - End-of-year push on e-system architecture and related deliverables.

## Decisions & Commitments
- Proceed with onboarding: set an introduction meeting for Qibo.
- Global Logic:
  - Philip to manage Tuesday’s workshop; Bernhard to join.
  - Philip to meet Mariusz on Friday to align on workshop scope.[idx-113]
  - A to lead another workshop on Wednesday.[idx-119]
- Tooling:
  - Show the Google Agents PoC and Polaris seats to the team.[idx-148]
  - Prioritize data ingestion before MCP integration.
  - TTS to own MCP implementation; A to support with coding if necessary.

## Action Items
1. Set up an introduction meeting to onboard Qibo to the project.
2. Attend the Global Logic workshop on Tuesday; D to manage; Bernhard to join.[idx-109]
3. Meet Mariusz from Global Logic on Friday to align on workshop scope.[idx-109]
4. Run another workshop on Wednesday (A to lead).[idx-119]
5. Show the Google Agents PoC and Polaris seats to the team.[idx-148]
6. Ingest relevant data into the database before MCP integration.
7. Provide MCP implementation; TTS owns, A supports if needed.
8. Decide and recommend on the Polarian data access approach.
9. Resolve the Bosch ID access topic blocking the tool.

## Risks / Blockers
- Persistent IT and data access hurdles (Polarian permissions, Bosch ID).
- Lack of a consolidated overview across departments can slow approvals and cause repeated questions.
- Unclear vendor workshop scope may waste time if objectives are not set.
- Unofficial API usage leading to blacklisting/rate-limits—risk to production systems.[idx-180]

## Notes & Context
- AI use-cases include LLM-supported search, requirement retrieval, and similarity search to assist engineers.[idx-176]
- Hosting front-end inside Polarian could help with permission alignment, but underlying data governance must still be resolved.
- Document Intelligence is being used via Word exports for layered requirement structuring; longer-term, a more integrated data pipeline is preferred.
- Staffing changes and internal movements were mentioned but are peripheral to the immediate project tasks.