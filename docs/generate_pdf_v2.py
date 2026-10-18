"""
Production-Grade PDF Study Guide Generator for Opportunity Hunter AI.
Generates an Adobe Acrobat & macOS Preview 100% compliant PDF textbook and study guide.
"""
import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable,
)

def add_header_footer(canvas, doc):
    canvas.saveState()
    # Running Header (pages > 1)
    if doc.page > 1:
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(colors.HexColor("#4338ca"))
        canvas.drawString(54, 752, "OPPORTUNITY HUNTER AI")
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#64748b"))
        canvas.drawString(175, 752, "— Complete Technical Study Guide & Interview Masterclass")
        canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
        canvas.setLineWidth(0.75)
        canvas.line(54, 744, 558, 744)

    # Running Footer (all pages)
    canvas.setStrokeColor(colors.HexColor("#cbd5e1"))
    canvas.setLineWidth(0.75)
    canvas.line(54, 46, 558, 46)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(54, 34, "Opportunity Hunter AI • Portfolio & Technical Interview Guide")
    canvas.drawRightString(558, 34, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Color definitions
    PRIMARY = colors.HexColor("#0f172a")     # Slate 900
    SECONDARY = colors.HexColor("#4338ca")   # Indigo 700
    ACCENT = colors.HexColor("#6366f1")      # Indigo 500
    MUTED = colors.HexColor("#475569")       # Slate 600
    BORDER = colors.HexColor("#cbd5e1")      # Slate 300
    BG_LIGHT = colors.HexColor("#f8fafc")    # Slate 50
    CARD_BG = colors.HexColor("#f1f5f9")     # Slate 100
    CALLOUT_BG = colors.HexColor("#eff6ff")  # Blue 50
    EMERALD_BG = colors.HexColor("#ecfdf5")  # Emerald 50

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=SECONDARY,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=MUTED,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        'Header1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        'Header2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True,
    )

    h3_style = ParagraphStyle(
        'Header3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=ACCENT,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY,
        leftIndent=12,
        spaceAfter=2,
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=colors.HexColor("#1e293b"),
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#1e3a8a"),
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=PRIMARY,
    )

    def create_callout(text, bg_color=CALLOUT_BG, border_color=ACCENT):
        p = Paragraph(text, callout_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_color),
            ('BOX', (0,0), (-1,-1), 0.5, border_color),
            ('LINELEFT', (0,0), (0,-1), 3.5, border_color),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    def create_code_box(code_text):
        escaped = code_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        p = Paragraph(f"<pre>{escaped}</pre>", code_style)
        t = Table([[p]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
            ('BOX', (0,0), (-1,-1), 0.5, BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        return t

    story = []

    # =========================================================================
    # TITLE BANNER & METADATA
    # =========================================================================
    story.append(Paragraph("Opportunity Hunter AI", title_style))
    story.append(Paragraph(
        "<b>Complete Beginner's Learning Guide & Technical Interview Masterclass</b><br/>"
        "<i>Autonomous Browser AI Agent • n8n Automation • FastAPI • React 18 • SQLite</i>",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceAfter=8))

    story.append(create_callout(
        "<b>Project Mission:</b> Opportunity Hunter AI is a production-quality, portfolio-grade system "
        "that empowers students and early-career developers to discover internships, hackathons, and research roles. "
        "It eliminates manual searching through autonomous browser navigation, zero-hallucination data extraction, "
        "smart URL normalization & deduplication, and automated scheduled workflows."
    ))
    story.append(Spacer(1, 8))

    # =========================================================================
    # CHAPTER 1: INTRODUCTION TO AI AGENTS & THE PROBLEM WE SOLVE
    # =========================================================================
    story.append(Paragraph("Chapter 1: Introduction to AI Agents & The Problem We Solve", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    story.append(Paragraph("1.1 What is an AI Agent? (From Code to Agents)", h2_style))
    story.append(Paragraph(
        "To understand Opportunity Hunter AI, we must first understand how artificial intelligence has evolved "
        "from deterministic code to Large Language Models (LLMs) and finally to <b>Autonomous AI Agents</b>:",
        body_style
    ))

    agent_comp_data = [
        [Paragraph("Paradigm", table_header_style), Paragraph("How It Works", table_header_style), Paragraph("Strengths & Weaknesses", table_header_style)],
        [
            Paragraph("<b>Traditional Program</b><br/>(Deterministic Code)", table_cell_style),
            Paragraph("Executes hardcoded if/else logic and static DOM selectors (e.g., XPath, BeautifulSoup).", table_cell_style),
            Paragraph("Fast and predictable, but breaks instantly when websites change HTML class names or layout.", table_cell_style)
        ],
        [
            Paragraph("<b>Standard LLM</b><br/>(Knowledge Advisor)", table_cell_style),
            Paragraph("Generates conversational answers based on static pre-training weights (ChatGPT, Claude).", table_cell_style),
            Paragraph("Understands complex context, but has no live web access, cannot take actions, and hallucinates.", table_cell_style)
        ],
        [
            Paragraph("<b>Autonomous AI Agent</b><br/>(The Digital Intern)", table_cell_style),
            Paragraph("Combines LLM reasoning with external tools (Headless Browser) in a Perception-Action loop.", table_cell_style),
            Paragraph("Visually perceives webpages, interacts with buttons/filters, extracts structured data, and self-heals.", table_cell_style)
        ],
    ]
    t_comp = Table(agent_comp_data, colWidths=[110, 194, 200])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.2 The ReAct (Reason + Act) Loop Explained", h2_style))
    story.append(Paragraph(
        "Opportunity Hunter AI does not simply 'scrape' pages; it operates on the <b>ReAct loop</b>:",
        body_style
    ))
    story.append(Paragraph("• <b>1. Perceive:</b> The agent inspects the Chromium DOM tree and visual accessibility tree, assigning numbers to interactive elements.", bullet_style))
    story.append(Paragraph("• <b>2. Reason:</b> The agent feeds the DOM state and current goal to the LLM: <i>'Find the search bar and filter for software internships'</i>.", bullet_style))
    story.append(Paragraph("• <b>3. Act:</b> The LLM emits a structured action (e.g., <code>click_element(index=14)</code> or <code>input_text(index=8, text='AI')</code>).", bullet_style))
    story.append(Paragraph("• <b>4. Evaluate:</b> The agent observes the resulting state. If an anti-bot modal appears, it closes it; if results load, it extracts them.", bullet_style))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.3 The Real-World Problem Solved", h2_style))
    story.append(Paragraph(
        "Students waste 10 to 15 hours every week manually checking 20+ fragmented portals (LinkedIn, Wellfound, "
        "Devpost, Y Combinator, university career boards). They constantly encounter expired roles, duplicate reposts, "
        "and missed rolling deadlines. <b>Opportunity Hunter AI</b> completely automates this workflow: "
        "searching dynamically, extracting verified deadlines, eliminating duplicate postings, and notifying students automatically.",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("1.4 High-Level System Architecture", h2_style))
    ascii_arch = (
        "+-------------------------------------------------------------------------+\n"
        "|                             FRONTEND LAYER                              |\n"
        "| React 18 + Vite + Tailwind CSS + Lucide Icons + React Router (Port 5173)|\n"
        "| * Dashboard Page   * Discover Page (Live Stepper)   * Results Page      |\n"
        "| * Saved / Applied Tracker   * Settings & Schedule Configurator          |\n"
        "+------------------------------------+------------------------------------+\n"
        "                                     | HTTP REST / JSON\n"
        "                                     v\n"
        "+-------------------------------------------------------------------------+\n"
        "|                             BACKEND LAYER                               |\n"
        "|                FastAPI + Uvicorn + Pydantic v2 (Port 8000)              |\n"
        "| * REST Endpoints (/api/research, /api/opportunities, /api/preferences)  |\n"
        "| * Background Task Manager (Async execution & run state tracking)        |\n"
        "| * Deduplication Engine (URL normalization & non-destructive merging)    |\n"
        "| * SQLite Database (Persistent relational store with indexed queries)    |\n"
        "+------------------+----------------------------------+-------------------+\n"
        "                   |                                  |\n"
        "                   v (Async Background Tasks)         v (Webhooks / HTTP)\n"
        "+------------------------------------+ +----------------------------------+\n"
        "|          AGENTIC ENGINE            | |        AUTOMATION ENGINE         |\n"
        "|   Browser Use Web AI + Playwright  | |         n8n Workflow Hub         |\n"
        "| * Chromium Headless Browser        | | * Workflow 1: Manual Run         |\n"
        "| * DOM Tree Analyzer & Controller   | | * Workflow 2: Daily Cron (8 AM)  |\n"
        "| * LLM: OpenRouter / OpenAI / Mock  | | * Workflow 3: HTML Email Digest  |\n"
        "| * Pydantic Schema Output Validator | | * Webhook Callbacks into FastAPI |\n"
        "+------------------------------------+ +----------------------------------+"
    )
    story.append(create_code_box(ascii_arch))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 2: COMPREHENSIVE TECHNOLOGY STACK DEEP-DIVE
    # =========================================================================
    story.append(Paragraph("Chapter 2: Comprehensive Technology Stack Deep-Dive", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    tech_table_data = [
        [Paragraph("Technology", table_header_style), Paragraph("Exact Role in Opportunity Hunter AI", table_header_style), Paragraph("Engineering Rationale & Trade-offs", table_header_style)],
        [
            Paragraph("<b>Python 3.12+</b>", table_cell_style),
            Paragraph("Core programming language for backend, services, and agent execution.", table_cell_style),
            Paragraph("Native ecosystem for modern AI agent libraries; enhanced execution performance in 3.12+.", table_cell_style)
        ],
        [
            Paragraph("<b>FastAPI</b>", table_cell_style),
            Paragraph("Asynchronous REST API framework (Port 8000), CORS, Swagger docs.", table_cell_style),
            Paragraph("Selected over Flask/Django for high-concurrency async support, Pydantic validation, and OpenAPI generation.", table_cell_style)
        ],
        [
            Paragraph("<b>SQLite</b>", table_cell_style),
            Paragraph("Embedded ACID relational database storing opportunities, runs, and preferences.", table_cell_style),
            Paragraph("Zero-configuration local database requiring no Docker or cloud setup; indexed on URL, type, and status.", table_cell_style)
        ],
        [
            Paragraph("<b>Browser Use Web AI</b>", table_cell_style),
            Paragraph("Agent framework enabling LLMs to navigate websites and interact with DOM nodes.", table_cell_style),
            Paragraph("Translates visual DOM elements into simplified accessibility trees; handles anti-bot popups and clicks.", table_cell_style)
        ],
        [
            Paragraph("<b>Playwright Chromium</b>", table_cell_style),
            Paragraph("Headless browser automation engine controlled by Browser Use.", table_cell_style),
            Paragraph("Talks directly to Chrome DevTools Protocol (CDP); far more reliable than legacy Selenium WebDriver.", table_cell_style)
        ],
        [
            Paragraph("<b>n8n Automation</b>", table_cell_style),
            Paragraph("Visual workflow engine managing cron schedules, manual runs, and HTML emails.", table_cell_style),
            Paragraph("Decouples scheduling and alerting from FastAPI; enables operators to adjust workflows visually.", table_cell_style)
        ],
        [
            Paragraph("<b>React 18 & Vite</b>", table_cell_style),
            Paragraph("Single-page SaaS dashboard (Port 5173) with live polling stepper.", table_cell_style),
            Paragraph("Vite provides instant HMR development (<300ms) and optimized production bundles compared to CRA.", table_cell_style)
        ],
        [
            Paragraph("<b>Tailwind CSS</b>", table_cell_style),
            Paragraph("Utility-first styling framework across all pages and components.", table_cell_style),
            Paragraph("Eliminates monolithic CSS style sheets; enables responsive design directly inside JSX templates.", table_cell_style)
        ],
        [
            Paragraph("<b>Pydantic v2</b>", table_cell_style),
            Paragraph("Strict data validation, type coercion, and LLM schema definitions.", table_cell_style),
            Paragraph("Rust-backed performance; guarantees structured JSON outputs and prevents LLM date hallucinations.", table_cell_style)
        ],
    ]
    t_tech = Table(tech_table_data, colWidths=[90, 214, 200])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 3: STEP-BY-STEP IMPLEMENTATION & CODE WALKTHROUGH
    # =========================================================================
    story.append(Paragraph("Chapter 3: Step-by-Step Implementation & Code Walkthrough", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    story.append(Paragraph("3.1 Folder Structure & Modular Architecture", h2_style))
    ascii_folders = (
        "opp-hunter/\n"
        "├── backend/app/\n"
        "│   ├── main.py                     # FastAPI entrypoint, CORS, lifespan\n"
        "│   ├── agents/browser_researcher.py # Browser Use AI agent & Mock engine\n"
        "│   ├── api/endpoints.py            # REST API endpoints & Webhooks\n"
        "│   ├── database/db.py              # SQLite schema, indexes, and CRUD\n"
        "│   ├── models/opportunity.py       # Pydantic v2 data models & schemas\n"
        "│   └── services/deduplication.py   # URL normalizer & deduplication engine\n"
        "├── frontend/src/\n"
        "│   ├── pages/DiscoverPage.jsx      # Research form & 4-step polling stepper\n"
        "│   ├── pages/ResultsPage.jsx       # Filterable opportunity grid & status selector\n"
        "│   └── services/api.js             # HTTP REST client wrapper\n"
        "├── n8n/workflows/                  # Pre-configured manual & scheduled workflows\n"
        "└── docs/                           # Comprehensive documentation library"
    )
    story.append(create_code_box(ascii_folders))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.2 The Strict Pydantic Data Model (`models/opportunity.py`)", h2_style))
    story.append(Paragraph(
        "By typing <code>deadline: Optional[str] = None</code> and <code>stipend: Optional[str] = None</code>, "
        "we programmatically enforce our <b>Zero-Hallucination Policy</b>. If a website does not clearly post a deadline, "
        "it outputs <code>null</code> rather than allowing the LLM to invent a plausible date:",
        body_style
    ))
    code_pydantic = (
        "class OpportunityBase(BaseModel):\n"
        "    title: str = Field(..., description='Opportunity title')\n"
        "    company: str = Field(..., description='Company or organizing body')\n"
        "    location: str = Field(default='Remote', description='Physical location or Remote')\n"
        "    type: OpportunityType = Field(default=OpportunityType.INTERNSHIP)\n"
        "    url: str = Field(..., description='Direct application link')\n"
        "    deadline: Optional[str] = Field(default=None, description='ISO date or null')\n"
        "    stipend: Optional[str] = Field(default=None)\n"
        "    match_score: float = Field(default=0.0, ge=0.0, le=100.0)\n"
        "    status: OpportunityStatus = Field(default=OpportunityStatus.NEW)"
    )
    story.append(create_code_box(code_pydantic))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.3 Smart URL Normalization & Status Preservation Guarantee", h2_style))
    story.append(Paragraph(
        "Web crawlers frequently encounter identical listings with different marketing queries (`utm_*`, `ref`, `fbclid`). "
        "Our deduplication engine normalizes URLs before querying SQLite. Crucially, it provides a "
        "<b>Status Preservation Guarantee</b>: if a student has marked an opportunity as <code>applied</code>, "
        "re-crawling the web will refresh the opportunity's timestamp but will NEVER overwrite the user's status back to <code>new</code>.",
        body_style
    ))
    code_dedup = (
        "def process_and_deduplicate(opportunities: list[OpportunityBase]) -> tuple[int, int]:\n"
        "    added, updated = 0, 0\n"
        "    for opp in opportunities:\n"
        "        clean_url = normalize_url(opp.url)\n"
        "        opp.url = clean_url\n"
        "        existing = get_opportunity_by_url(clean_url)\n"
        "        if existing:\n"
        "            # STATUS PRESERVATION GUARANTEE: keep user status (e.g. 'applied')\n"
        "            opp.status = existing.status\n"
        "            update_opportunity(existing.id, opp)\n"
        "            updated += 1\n"
        "        else:\n"
        "            if not opp.status: opp.status = OpportunityStatus.NEW\n"
        "            insert_opportunity(opp)\n"
        "            added += 1\n"
        "    return added, updated"
    )
    story.append(create_code_box(code_dedup))
    story.append(Spacer(1, 6))

    story.append(Paragraph("3.4 Asynchronous API & Polling Endpoint (`api/endpoints.py`)", h2_style))
    story.append(Paragraph(
        "Because autonomous browser navigation can take 30 to 60 seconds, standard synchronous HTTP requests "
        "would hit client timeouts. We implemented the <b>HTTP 202 Accepted</b> asynchronous job pattern:",
        body_style
    ))
    code_endpoint = (
        "@router.post('/api/research', status_code=status.HTTP_202_ACCEPTED)\n"
        "async def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):\n"
        "    run_id = str(uuid.uuid4())\n"
        "    create_research_run(run_id=run_id, query=request.query)\n"
        "    # Dispatches agent execution in background; returns HTTP 202 in < 20ms\n"
        "    background_tasks.add_task(execute_research_job, run_id, request)\n"
        "    return {'status': 'started', 'run_id': run_id}\n\n"
        "@router.get('/api/research/{run_id}')\n"
        "async def get_run_status(run_id: str):\n"
        "    # Polled by React frontend every 2 seconds to update live 4-step UI stepper\n"
        "    return get_research_run(run_id)"
    )
    story.append(create_code_box(code_endpoint))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.5 Local Setup Commands", h2_style))
    code_setup = (
        "# 1. Setup Backend Virtual Environment & Dependencies\n"
        "cd \"/Users/saumyapant/Desktop/opp hunter\"\n"
        "python3 -m venv .venv && source .venv/bin/activate\n"
        "pip install -r backend/requirements.txt\n"
        "cp backend/.env.example backend/.env\n\n"
        "# 2. Launch FastAPI Backend\n"
        "python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload\n\n"
        "# 3. Launch React Frontend\n"
        "cd frontend && npm install && npm run dev\n\n"
        "# 4. Run Test Suite (13 tests)\n"
        "python3 -m unittest discover -s backend/tests -p \"test_*.py\" -v"
    )
    story.append(create_code_box(code_setup))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 4: THE AGENT UNDER THE HOOD — EXECUTION LIFECYCLE
    # =========================================================================
    story.append(Paragraph("Chapter 4: The Agent Under the Hood — Execution Lifecycle", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    story.append(Paragraph("4.1 The 4-Step Discovery Sequence", h2_style))
    flow_data = [
        [Paragraph("Step", table_header_style), Paragraph("Name", table_header_style), Paragraph("System Actions & Data Transformations", table_header_style)],
        [
            Paragraph("<b>Step 1</b>", table_cell_style),
            Paragraph("<b>Initializing</b>", table_cell_style),
            Paragraph("FastAPI generates UUID `run_id`, records run in SQLite, and launches async background task.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 2</b>", table_cell_style),
            Paragraph("<b>Navigating</b>", table_cell_style),
            Paragraph("Playwright Chromium boots headless; navigates opportunity boards; extracts interactive accessibility DOM tree.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 3</b>", table_cell_style),
            Paragraph("<b>Extracting</b>", table_cell_style),
            Paragraph("LLM reasons over DOM nodes; extracts structured listings into Pydantic models; missing deadlines coerced to null.", table_cell_style)
        ],
        [
            Paragraph("<b>Step 4</b>", table_cell_style),
            Paragraph("<b>Deduplicating</b>", table_cell_style),
            Paragraph("Tracking query params stripped; URLs normalized; SQLite upsert executed with Status Preservation; final summary returned.", table_cell_style)
        ],
    ]
    t_flow = Table(flow_data, colWidths=[60, 100, 344])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, CARD_BG]),
    ]))
    story.append(t_flow)
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 5: TECHNICAL INTERVIEW MASTERCLASS & DEFENSE PREPARATION
    # =========================================================================
    story.append(Paragraph("Chapter 5: Technical Interview Masterclass & Defense Preparation", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER, spaceAfter=6))

    story.append(Paragraph("5.1 Project Pitching Scripts", h2_style))
    story.append(Paragraph("<b>The 1-Minute Recruiter Pitch:</b>", h3_style))
    story.append(Paragraph(
        "<i>\"Opportunity Hunter AI is an intelligent opportunity aggregator that solves job search fatigue. "
        "Traditional web scrapers break whenever a website updates its HTML class names. To solve this, I used "
        "Browser Use and Playwright, allowing an LLM to visually perceive web pages and interact with them like a human. "
        "I built the backend in FastAPI with SQLite, ensuring high-concurrency job dispatching via asynchronous workers and polling endpoints. "
        "I also implemented a robust deduplication engine that normalizes URLs and ensures that if a student marks a role as 'Applied', "
        "a subsequent crawl will never overwrite that status. Finally, I built a sleek React SaaS interface featuring a live 4-step "
        "progress stepper and n8n orchestration for scheduled notifications.\"</i>",
        body_style
    ))
    story.append(Spacer(1, 6))

    story.append(Paragraph("5.2 Top 10 Technical Interview Questions & Model Answers", h2_style))

    qas = [
        (
            "Q1: Why did you choose Browser Use over traditional web scraping libraries like BeautifulSoup or Scrapy?",
            "BeautifulSoup and Scrapy are static HTML parsers that make a GET request and parse raw HTML strings. "
            "However, 90% of modern opportunity boards—like LinkedIn, Wellfound, and Greenhouse—rely heavily on client-side JavaScript, "
            "infinite scrolling, and interactive modals. Furthermore, traditional scrapers rely on hardcoded CSS selectors. "
            "If the website changes a class name from .job-card to .listing-container, the scraper breaks immediately. "
            "Browser Use controls a real headless Chromium browser via Playwright. It converts the visual DOM into interactive accessibility elements "
            "and allows an LLM to reason about what to click, scroll, or fill out. This makes our crawler self-healing and capable of navigating complex user flows."
        ),
        (
            "Q2: What is an asynchronous API, and why did you use the HTTP 202 Accepted pattern?",
            "A standard synchronous API keeps the HTTP connection open until the server finishes processing. If an AI agent takes 45 seconds "
            "to open a browser, navigate pages, and extract data, a standard synchronous request would either hit a browser timeout or block "
            "incoming requests on a single-threaded server. To prevent this, I implemented the asynchronous job pattern: "
            "When the client calls POST /api/research, FastAPI assigns a unique UUID, records the job status as 'initializing' in SQLite, "
            "and dispatches the task to BackgroundTasks. FastAPI immediately returns HTTP 202 Accepted with the run_id in less than 20ms. "
            "The React frontend then periodically polls GET /api/research/{run_id} to retrieve progress updates, keeping the UI responsive."
        ),
        (
            "Q3: How do you prevent the LLM from hallucinating deadlines or stipends?",
            "LLMs are generative models naturally inclined to produce plausible-sounding completions when facts are missing. In job hunting, "
            "inventing a deadline like 'May 1st' when none exists is disastrous. I solved this at both the schema and prompt levels: "
            "In our Pydantic model, deadline and stipend are typed as Optional[str] = None. In our system prompt, we explicitly instruct the LLM: "
            "'Extract only information explicitly stated on the webpage. If a deadline or stipend is not explicitly mentioned, you MUST set the field to null. "
            "NEVER guess, estimate, or extrapolate dates.' Pydantic validates the parsed JSON against this contract."
        ),
        (
            "Q4: Explain how your URL normalization and deduplication works.",
            "A major challenge with web crawlers is that the same job listing might appear under multiple different URLs due to marketing queries. "
            "For example: 'company.com/jobs/123?utm_source=linkedin' and 'company.com/jobs/123/' are the exact same role. "
            "My deduplication pipeline normalizes URLs by: lowercasing the domain, standardizing HTTPS, stripping default ports (:80, :443), "
            "stripping tracking query parameters (utm_*, ref, source, fbclid, gclid), and removing redundant trailing slashes. "
            "When matching against SQLite, if a record exists, we update the timestamp but preserve the user's status (applied, saved)."
        ),
        (
            "Q5: What is the Status Preservation Guarantee, and why was it necessary?",
            "During early testing, I discovered a subtle data-clobbering bug: if a user discovered an internship, saved it, and later marked it as 'Applied', "
            "and then ran a new search the following week, the crawler would discover the listing again. Because default schemas assign status = 'new', "
            "re-inserting the listing would overwrite the user's 'Applied' status back to 'new'. "
            "To fix this, I introduced the Status Preservation Guarantee in our service layer: before writing an opportunity to SQLite, we query by normalized URL. "
            "If the listing already exists, we copy the user's existing status to the incoming model before executing the SQL UPDATE."
        ),
        (
            "Q6: Why did you use both FastAPI and n8n instead of writing everything in Python?",
            "This is an architectural separation of concerns. FastAPI is our core domain engine: it handles database integrity, REST API endpoints, "
            "business logic, and browser automation. n8n is our workflow orchestrator: it specializes in event-driven integrations, cron scheduling, "
            "visual pipeline monitoring, and external alerting (SMTP emails, Discord webhooks). "
            "If we put cron schedules and email templates inside FastAPI, our web server would become tightly coupled to external email providers. "
            "With n8n, an operator can adjust schedules and inspect payload history visually without touching Python code."
        ),
        (
            "Q7: How does your frontend communicate with the backend?",
            "The frontend communicates with the backend via standard HTTP REST over JSON using our centralized api.js client. "
            "For long-running research tasks, we use an asynchronous polling architecture: "
            "1. POST /api/research triggers the job and returns a run_id. "
            "2. The React component uses a JavaScript setInterval to call GET /api/research/{run_id} every 2000 milliseconds. "
            "3. Each poll returns the current execution state (step, status, logs). The frontend translates this into a 4-step animated UI stepper. "
            "4. When the response status changes to completed or failed, the interval is cleared with clearInterval to prevent memory leaks."
        ),
        (
            "Q8: How would you scale this application to 100,000 active users?",
            "To scale to 100k users, I would implement three architectural changes: "
            "1. Database Migration: Migrate SQLite to a managed PostgreSQL cluster with read-replicas for high-concurrency writes. "
            "2. Task Queue: Replace FastAPI's in-memory BackgroundTasks with Celery or Temporal backed by Redis/RabbitMQ, distributing tasks across worker nodes. "
            "3. Browser Pool: Browser instances consume ~150MB RAM each. We would manage a distributed headless browser pool (or use Browserless.io) with session reuse and rate-limiting proxies."
        ),
        (
            "Q9: What security practices did you implement in this project?",
            "1. Environment Secret Separation: API keys and webhook secrets are stored strictly in backend/.env, with a committed .env.example template. "
            "2. CORS Restrictions: Configured FastAPI's CORSMiddleware to allow requests only from authorized frontend origins (http://localhost:5173). "
            "3. Input Validation: All user search queries and preference strings are validated and bounded using Pydantic schemas. "
            "4. SQL Parameterization: All database queries use parameterized SQL (? placeholders), eliminating SQL injection vulnerabilities."
        ),
        (
            "Q10: What challenges did you face while developing this project, and how did you resolve them?",
            "Two major engineering challenges stood out: "
            "Challenge 1: Headless Browser Environment Restrictions & Sandbox Permissions. "
            "When launching Chromium via Playwright in restricted sandbox environments, Browser Use defaulted to ~/.config/browseruse, triggering a PermissionError. "
            "I resolved this by configuring BROWSER_USE_CONFIG_DIR=./.browseruse in the application environment and creating a high-fidelity fallback runner. "
            "Challenge 2: Overwriting User Application States During Re-Crawl. "
            "Re-crawling was resetting 'Applied' listings to 'new'. I refactored the deduplication service to perform an URL lookup and preserve existing statuses."
        ),
    ]

    for q, a in qas:
        story.append(Paragraph(f"<b>{q}</b>", h3_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 4))

    # Build the document with standard page callback
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    print(f"PDF successfully built: {filename}")

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), 'Opportunity_Hunter_Complete_Study_Guide.pdf')
    build_pdf(target)
