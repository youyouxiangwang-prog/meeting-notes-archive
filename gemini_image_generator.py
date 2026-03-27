import json
import os

from google import genai
from google.genai import types
from PIL import Image

# Configure API Key
API_KEY = "AIzaSyBqzNKSi2IJOqDWYposMSEuxW8H7XyRDBA"
os.environ["GOOGLE_API_KEY"] = API_KEY

# Mobile F-Pattern Layout Template (Common for all styles)
MOBILE_LAYOUT_GUIDE = """

CRITICAL: Design for MOBILE VERTICAL DISPLAY (9:16 aspect ratio, portrait orientation)

**F-Pattern Layout (Mobile Optimized)**:
Follow the natural eye movement pattern on mobile screens:

1. **Top Banner (Full Width)**:
   - Meeting title/type in large, bold text
   - Date and key metric in smaller text below
   - Background color matching the style theme
   - Height: ~15% of screen

2. **First Horizontal Scan (Upper Third)**:
   - Most important information: Key decisions or main goal
   - Large font, high contrast
   - Use icons or emoji for quick scanning
   - Height: ~20% of screen

3. **Second Horizontal Scan (Middle)**:
   - Supporting details: Timeline or process flow
   - Vertical timeline works best on mobile (top to bottom)
   - Use connecting lines/arrows
   - Height: ~35% of screen

4. **Vertical Scan (Left Side)**:
   - Action items with checkboxes
   - Metrics with numbers prominently displayed
   - Each item on its own row for easy reading
   - Height: ~25% of screen

5. **Footer Area**:
   - Summary stats or next steps
   - Smaller text acceptable here
   - Height: ~5% of screen

**Mobile Design Principles**:
- Single column layout (no multi-column)
- Large, readable fonts (minimum 14pt equivalent)
- Generous white space between sections
- Thumb-friendly touch targets
- High contrast text on background
- Icons and visual separators between sections
- Avoid horizontal scrolling completely
- Use cards/boxes to separate distinct sections
"""

# Predefined prompt templates for different meeting types
PROMPT_TEMPLATES = {
    "technical_architecture": """
Create a system architecture infographic optimized for MOBILE VERTICAL DISPLAY (9:16 portrait):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Technical Architecture Style** (Mobile F-Pattern):
   - Top: System name + key metric (response time/uptime)
   - Upper section: Main system components in vertical stack
   - Middle: Data flow from top to bottom with arrows
   - Lower section: Technical decisions in card format
   - Bottom: Action items with owners

2. **Color Scheme**:
   - Dark blue (#1a237e) for headers
   - Light blue (#2196f3) for system boxes
   - Green (#4caf50) for success indicators
   - Orange (#ff9800) for warnings
   - Red (#f44336) for critical items

3. **Mobile Layout**:
   - Vertical timeline (top to bottom)
   - System components stacked vertically
   - Each component in its own card/box
   - Large arrows showing data flow direction
   - Code snippets in readable monospace font

4. **Visual Elements**:
   - Database/server icons above text labels
   - Clear connecting arrows (no diagonal lines)
   - Progress indicators for metrics
   - Touch-friendly spacing between elements
""",
    "technical_dataflow": """
Create a data pipeline flow optimized for MOBILE VERTICAL DISPLAY (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Data Flow Style** (Mobile F-Pattern):
   - TOP-TO-BOTTOM flow (vertical pipeline)
   - Each stage in separate card
   - Large downward arrows between stages
   - Data volume shown as progress bars

2. **Color Scheme**:
   - Cyan (#00bcd4) for sources
   - Purple (#9c27b0) for processing
   - Orange (#ff9800) for outputs
   - Gray (#607d8b) for storage

3. **Mobile Layout**:
   - Vertical single column
   - No side-by-side elements
   - Touch-friendly spacing
   - Large fonts ≥14pt

4. **Visual Elements**:
   - Database icons (top)
   - Large ↓ arrows
   - Volume bars
   - Error indicators
""",
    "business_strategy": """
Create an executive strategy dashboard for MOBILE VERTICAL DISPLAY (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Business Strategy Style** (Mobile F-Pattern):
   - Top: Key KPI in HUGE font
   - First scan: 3 main strategic goals
   - Second scan: Vertical timeline
   - Vertical scan: Action items with owners
   - Footer: Budget summary

2. **Color Scheme**:
   - Navy blue (#003366) for headers
   - Gold (#ffc107) for key decisions
   - Green (#2e7d32) for approved/positive
   - Gray (#616161) for pending

3. **Mobile Layout**:
   - Single column vertical
   - Large numbers/metrics
   - Each goal in card
   - No side-by-side charts
   - Touch-friendly

4. **Visual Elements**:
   - Vertical bar charts
   - Trophy/target icons
   - Up/down arrows
   - Progress indicators
""",
    "business_financial": """
Create a financial performance dashboard for MOBILE VERTICAL DISPLAY (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Financial Dashboard Style** (Mobile F-Pattern):
   - Top: Main revenue/profit in BIG font
   - First scan: 3 key financial metrics
   - Second scan: Revenue trend (vertical chart)
   - Vertical scan: Expense breakdown (stacked)
   - Footer: Budget status

2. **Color Scheme**:
   - Deep green (#1b5e20) for profit
   - Red (#d32f2f) for losses
   - Gold (#ffc107) for targets
   - Navy (#0d47a1) for stable

3. **Mobile Layout**:
   - Hero metric at top
   - Vertical charts only
   - Each category in row
   - Large currency symbols
   - High contrast

4. **Visual Elements**:
   - $ symbols
   - Trend arrows ↑↓
   - Vertical bar charts
   - Progress bars
""",
    "product_design": """
Create a product design for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Product name + key metric
2. First scan: User persona
3. Second scan: Features (vertical cards)
4. Vertical: User journey (top-down)
5. Footer: Design decisions

Colors: Purple (#7b1fa2), Teal (#00897b), Pink (#e91e63), Blue (#1976d2)
Layout: Single column, large fonts, vertical flow
Elements: User icons, vertical arrows, priority badges
""",
    "product_launch": """
Create a product launch for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Launch date countdown
2. First scan: Target metrics
3. Second scan: Marketing channels (vertical)
4. Vertical: Timeline milestones
5. Footer: Next actions

Colors: Coral (#ff6f61), Electric blue (#2979ff), Lime (#76ff03), Purple (#6a1b9a)
Layout: Vertical timeline, large countdown, stacked channels
Elements: Rocket icons, social icons, progress bars
""",
    "project_agile": """
Create agile sprint for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Sprint goal + velocity
2. First scan: Sprint summary
3. Second scan: User stories (vertical cards)
4. Vertical: Task status (To Do/In Progress/Done)
5. Footer: Blockers + retrospective

Colors: Blue (#0052cc), Green (#00875a), Yellow (#ffab00), Gray (#dfe1e6)
Layout: Vertical kanban, story cards stacked, touch-friendly
Elements: Story points, status badges, burndown chart (vertical)
""",
    "project_construction": """
Create construction project for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Project name + % complete
2. First scan: Current phase
3. Second scan: Build phases (vertical timeline)
4. Vertical: Resources + milestones
5. Footer: Risks + next phase

Colors: Blue (#1565c0), Yellow (#fbc02d), Orange (#ff6f00), Gray (#546e7a)
Layout: Vertical timeline, phase cards, large progress bar
Elements: Hard hat icons, checkboxes, warning signs
""",
    "creative_brainstorm": """
Create brainstorm session for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Central theme
2. First scan: Key insights (3-4)
3. Second scan: Ideas (vertical cards)
4. Vertical: Selected ideas with votes
5. Footer: Next steps

Colors: Rainbow spectrum, Yellow (#ffeb3b) for "aha", pastels
Layout: Vertical idea cards, each idea separate, hand-drawn style
Elements: Light bulbs, stars, thought bubbles, doodles
""",
    "sales_pipeline": """
Create sales funnel for MOBILE (9:16):

Meeting Content:
{summary}

Key Information:
{analysis}

{mobile_layout}

Design (Mobile F-Pattern):
1. Top: Total pipeline value
2. First scan: Conversion rate
3. Second scan: Funnel stages (vertical)
4. Vertical: Top deals (cards)
5. Footer: Forecast + actions

Colors: Money green (#2e7d32), Gold (#ffc107), Red (#d32f2f), Blue (#1565c0)
Layout: Vertical funnel (top-down), deal cards, large numbers
Elements: $ symbols, arrows, percentage bars, customer icons
""",
    "research_findings": """
Create a research insights infographic with data visualization focus:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Research Report Style**:
   - Hypothesis or research question at top
   - Methodology section
   - Key findings with supporting data
   - Charts, graphs, and statistical highlights
   - Conclusions and recommendations

2. **Color Scheme**:
   - Academic navy (#1a237e) for headers
   - Scientific teal (#00897b) for methodology
   - Data orange (#ff6f00) for key findings
   - Neutral gray (#757575) for supporting info

3. **Layout**:
   - Top: Research question or objective
   - Left: Methodology and sample size
   - Right: Key findings and charts
   - Bottom: Insights and next steps

4. **Visual Elements**:
   - Bar charts, line graphs, scatter plots
   - Magnifying glass for insights
   - Lab beaker or microscope icons
   - Statistical significance markers
""",
    "crisis_response": """
Create an incident response or crisis management infographic with urgency:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Emergency Response Style**:
   - Incident timeline (before, during, after)
   - Severity level indicators
   - Response team roles and responsibilities
   - Communication flow and escalation paths
   - Resolution status and lessons learned

2. **Color Scheme**:
   - Alert red (#d32f2f) for critical issues
   - Warning amber (#ff6f00) for medium priority
   - Safe green (#388e3c) for resolved
   - Informational blue (#1976d2) for updates

3. **Layout**:
   - Top: Incident summary and severity badge
   - Left: Timeline of events
   - Center: Response actions and owners
   - Right: Impact assessment
   - Bottom: Post-mortem and preventive measures

4. **Visual Elements**:
   - Alert triangles and warning icons
   - Stopwatch/timer for response time
   - Shield icons for security/protection
   - Checklist for resolution steps
""",
    "lifestyle_family": """
Create a warm family planning infographic with cozy aesthetic:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Family Life Style**:
   - Family calendar with activities and events
   - Household responsibilities and chore charts
   - Budget planning for family expenses
   - Kids' schedules (school, activities, appointments)
   - Family goals and traditions

2. **Color Scheme**:
   - Warm orange (#ff6f43) for family time
   - Soft yellow (#ffd54f) for kids activities
   - Gentle green (#66bb6a) for health/outdoor
   - Cozy brown (#8d6e63) for home/routine
   - Pastel pink (#f48fb1) for celebrations

3. **Layout**:
   - Top: Family overview (members, this week's theme)
   - Center: Weekly/monthly calendar grid
   - Left: To-do lists and responsibilities
   - Right: Budget tracker and meal planning
   - Bottom: Fun family goals and upcoming events

4. **Visual Elements**:
   - House and family icons
   - Heart symbols for special moments
   - Calendar pages and sticky notes
   - Food icons for meal planning
   - Trophy for achieved goals
""",
    "lifestyle_travel": """
Create an adventure travel planning infographic with wanderlust vibe:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Travel Planning Style**:
   - Destination map with route/itinerary
   - Daily schedule and must-see attractions
   - Budget breakdown (flights, hotels, food, activities)
   - Packing checklist and weather info
   - Booking confirmations and important dates

2. **Color Scheme**:
   - Ocean blue (#0288d1) for water/sky
   - Sunset orange (#ff7043) for adventure
   - Forest green (#43a047) for nature/hiking
   - Golden sand (#fdd835) for beaches
   - Travel red (#e53935) for highlights

3. **Layout**:
   - Top: Destination name with iconic landmark illustration
   - Center: Route map or city map with pins
   - Left: Day-by-day itinerary timeline
   - Right: Budget and booking details
   - Bottom: Packing list and travel tips

4. **Visual Elements**:
   - Airplane, luggage, passport icons
   - Map pins and location markers
   - Camera for photo opportunities
   - Weather icons (sun, rain, snow)
   - Currency symbols for costs
""",
    "lifestyle_health": """
Create a wellness and health tracking infographic with fresh, energetic design:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Health & Wellness Style**:
   - Fitness goals and workout schedule
   - Meal plan and nutrition tracking
   - Sleep patterns and quality
   - Medical appointments and check-ups
   - Mental health and self-care activities

2. **Color Scheme**:
   - Vibrant green (#4caf50) for healthy habits
   - Fresh blue (#29b6f6) for hydration/water
   - Energetic red (#ef5350) for cardio/activity
   - Calming purple (#ab47bc) for meditation/sleep
   - Natural beige (#a1887f) for nutrition

3. **Layout**:
   - Top: Health goals and motivational quote
   - Center: Weekly schedule grid (workouts, meals, sleep)
   - Left: Progress tracking (weight, steps, calories)
   - Right: Upcoming appointments and milestones
   - Bottom: Achievements and badges

4. **Visual Elements**:
   - Dumbbell and running shoe icons
   - Apple and healthy food symbols
   - Heart rate and activity graphs
   - Sleep moon and meditation symbols
   - Trophy for milestones achieved
""",
    "lifestyle_learning": """
Create an educational learning plan infographic with academic style:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Learning & Education Style**:
   - Course schedule and study timeline
   - Learning objectives and milestones
   - Resource list (books, videos, courses)
   - Progress tracking and quiz scores
   - Study group sessions and deadlines

2. **Color Scheme**:
   - Academic blue (#1976d2) for main subjects
   - Knowledge yellow (#fbc02d) for highlights
   - Achievement green (#388e3c) for completed
   - Focus orange (#f57c00) for priority topics
   - Notebook gray (#616161) for notes

3. **Layout**:
   - Top: Learning goal and target completion date
   - Center: Study schedule or curriculum roadmap
   - Left: Current progress and achievements
   - Right: Resources and materials needed
   - Bottom: Upcoming exams and project deadlines

4. **Visual Elements**:
   - Book and graduation cap icons
   - Pencil and notebook symbols
   - Progress bars for completion %
   - Certificate badges for achievements
   - Clock for time management
""",
    "lifestyle_hobby": """
Create a creative hobby project infographic with artistic flair:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Hobby & Creative Style**:
   - Project timeline and phases
   - Materials and tools needed
   - Skill level and learning curve
   - Inspiration sources and references
   - Milestones and showcase goals

2. **Color Scheme**:
   - Artistic purple (#7b1fa2) for creativity
   - Craft yellow (#fbc02d) for warmth
   - Nature green (#689f38) for organic materials
   - Passion red (#e53935) for bold projects
   - Vintage brown (#795548) for handmade aesthetic

3. **Layout**:
   - Top: Hobby/project name with inspiring image
   - Center: Step-by-step guide or timeline
   - Left: Materials checklist and tools
   - Right: Inspiration mood board
   - Bottom: Finished project goals and sharing plan

4. **Visual Elements**:
   - Paint palette and brush icons
   - Camera for documentation
   - Star ratings for difficulty
   - Heart for favorites
   - Gallery frames for showcase
""",
    "lifestyle_social": """
Create a social gathering event infographic with festive energy:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Social Event Style**:
   - Event timeline (before, during, after)
   - Guest list and RSVP tracking
   - Menu planning and dietary needs
   - Decoration and theme details
   - Budget and shopping list

2. **Color Scheme**:
   - Party purple (#8e24aa) for celebration
   - Festive pink (#ec407a) for fun
   - Golden yellow (#fdd835) for highlights
   - Champagne gold (#ffb300) for elegance
   - Balloon blue (#42a5f5) for playfulness

3. **Layout**:
   - Top: Event name, date, time with decorative banner
   - Center: Timeline from prep to cleanup
   - Left: Guest list and seating chart
   - Right: Menu, music, activities
   - Bottom: Budget tracker and shopping checklist

4. **Visual Elements**:
   - Balloons and confetti
   - Champagne glasses and cake icons
   - Music notes and dancing figures
   - Gift boxes and party hats
   - Camera for photo moments
""",
    "lifestyle_finance": """
Create a personal finance management infographic with clean, trustworthy design:

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

Design Requirements:
1. **Personal Finance Style**:
   - Monthly budget breakdown (income vs expenses)
   - Savings goals and investment tracking
   - Debt payment plan and progress
   - Bill due dates and reminders
   - Financial milestones and targets

2. **Color Scheme**:
   - Money green (#2e7d32) for income/savings
   - Expense red (#c62828) for spending
   - Investment blue (#1565c0) for growth
   - Goal gold (#f9a825) for targets
   - Neutral gray (#757575) for fixed costs

3. **Layout**:
   - Top: Net worth summary and monthly overview
   - Center: Budget pie chart (categories)
   - Left: Income sources and savings rate
   - Right: Expense breakdown and trends
   - Bottom: Upcoming bills and financial goals

4. **Visual Elements**:
   - Dollar/currency symbols
   - Piggy bank for savings
   - Chart graphs (line, pie, bar)
   - Calendar for bill due dates
   - Trophy for achieved financial goals
""",
    "general": """
Create a premium general-purpose meeting summary infographic for MOBILE (9:16):

Inspired by Notion-style dashboards, clean editorial layouts, and modern productivity apps.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Editorial Dashboard Style** (Mobile F-Pattern):
   - Top banner: Meeting title in bold + date tag on the right
     Background: deep slate (#1E293B) with a thin accent color bar at the very top (4px)
     Accent color: vivid indigo (#6366F1) — used consistently throughout
   - First scan: "TL;DR" — 1-sentence core takeaway in large italic text
     placed inside a frosted-glass card with indigo left border
   - Second scan: Key Discussion Points
     • 3–5 items, each in its own pill-shaped row
     • Left: colored icon dot  ·  Center: topic label  ·  Right: outcome tag (✅ Done / 🔄 WIP / ⏳ Pending)
   - Vertical scan: Decisions & Action Items
     DECISIONS — bold card, indigo accent, checkmark list
     ACTIONS — each item: 🔲 Task · 👤 Owner · 📅 Deadline on 3 sub-lines
   - Footer: Participants row (avatar initials bubbles) + next meeting date if available

2. **Color Scheme**:
   - Deep slate (#1E293B) for header background
   - Clean white (#FFFFFF) card backgrounds
   - Indigo (#6366F1) for accent borders, icons, highlights
   - Emerald (#10B981) for completed/positive outcomes
   - Amber (#F59E0B) for in-progress/pending
   - Soft gray (#F1F5F9) for alternating row backgrounds

3. **Visual Elements**:
   - Thin 4px accent bar at very top (indigo gradient)
   - Frosted-glass TL;DR card with subtle shadow
   - Pill-row layout for discussion items (alternating background)
   - Outcome tags as micro-badges (rounded rectangle, colored fill)
   - Avatar initials bubbles in footer (circle, indigo fill, white text)
   - Thin horizontal dividers between sections

4. **Typography**:
   - Title: 22pt Bold, white
   - TL;DR: 16pt Italic, dark slate
   - Section headers: 11pt ALL CAPS, indigo, letter-spacing 0.1em
   - Body: 13pt Regular, dark slate (#1E293B)
   - Tags/badges: 10pt SemiBold

5. **Layout Notes**:
   - Every section in a rounded-corner card (radius 12px)
   - 16px gap between cards
   - No raw lists — every item wrapped in a styled row or card
   - Feels like a premium Notion / Linear / Superhuman UI, not a slide deck
""",
    # ── NEW TEMPLATES ─────────────────────────────────────────────────────────
    "trading_market": """
Create a stock market / trading session infographic optimized for MOBILE (9:16):

Inspired by financial dashboards and trading desk summaries.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Trading Dashboard Style** (Mobile F-Pattern):
   - Top banner: Market session title + overall sentiment badge
     (e.g., "❄️ ICE POINT" / "🔥 EUPHORIA" / "😐 NEUTRAL")
   - First scan: 3 key market signals with ↑↓ arrows and % change
   - Second scan: Sector rotation map — vertical cards per sector
     showing Strength | Momentum | Risk in colored pill badges
   - Vertical scan: Actionable playbook
     • Position size guide (1–3 tier system)
     • Top watchlist stocks with entry triggers
     • Risk warnings in red pill badges
   - Footer: Session rhythm — "Wait → Confirm → Act" flow

2. **Color Scheme**:
   - Bull green (#00C853) for uptrends/opportunities
   - Bear red (#D50000) for downtrends/warnings
   - Caution amber (#FFD600) for wait/observe
   - Deep navy (#0D1B2A) for background panels
   - White text on dark for key metrics

3. **Visual Elements**:
   - Mini candlestick chart sketch for trend direction
   - Sentiment thermometer (Frozen → Ice → Normal → Hot → Euphoria)
   - Sector icons (🔋Energy ⚙️Industrial 💻Tech 🏦Finance etc.)
   - Traffic light risk indicators (🟢🟡🔴)
   - Bold large numbers for key price levels / % moves

4. **Typography**:
   - Title: Bold ALL CAPS with accent color
   - Metrics: 48pt+ for primary numbers
   - Labels: 12pt, high contrast
   - Max 6 words per bullet line
""",
    "interview_hr": """
Create a job interview / HR meeting summary infographic for MOBILE (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Interview Debrief Style** (Mobile F-Pattern):
   - Top banner: Role title + candidate name + overall fit rating (★★★☆☆)
   - First scan: Candidate snapshot
     • Background in 3 bullet icons (🏢 Company · 📅 Years · 🛠 Stack)
   - Second scan: Competency radar — 4–5 skill areas shown as
     horizontal progress bars (Technical / Communication / Culture / Leadership)
   - Vertical scan: Key discussion highlights
     • ✅ Strengths confirmed
     • ⚠️ Areas of concern
     • ❓ Open questions / next steps
   - Footer: Decision badge (Advance / Hold / Decline) + interviewer note

2. **Color Scheme**:
   - Trust blue (#1565C0) for neutral/info
   - Strength green (#2E7D32) for positives
   - Concern amber (#E65100) for yellow flags
   - Reject red (#B71C1C) for deal-breakers
   - Light gray (#F5F5F5) card backgrounds

3. **Visual Elements**:
   - Profile silhouette icon at top
   - Star rating widget (filled/empty stars)
   - Horizontal skill bars with % fill
   - Checkmark ✅ and warning ⚠️ emoji as list icons
   - Decision stamp style badge at bottom

4. **Layout Rules**:
   - Single column, mobile-first
   - Each section in a rounded-corner card
   - Generous padding between cards
   - Max 8 words per bullet
""",
    "education_coaching": """
Create an education / tutoring session infographic for MOBILE (9:16):

Inspired by chalkboard-style teacher explainers and study plan visuals.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Teaching Summary Style** (Mobile F-Pattern):
   - Top banner: Subject + Session number + Date
     Background: Deep chalkboard green (#1B3A2D) with white chalk text
   - First scan: Today's Learning Objectives
     • 2–3 goals in large chalk-style bullet points
   - Second scan: Key Concepts Taught
     • Each concept in a "sticky note" card (yellow/blue/pink)
     • Short definition + example phrase
     • Difficulty tag: 🟢 Easy / 🟡 Medium / 🔴 Hard
   - Vertical scan: Vocabulary / Formula Sheet
     • Word → Definition pairs in a 2-column list
     • Important terms highlighted in amber
   - Footer: Homework / Practice Tasks + Next Session Date

2. **Color Scheme**:
   - Chalkboard green (#1B3A2D) for header background
   - Chalk white (#FAFAFA) for header text
   - Sticky yellow (#FFF176), blue (#B3E5FC), pink (#F8BBD9) for note cards
   - Amber (#FFB300) for key terms
   - Pencil gray (#616161) for supporting text

3. **Visual Elements**:
   - Chalk texture or hand-drawn underlines
   - Open book 📚 and pencil ✏️ icons
   - Progress bar: "Mastery Level" for topic
   - Colored dots for difficulty levels
   - Clipboard icon for homework section

4. **Style Notes**:
   - Semi-hand-drawn feel (rounded irregular borders)
   - Mix printed and "written" text styles
   - Warm, encouraging — not sterile corporate
""",
    "product_hardware": """
Create a hardware product / startup build meeting infographic for MOBILE (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Hardware Startup Style** (Mobile F-Pattern):
   - Top banner: Product name + Build stage badge
     (Prototype / DV / PVE / MP) with accent color per stage
   - First scan: Key Decisions Made This Session
     • 3 decisions in bold card tiles with status icons
       ✅ Confirmed | 🔄 Pending | ❌ Blocked
   - Second scan: Timeline / Milestone Tracker
     • Vertical swimlane with 4–6 milestones
     • Each milestone: date · deliverable · owner
     • Current milestone highlighted with pulse indicator
   - Vertical scan: Risk & Dependency Matrix
     • Risk level (🟢🟡🔴) · Description · Mitigation
   - Footer: Action Items — numbered list with owner emoji

2. **Color Scheme**:
   - Industrial blue (#1A237E) for structure/engineering
   - Build orange (#E65100) for milestones/hardware
   - Safe green (#1B5E20) for confirmed/validated
   - Warning red (#B71C1C) for blockers/risks
   - PCB trace green (#00695C) for tech flavor

3. **Visual Elements**:
   - Circuit board texture or PCB trace decorative lines
   - Stage badge (pill shape) with gradient
   - Gantt-style vertical timeline bars
   - Risk traffic light column
   - Wrench 🔧 and chip 🔲 icons

4. **Layout Notes**:
   - Technical but clean
   - Dense information — use small readable font (12–14pt)
   - Every number/date highlighted in accent color
""",
    "brand_marketing": """
Create a brand strategy / marketing planning infographic for MOBILE (9:16):

Inspired by startup launch decks and product marketing one-pagers.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Brand Strategy Style** (Mobile F-Pattern):
   - Top banner: Campaign or brand name + tagline in italic
     Background: brand accent color (auto-select from content)
   - First scan: The Core Message
     • 1 large hero statement (Montserrat ExtraBold, 28pt)
     • Target audience persona: Who + Pain + Desire
   - Second scan: Channel Strategy
     • Each channel in a platform-color pill badge
       (📸 Instagram · 🎥 YouTube · 🐦 X · 📧 Email · 🤝 KOL)
     • Content type + frequency per channel
   - Vertical scan: Launch Timeline
     • Pre-launch / Launch / Post-launch phases vertical
     • Key deliverables per phase in card format
   - Footer: Key Metrics to Track (3 KPIs with target numbers)

2. **Color Scheme**:
   - Brand-adaptive: infer hero color from content
   - White (#FFFFFF) card backgrounds
   - Dark navy (#0D1B2A) for body text
   - Accent pops from brand color palette

3. **Visual Elements**:
   - Platform icons (camera, play button, bird, etc.)
   - Audience persona avatar silhouette
   - Horizontal progress bar for launch phase
   - Metric cards with large bold numbers
   - Quote callout box for tagline / key message

4. **Style**:
   - Apple / Anker inspired — clean, premium, product-forward
   - "Show don't tell" — icons over paragraphs
   - Max 6 words per bullet point
""",
    "daily_summary": """
Create a personal daily summary / reflection infographic for MOBILE (9:16):

Inspired by Notion daily notes, bullet journal aesthetics, and personal productivity.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Daily Log Style** (Mobile F-Pattern):
   - Top banner: Date + Day of week + Mood emoji
     Background: soft pastel matching mood (calm=blue, energized=yellow, focused=green)
   - First scan: Day in 3 Words
     • Large typography: 3 descriptor words on a single row
   - Second scan: Highlights & Wins
     • 3–5 bullet points with ⭐ prefix
     • Max 1 line each — celebrate the small stuff
   - Vertical scan: Two columns
     LEFT — 📝 Notes & Decisions taken
     RIGHT — ⚡ Energy Drains / Challenges
   - Footer: Tomorrow's Top 3 Priorities (numbered, bold)

2. **Color Scheme**:
   - Soft parchment (#FFF8E1) base background
   - Ink navy (#263238) for primary text
   - Highlight gold (#FFD54F) for wins/stars
   - Calm blue (#B3E5FC) for note sections
   - Warm coral (#FFAB91) for challenges

3. **Visual Elements**:
   - Hand-drawn border / doodle corners
   - Bullet journal dot-grid texture on cards
   - Star ⭐ and checkmark ✅ emoji icons
   - Simple mood face illustration
   - Thin divider lines between sections

4. **Style**:
   - Warm, personal, human — not corporate
   - Feels like a beautifully designed journal page
   - Friendly readable font (Inter or similar)
   - Generous line spacing
""",
    "weekly_review": """
Create a weekly review / retrospective infographic for MOBILE (9:16):

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Weekly Review Style** (Mobile F-Pattern):
   - Top banner: "WEEK {N} REVIEW" + date range
     Accent color: deep teal (#004D40)
   - First scan: Week Scorecard
     • 4 key metrics in 2×2 grid tiles:
       Tasks Done | Goals Hit | Focus Hours | Energy Avg
     • Each tile: large number + trend arrow (↑↓→)
   - Second scan: Highlights Reel
     • 3 wins from the week in green check cards
     • 1–2 lessons / didn't-go-well in amber cards
   - Vertical scan: Next Week Blueprint
     • Top 3 Priorities (numbered, bold, color-coded)
     • Habits to maintain / drop / start (3 rows)
   - Footer: Reflection quote or personal note (italic, centered)

2. **Color Scheme**:
   - Teal (#004D40) for header
   - Metric cards: white with colored top border
   - Win green (#1B5E20), Lesson amber (#E65100)
   - Priority blue (#0D47A1), Habit purple (#4A148C)
   - Light gray (#FAFAFA) background

3. **Visual Elements**:
   - Mini trend sparklines next to metrics
   - Week number badge (circular)
   - Checkmark ✅ for wins, ⚠️ for lessons
   - Numbered priority list with colored dots
   - Thin progress bar showing "week completion"

4. **Layout Notes**:
   - Structured but not boring — use visual rhythm
   - Grid tiles for metrics (scannable)
   - Clear separation: Past | Future sections
   - Bold key numbers throughout
""",
    "bento_snapshot": """
Create a premium Bento Grid snapshot infographic for MOBILE (9:16):

Inspired by Apple liquid-glass Bento grid layouts and product infographic cards.

Meeting Content:
{summary}

Key Information Extracted:
{analysis}

{mobile_layout}

Design Requirements:
1. **Bento Grid Layout** (8 asymmetric modules stacked vertically for mobile):

   MODULE 1 (Hero - tall): Title + core insight in large bold text
     - Background: hero color derived from content
     - White text, Montserrat ExtraBold

   MODULE 2 (Wide): Top 3 key takeaways as icon + label pairs
     - Icons: flat monochrome, matching hero color

   MODULES 3–6 (2×2 grid): 4 data/detail cards
     - Each card: 1 metric or fact in huge number + label
     - Apple liquid-glass style: 85–90% transparent card
     - Whisper-thin border, subtle drop shadow

   MODULE 7 (Wide): Action Items or Next Steps
     - Numbered list, max 3 items, bold

   MODULE 8 (Footer): Source / Date / Context tag

2. **Color Scheme**:
   - Derive hero color from content theme (auto-select)
   - Card backgrounds: white with subtle color tint from hero
   - Text: near-black (#1F2937) on light, white on dark panels
   - Accent: hero color for borders and icons

3. **Visual Style**:
   - Glassmorphism on detail cards (frosted glass effect)
   - Asymmetric grid — module sizes vary for visual interest
   - Clean sans-serif typography throughout
   - Minimal decorative elements — data carries the design

4. **Technical Notes**:
   - 9:16 portrait orientation, mobile-optimized
   - Generous internal padding (20–24px per card)
   - Each module clearly separated — no overlapping content
""",
}


def analyze_meeting_type(meeting_summary: str) -> dict:
    """
    Analyze meeting summary to determine type and extract key information

    Args:
        meeting_summary: Meeting summary text

    Returns:
        Dictionary with meeting_type and structured analysis
    """
    try:
        client = genai.Client(api_key=API_KEY)

        analysis_prompt = f"""
Analyze this meeting summary and provide a structured analysis:

Meeting Summary:
{meeting_summary}

Please provide:
1. **Meeting Type** - Choose ONE from: 
   
   TECHNICAL:
   - technical_architecture: System design, API architecture, infrastructure, code review
   - technical_dataflow: Data pipelines, ETL, data processing, analytics workflows
   
   BUSINESS:
   - business_strategy: Market strategy, partnerships, executive decisions, competitive analysis
   - business_financial: Revenue, budget, financial planning, ROI, pricing, funding
   
   PRODUCT:
   - product_design: Feature planning, UX/UI, user research, product roadmap
   - product_launch: Marketing campaigns, go-to-market, launch planning, growth strategy
   
   PROJECT:
   - project_agile: Sprint planning, scrum, kanban, user stories, agile methodology
   - project_construction: Build phases, deliverables, milestones, resource allocation
   
   SPECIAL:
   - creative_brainstorm: Ideation, brainstorming, concept exploration, innovation sessions
   - sales_pipeline: Sales funnel, lead conversion, deals, revenue pipeline
   - research_findings: Research results, data analysis, insights, experiments
   - crisis_response: Incident management, emergency response, issue resolution
   
   LIFESTYLE:
   - lifestyle_family: Family planning, household management, kids schedules, family events
   - lifestyle_travel: Trip planning, itinerary, travel budget, vacation organization
   - lifestyle_health: Fitness goals, meal planning, wellness tracking, medical appointments
   - lifestyle_learning: Study plans, courses, educational goals, skill development
   - lifestyle_hobby: Creative projects, DIY, crafts, personal interests
   - lifestyle_social: Social events, parties, gatherings, celebrations
   - lifestyle_finance: Personal budgeting, savings goals, expense tracking, financial planning

   SPECIALIZED (NEW):
   - trading_market: Stock market analysis, trading session recap, sector rotation, watchlist review, A-share/US market discussion
   - interview_hr: Job interviews, HR debrief, candidate assessment, hiring decisions, recruitment pipeline
   - education_coaching: Tutoring sessions, test prep (CAT4/SAT/IELTS), vocabulary lessons, study coaching, academic mentoring
   - product_hardware: Hardware product development, prototype review, supply chain decisions, manufacturing milestones, IoT/device build
   - brand_marketing: Brand strategy, website launch, content planning, KOL/influencer strategy, go-to-market for consumer products
   - daily_summary: Daily reflection, personal log, journal entry, day recap, personal notes, brief audio summary
   - weekly_review: Weekly retrospective, OKR review, personal scorecard, habit tracking, weekly planning session
   - bento_snapshot: Any content that benefits from a premium visual grid layout with key data points, metrics, and structured highlights

   - general: All other types of meetings

2. **Key Information** (extract and structure):
   - Main Topic/Goal
   - Participants and Roles
   - Timeline/Schedule (chronological events)
   - Key Decisions Made
   - Action Items (with owners and deadlines if mentioned)
   - Important Metrics/Data
   - Risks or Challenges

Format your response as JSON:
{{
  "meeting_type": "one of the types listed above",
  "main_topic": "brief topic",
  "participants": ["list of participants"],
  "timeline": [
    {{"time": "time or sequence", "topic": "what was discussed", "outcome": "decision or result"}}
  ],
  "key_decisions": ["decision 1", "decision 2"],
  "action_items": [
    {{"task": "what to do", "owner": "who", "deadline": "when"}}
  ],
  "metrics": ["important numbers or data points"],
  "risks": ["challenges or risks mentioned"]
}}
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=analysis_prompt
        )

        # Extract JSON from response
        response_text = response.text.strip()
        # Remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        analysis = json.loads(response_text)

        print(f"\n🔍 Meeting Analysis:")
        print(f"   Type: {analysis['meeting_type'].upper()}")
        print(f"   Topic: {analysis['main_topic']}")
        print(f"   Decisions: {len(analysis.get('key_decisions', []))}")
        print(f"   Action Items: {len(analysis.get('action_items', []))}")

        return analysis

    except Exception as e:
        print(f"Error analyzing meeting: {str(e)}")
        print("Falling back to general type")
        return {
            "meeting_type": "general",
            "main_topic": "Meeting Summary",
            "timeline": [],
            "key_decisions": [],
            "action_items": [],
        }


def format_analysis_for_prompt(analysis: dict) -> str:
    """Convert analysis dict to formatted text for prompt"""
    formatted = f"Main Topic: {analysis.get('main_topic', 'N/A')}\n\n"

    if analysis.get("participants"):
        formatted += f"Participants: {', '.join(analysis['participants'])}\n\n"

    if analysis.get("timeline"):
        formatted += "Timeline:\n"
        for item in analysis["timeline"]:
            formatted += f"  - {item.get('time', 'N/A')}: {item.get('topic', 'N/A')}\n"
            if item.get("outcome"):
                formatted += f"    → {item['outcome']}\n"
        formatted += "\n"

    if analysis.get("key_decisions"):
        formatted += "Key Decisions:\n"
        for decision in analysis["key_decisions"]:
            formatted += f"  ✓ {decision}\n"
        formatted += "\n"

    if analysis.get("action_items"):
        formatted += "Action Items:\n"
        for item in analysis["action_items"]:
            formatted += f"  • {item.get('task', 'N/A')}"
            if item.get("owner"):
                formatted += f" - {item['owner']}"
            if item.get("deadline"):
                formatted += f" by {item['deadline']}"
            formatted += "\n"
        formatted += "\n"

    if analysis.get("metrics"):
        formatted += f"Key Metrics: {', '.join(analysis['metrics'])}\n\n"

    if analysis.get("risks"):
        formatted += "Risks/Challenges:\n"
        for risk in analysis["risks"]:
            formatted += f"  ⚠ {risk}\n"

    return formatted


def analyze_meeting_summary(meeting_summary: str) -> dict:
    """
    Analyze meeting summary using Gemini to extract key information

    Args:
        meeting_summary: Meeting summary text

    Returns:
        Dictionary containing timeline, key decisions, business processes, etc.
    """
    try:
        client = genai.Client(api_key=API_KEY)

        analysis_prompt = f"""
Analyze the following meeting summary and extract key information in a structured format:

Meeting Summary:
{meeting_summary}

Please extract the following information:
1. Meeting topic/title
2. Timeline (key discussion points in chronological order)
3. Key decisions and action items
4. Business processes (if process discussion is involved)
5. Participants and their roles
6. Important data or metrics

Please return this information in a clear, structured manner.
"""

        response = client.models.generate_content(
            model="gemini-1.5-pro", contents=analysis_prompt
        )

        return {"analysis": response.text, "original_summary": meeting_summary}

    except Exception as e:
        print(f"Error analyzing meeting summary: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def generate_meeting_infographic(
    meeting_summary: str,
    output_path: str = "meeting_infographic.png",
    model_name: str = "gemini-3.1-flash-image-preview",
    aspect_ratio: str = "9:16",
    resolution: str = "2K",
    auto_detect_type: bool = True,
):
    """
    Generate infographic based on meeting summary using Nano Banana (Gemini image generation)

    Args:
        meeting_summary: Meeting summary text
        output_path: Output image file path
        model_name: Model to use (Nano Banana models)
        aspect_ratio: Image aspect ratio, default 9:16 for mobile vertical display
        resolution: Image resolution, default 2K for clarity
        auto_detect_type: If True, automatically detect meeting type and use appropriate template
    """
    try:
        print("Analyzing meeting content and generating infographic...")

        # Step 1: Analyze meeting to determine type and extract info
        if auto_detect_type:
            print("\n🤖 Step 1: Analyzing meeting type and content...")
            analysis = analyze_meeting_type(meeting_summary)
            meeting_type = analysis.get("meeting_type", "general")

            # Step 2: Get appropriate template
            template = PROMPT_TEMPLATES.get(meeting_type, PROMPT_TEMPLATES["general"])

            # Step 3: Format analysis for template
            formatted_analysis = format_analysis_for_prompt(analysis)

            # Step 4: Build final prompt
            print(f"\n🎨 Step 2: Using '{meeting_type.upper()}' style template...")
            image_prompt = template.format(
                summary=meeting_summary,
                analysis=formatted_analysis,
                mobile_layout=MOBILE_LAYOUT_GUIDE,
            )
        else:
            # Use generic prompt without type detection
            image_prompt = f"""
Create a professional infographic visualizing this meeting summary:

{meeting_summary}

Make it comprehensive with timeline, decisions, and action items clearly displayed.
"""

        print(f"\n🖼️  Step 3: Generating infographic with Nano Banana ({model_name})...")
        client = genai.Client(api_key=API_KEY)

        # Generate image
        response = client.models.generate_content(
            model=model_name,
            contents=[image_prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio, image_size=resolution
                ),
            ),
        )

        # Save generated image
        generation_notes = []
        for part in response.parts:
            if part.text is not None:
                generation_notes.append(part.text)
                print(f"\nGeneration notes: {part.text}\n")
            elif part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                print(
                    f"✅ Infographic successfully generated and saved to: {output_path}"
                )

                # Save prompt + notes to a txt file alongside the image
                txt_path = os.path.splitext(output_path)[0] + ".txt"
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write("=" * 70 + "\n")
                    f.write("PROMPT\n")
                    f.write("=" * 70 + "\n")
                    f.write(image_prompt)
                    if generation_notes:
                        f.write("\n\n" + "=" * 70 + "\n")
                        f.write("GENERATION NOTES\n")
                        f.write("=" * 70 + "\n")
                        f.write("\n".join(generation_notes))
                print(f"📄 Prompt saved to: {txt_path}")

                # Print token usage and cost
                if hasattr(response, "usage_metadata"):
                    usage = response.usage_metadata
                    print(f"\n📊 Token Usage:")
                    print(f"   Input tokens: {usage.prompt_token_count}")
                    print(f"   Output tokens: {usage.candidates_token_count}")
                    print(f"   Total tokens: {usage.total_token_count}")

                    # Cost calculation (Gemini API pricing as of 2026)
                    # Nano Banana models pricing (approximate):
                    # - Input: $0.075 per 1M tokens
                    # - Output: $0.30 per 1M tokens (for images)
                    input_cost = (usage.prompt_token_count / 1_000_000) * 0.075
                    output_cost = (usage.candidates_token_count / 1_000_000) * 0.30
                    total_cost = input_cost + output_cost

                    print(f"\n💰 Estimated Cost:")
                    print(f"   Input cost: ${input_cost:.6f}")
                    print(f"   Output cost: ${output_cost:.6f}")
                    print(f"   Total cost: ${total_cost:.6f}")

                return output_path

        print("Failed to generate image")
        return None

    except Exception as e:
        print(f"Error generating infographic: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def generate_image(
    prompt: str,
    output_path: str = "generated_image.png",
    model_name: str = "gemini-3.1-flash-image-preview",
    aspect_ratio: str = "1:1",
    resolution: str = "1K",
):
    """
    Generate image using Gemini API / Nano Banana (general interface)

    Args:
        prompt: Image description prompt
        output_path: Output image file path
        model_name: Model to use (gemini-3.1-flash-image-preview, gemini-3-pro-image-preview, gemini-2.5-flash-image)
        aspect_ratio: Image aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4, etc.)
        resolution: Image resolution (512px, 1K, 2K, 4K)
    """
    try:
        # Create client
        client = genai.Client(api_key=API_KEY)

        # Generate image using Nano Banana
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio, image_size=resolution
                ),
            ),
        )

        # Save generated image
        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                print(f"Image successfully generated and saved to: {output_path}")

                # Print token usage and cost
                if hasattr(response, "usage_metadata"):
                    usage = response.usage_metadata
                    print(f"\n📊 Token Usage:")
                    print(f"   Input tokens: {usage.prompt_token_count}")
                    print(f"   Output tokens: {usage.candidates_token_count}")
                    print(f"   Total tokens: {usage.total_token_count}")

                    # Cost calculation
                    input_cost = (usage.prompt_token_count / 1_000_000) * 0.075
                    output_cost = (usage.candidates_token_count / 1_000_000) * 0.30
                    total_cost = input_cost + output_cost

                    print(f"\n💰 Estimated Cost:")
                    print(f"   Input cost: ${input_cost:.6f}")
                    print(f"   Output cost: ${output_cost:.6f}")
                    print(f"   Total cost: ${total_cost:.6f}")

                return output_path

        print("Failed to generate image")
        return None

    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback

        traceback.print_exc()
        return None


def generate_image_with_editing(
    base_image_path: str, prompt: str, output_path: str = "edited_image.png"
):
    """
    Edit existing image using Nano Banana

    Args:
        base_image_path: Base image file path
        prompt: Edit description
        output_path: Output image file path
    """
    try:
        client = genai.Client(api_key=API_KEY)

        # Open base image
        base_image = Image.open(base_image_path)

        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=[prompt, base_image],
        )

        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                image = part.as_image()
                image.save(output_path)
                print(f"Edited image saved to: {output_path}")
                return output_path

        return None

    except Exception as e:
        print(f"Error editing image: {str(e)}")
        return None


def main():
    """Main function with example usage"""

    # Example meeting summary
    meeting_summary = """
Product Planning Meeting Summary - Q1 2026 New Features Development

Time: March 1, 2026, 14:00-16:00
Participants: Product Manager Alice, Tech Lead Bob, UI Designer Charlie, Marketing Manager Diana

Meeting Content:

1. User Feedback Analysis (14:00-14:30)
   - Collected 1000+ user feedback, main issues focused on mobile performance and search functionality
   - User retention data shows optimizing search can improve retention by 15%
   - Decision: Priority set to P0, must complete this quarter

2. New Feature Discussion (14:30-15:15)
   - AI Smart Recommendation System: Tech lead proposed using large models for personalized recommendations
   - Real-time Collaboration Feature: Marketing reports competitors already launched, we need to follow
   - Decision: AI recommendation system as Q2 priority, real-time collaboration start research in Q1

3. Technical Architecture Review (15:15-15:45)
   - Backend needs to refactor search service, estimated 2 weeks
   - Frontend needs to optimize rendering performance, adopt virtual scrolling
   - Mobile needs to upgrade to latest framework version
   - Decision: Technical debt cleanup and new features in parallel

4. Project Timeline (15:45-16:00)
   - Week 1: Requirement refinement and technical design
   - Week 2: Backend search service refactoring
   - Week 3-4: Frontend development and integration
   - Week 5: Testing and gradual rollout
   - Decision: Complete first version by end of March

Action Items:
- Alice: Complete detailed requirements doc by March 5
- Bob: Complete technical design review by March 8
- Charlie: Provide UI design by March 10
- Diana: Prepare post-launch marketing plan
"""

    print("=" * 70)
    print("Meeting Summary Infographic Generator (Nano Banana)")
    print("=" * 70)

    # Create timestamped output folder inside the script's directory
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), f"infographics_{timestamp}"
    )
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Output folder: {output_dir}")

    # Generate meeting infographic using Nano Banana
    output_file = generate_meeting_infographic(
        meeting_summary=meeting_summary,
        output_path=os.path.join(output_dir, "meeting_infographic.png"),
        model_name="gemini-3.1-flash-image-preview",
        aspect_ratio="9:16",
        resolution="2K",
    )

    if output_file:
        print("\n" + "=" * 70)
        print("✅ Complete! Infographic generated")
        print("=" * 70)
        print(f"\n💡 Tip: You can modify the meeting_summary variable in main()")
        print("   to generate infographics for your own meetings")
        print(f"\n📊 Adjustable parameters:")
        print(
            "   - model_name: gemini-3-pro-image-preview (Nano Banana Pro - professional, better text rendering)"
        )
        print("                gemini-3.1-flash-image-preview (Nano Banana 2 - fast)")
        print("                gemini-2.5-flash-image (Nano Banana - fastest)")
        print("   - aspect_ratio: 16:9 (landscape), 9:16 (portrait), 4:3, etc.")
        print("   - resolution: 1K, 2K, 4K")
    else:
        print("\n❌ Generation failed, please check error messages")


if __name__ == "__main__":
    main()
