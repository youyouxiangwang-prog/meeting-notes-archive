# User testing: meeting-summarizer app & wearable feedback

# User testing: meeting-summarizer app & wearable feedback

## Participants
- SPK_A: Product lead/demo host for the meeting-summarizer app and wearable concept.
- SPK_B: Beta tester/user providing feedback on app features, UX, and marketing.

## Overview
The session focused on how the user leverages AI-generated meeting summaries, gaps in exporting/sharing, navigational improvements, the cross-conversation intelligence feature, support for multi-source inputs, and extensive feedback on website messaging and the wearable device’s positioning and presentation. SPK_B prefers comprehensive AI summaries over transcripts or audio replays and provided pragmatic suggestions for usability, marketing clarity, and integration priorities.

## Usage patterns and preferences
- Prefers detailed, comprehensive AI summaries (vs. Zoom’s shorter summaries).
- Typically uses the AI summary as the primary artifact; rarely returns to audio; transcripts only for pinpoint searches.
- Appreciates summaries that start with participants, purpose, model, and end with action items.[idx-32]

## Summary structure and navigation
- Keep comprehensive AI summary as the main shareable output.[idx-23]
- Add a section overview/TOC (like Google Docs) and “Jump to” controls:
  - Quick jump to Action Items.
  - Quick jump to other sections (e.g., Financials).[idx-36]
- Allow users to choose whether Action Items appear at the top or bottom; at minimum, provide a jump link.[idx-37]

## Exporting and sharing
- Critical blocker: cannot export or even copy/paste AI outputs.
- Requested export formats: Word (preferred for text-heavy outputs) and PDF. Longer-term: PPT/Excel for report generation.
- Open to the app focusing on providing a clean “personal database” that can plug into other tools (e.g., Google LLM) for specialized outputs.

## Cross-conversation intelligence
- The feature is valuable for synthesizing across multiple related meetings (e.g., stakeholder interviews with similar questions).[idx-108]
- SPK_B wants to stack multiple calls (even without audio) and get consolidated reports.
- Current outputs can include tables, but formatting on mobile is hard to read (wide tables require scrolling).
- Sources were correctly attributed, but:
  - One source stays highlighted in blue persistently.
  - Source items are not clickable; the highlight remains on reopen.

## Multi-source data ingestion
- Wants to ingest:
  - Audio
  - Text transcripts (from other teammates)
  - PDFs, PPTs, and project files relevant to a conversation or assignment
- Goal: truly cross-conversation and cross-document synthesis.

## Discoverability and home screen
- AI Insight is pinned (good), but discoverability is still limited.
- Suggest adding a home screen that proactively prompts:
  - “See your notes”
  - “Ask a question”
  - “Generate insights”
- Improve visual hierarchy: consider placing AI Insight centrally as the “home” or primary entry point.

## Formatting and deliverability
- Cross-conversation outputs that include tables are hard to read on phone; layout should be responsive.
- Needs a top “section bar” to jump within long outputs.
- The inability to copy/export renders deliverables unusable.

## Calendar integration and proactive assistance
- Integrate with calendar to reduce manual steps:
  - Daily notification bar: “You’ve got X meetings today.”
  - Pre-meeting prompts: “Would you like me to generate a report or prep notes for your meeting with [Name]?”[idx-336]
  - Record/prepare automatically when appropriate.

## Website and marketing feedback
- “Connect your memory” is confusing; prefer straightforward language:
  - Use “Cross-conversations” as the primary concept.
  - Avoid “topics” and “time” as extra tags in headers; they feel gimmicky.
- Headline suggestions:
  - Replace “World’s first memory powered wearable AI agent” with “World’s first wearable AI agent.”[idx-238]
  - Emphasize the wearable’s physical, native, always-with-you value.
- Value proposition copy:
  - “Turn conversations into reports instantly” (reduce slashes/dashes).[idx-222]
  - Consider dynamic/rotating word in the headline: “Turn conversations into [Reports | Plans | Briefs] instantly.”[idx-222]
- Visuals and copy for wear options:
  - Show all wear modalities clearly with photos that cycle like a slideshow rather than four static bullets.
  - Describe modalities with action-oriented phrases (e.g., “Integrates with your existing Apple Watch band,” “Wear as a wristband,” “Attach as a pendant,” “Clip to lapel/clothing”) instead of simple nouns.
  - Remove unnecessary bullet dots in the descriptive section.

## Wearable device feedback
- Modalities: wristband, Apple Watch-compatible band, pendant, clip.
- User preference: wristband (doesn’t own an Apple Watch; uses Garmin—support for more ecosystems would be a plus).
- Likes the wearable’s visual direction and is interested in Kickstarter participation.

## Product positioning
- Focus on two differentiated value props:
  - Wearable, native capture (always with you).
  - Cross-conversation intelligence (unique synthesis algorithm).
- Consider not competing on every output type; instead, export clean datasets and let users leverage external tools (Google LLM, etc.) for advanced visuals.

## Identified bugs and issues
- Can’t export or copy/paste AI outputs.
- Cross-conversation sources:
  - Persistent blue highlight.
  - Not clickable; highlight persists after reopening.[idx-166]
- Mobile table formatting is difficult to read (wide tables; scrolling issues).

## Agreed Action Items
1. Send SPK_B a comparison between Zoom’s summary and this app’s summary.
2. Enable exporting/copying of AI outputs and deliver within about one week.
3. Investigate why cross-conversation sources show a persistent blue highlight and aren’t clickable.

## Potential roadmap considerations
- Short-term:
  - Add export/copy functionality (Word/PDF).
  - Fix source highlighting and make sources clickable.
  - Improve mobile formatting of tables and long outputs.
  - Add section overview/TOC with jump links (incl. Action Items).
  - Home screen to increase feature discoverability (AI Insight front-and-center).[idx-115]
- Medium-term:
  - Multi-source ingestion (text, PDFs, PPTs), and true cross-document synthesis.
  - Calendar integration with proactive pre-meeting templates/reports.
  - Clearer marketing/website copy and rotating headline.
  - Wear options slideshow and ecosystem compatibility (e.g., Garmin).
- Long-term:
  - Database-level export/API to connect with external LLMs for infographics and specialized reports.
  - Optional generation of PPT/Excel outputs, if aligned with product scope.