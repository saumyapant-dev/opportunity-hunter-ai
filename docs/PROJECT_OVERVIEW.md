# Opportunity Hunter AI — Project Overview

> **An autonomous, AI-driven opportunity discovery platform designed for computer science students, early-career developers, and builders seeking tech internships, hackathons, research fellowships, and entry-level positions.**

---

## 1. Problem Statement: Why Does This Project Exist?

As computer science students and early-career developers, discovering career-defining opportunities is notoriously chaotic, fragmented, and exhausting:

1. **Information Fragmentation**: High-impact student opportunities are scattered across dozens of disparate platforms:
   - Hackathons are on **Devpost**, **Unstop**, or **MLH**.
   - Startups and tech internships post on **Hacker News ("Who is Hiring?")**, **Wellfound**, **Y Combinator Work at a Startup**, or **Lever/Greenhouse** links.
   - Undergraduate research positions are buried in university departmental sites and faculty laboratory pages.
2. **High Time Overhead**: Students waste 5 to 10 hours every week manually opening multiple tabs, searching through generic job boards, filtering out senior roles requiring 5+ years of experience, and checking if deadlines have expired.
3. **Duplicate Spam Across Aggregators**: The same opportunity is constantly cross-posted with different URL tracking parameters (UTM parameters, referral codes). Students waste time reading and applying to the same listing twice.
4. **Missed Deadlines & Lost Momentum**: Competitive student programs and research grants frequently have tight application windows (1–2 weeks). Students often discover high-value openings only after the deadline has closed.
5. **Spreadsheet Fatigue**: Managing job discovery across disjointed tools (Notion, Google Sheets, browser bookmarks) introduces friction and manual tracking errors.

**Opportunity Hunter AI** solves this problem by deploying an **autonomous AI research agent** that directly browses the web, evaluates interactive career portals, extracts validated structured listings, eliminates duplicate entries, and manages applications directly inside a centralized dashboard.

---

## 2. Core Objectives

- **Autonomous Discovery**: Provide hands-free discovery using browser automation so students don't need to manually visit 10+ websites daily.
- **Skill-Specific Relevance**: Filter positions based on actual technical skills (`Python`, `React`, `Machine Learning`, `FastAPI`, `SQL`) and experience levels (`Beginner`, `Intermediate`, `Advanced`).
- **Data Integrity & Zero Hallucination**: Never invent deadlines, qualifications, compensation, or links. If a deadline is not present on the webpage, store it strictly as `null`.
- **Intelligent Deduplication**: Normalize incoming URLs and verify title/organization similarity, while strictly **preserving** user application status (`applied`, `saved`).
- **Multi-Channel Orchestration**: Combine local on-demand research with automated 8:00 AM daily cron workflows in **n8n** and email digest alerts.
- **Accessible Learning Tool**: Built with modular, clean code so beginners can understand and defend every layer of a modern full-stack AI agent.

---

## 3. What Is an AI Agent? (Beginner Explanation)

To understand this project, you must first understand the fundamental difference between three computational models:

### A. Traditional Software Program
A traditional program follows rigid, hand-coded rules:
$$\text{Input Data} \longrightarrow \text{Hardcoded If/Else Logic} \longrightarrow \text{Output Data}$$
*If a website updates its HTML class names from `.job-card` to `.listing-item`, a traditional scraper breaks immediately.*

### B. Standard Chatbot (e.g. ChatGPT interface)
A standard chatbot is a next-token text generator operating solely in memory:
$$\text{User Prompt} \longrightarrow \text{Neural Network (Trained Weights)} \longrightarrow \text{Text Response}$$
*A chatbot cannot open a browser, click buttons, scroll an interactive web page, or save data into your SQLite database.*

### C. An Autonomous AI Agent
An **AI Agent** is an autonomous software entity that uses an LLM as its reasoning engine within a **Perception-Action Loop**:
1. **Perceive**: The agent observes its dynamic environment (e.g., extracting interactive accessibility trees and bounding boxes from a live web browser).
2. **Reason**: The agent's LLM evaluates what it sees against the user's objective (*"I need to search for beginner Python internships on this board"*).
3. **Act**: The agent chooses and executes tools (typing into search inputs, clicking filters, scrolling down).
4. **Evaluate & Repeat**: The agent inspects the new screen state to verify whether the action succeeded or if it needs to adjust course.

```
                  ┌────────────────────────┐
                  │   User Goal / Query    │
                  └───────────┬────────────┘
                              ▼
           ┌──────────────────────────────────────┐
           │        OPPORTUNITY HUNTER AI         │
           │                                      │
           │  ┌──────────┐         ┌───────────┐  │
           │  │ Observe  │ ◄─────► │  Reason   │  │
           │  │ (DOM UI) │         │   (LLM)   │  │
           │  └────┬─────┘         └───────────┘  │
           │       │                     ▲        │
           │       ▼                     │        │
           │  ┌──────────┐               │        │
           │  │   Act    │───────────────┘        │
           │  │ (Clicks) │                        │
           │  └────┬─────┘                        │
           └───────┼──────────────────────────────┘
                   ▼
       Target Website (Playwright Headless Browser)
```

---

## 4. Key Features Overview

1. **Interactive Search & Discovery Console**:
   - Filter by core technical skills (`Python`, `React`, `Java`, `SQL`, `ML`, `DSA`) with support for custom tag inputs.
   - Target specific categories: `Internship`, `Hackathon`, `Research Fellowship`, and `Entry-level Job`.
   - Filter by location (`Remote`, `India`, `Worldwide`, or specific cities).
2. **Autonomous Browser Exploration**:
   - Uses `browser-use` (0.13.10) and `Playwright Chromium` to navigate modern JavaScript Single Page Applications (SPAs).
3. **Structured Pydantic Extraction**:
   - Strictly validates extracted listings against Pydantic schemas (`OpportunityListOutput`), ensuring typed objects with zero fabricated data.
4. **Smart URL Normalization & Deduplication**:
   - Strips tracking tokens (`utm_source`, `ref`, `fbclid`).
   - Ensures previously saved or applied opportunities are never reverted to `new` status upon re-discovery.
5. **Asynchronous Non-Blocking Execution**:
   - FastAPI immediate HTTP 202 dispatch with background task workers and live 4-step polling steppers.
6. **Application Pipeline Tracker**:
   - Dedicated tracker to advance listings across lifecycle stages: `Saved` $\rightarrow$ `Interested` $\rightarrow$ `Applied` $\rightarrow$ `Archived`.
7. **n8n Orchestration Workflows**:
   - Three importable JSON workflows for manual research webhooks, scheduled daily cron harvesting, and responsive HTML email digests.
8. **High-Fidelity Mock Research Engine**:
   - Built-in zero-cost simulator allowing comprehensive testing, offline development, and live interview demos without consuming LLM credits.
9. **Full System Diagnostics**:
   - Real-time status reporting for Playwright, LLM provider keys, n8n webhook connectivity, and SQLite health.

---

## 5. Current Scope & Intentional Limitations

In software engineering and technical interviews, acknowledging technical boundaries is as important as presenting features:

| Feature / Dimension | Current Implementation | Architectural Reason / Production Path |
|---|---|---|
| **Database** | Embedded SQLite (`opportunities.db`) | Zero-config, in-process local execution. Migrates to PostgreSQL for multi-user concurrency. |
| **Authentication** | Single-user local profile (`'default'`) | Avoids unnecessary login friction for local personal use. Production path: JWT / OAuth2. |
| **Browser Execution** | Local headless Chromium | Runs locally on the user's laptop. Production path: Remote browser grid (Browserbase). |
| **Anti-Bot Defenses** | Ethical exploration; halts on CAPTCHAs | Respects website access controls and robots guidelines without deceptive circumvention. |
| **Orchestration** | Dual mode (n8n + Direct FastAPI runner) | Ensures full standalone operation even if n8n is not installed or running. |
