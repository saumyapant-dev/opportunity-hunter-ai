- Opportunity Hunter AI 

An AI-powered tool that helps students discover internships, hackathons, research opportunities, and entry-level jobs based on their skills and interests.

As a CSE student, I wanted to build something that could make finding opportunities a little easier. Instead of manually searching through different websites, the idea behind Opportunity Hunter AI is to automate the research process and bring relevant opportunities together in one place.

The project combines browser automation, AI-powered research, workflow automation, and a web dashboard where users can explore and manage the opportunities they find.

## Live Demo

- Live Website:** https://opportunity-hunter-ai-8zhf.onrender.com
- GitHub Repository:** https://github.com/saumyapant-dev/opportunity-hunter-ai
- API Documentation:** https://opportunity-hunter-ai-8zhf.onrender.com/docs
- API Health Check:** https://opportunity-hunter-ai-8zhf.onrender.com/health

The application is deployed on Render, so you can explore the web app without running it on your local machine.

## What Can It Do?

Here are some of the main features I've worked on:

- AI-Powered Opportunity Discovery:** Uses Browser Use and Playwright-based browser automation to research websites and find relevant opportunities.
- Multiple Opportunity Categories:** Supports discovering internships, hackathons, research opportunities, and entry-level jobs.
- Personalized Search:** Users can configure their skills, interests, preferred locations, and experience level.
- Automated Workflows:** Integrates with n8n for triggering research workflows, scheduling discovery runs, and setting up email notifications.
- Opportunity Management:** Save interesting opportunities and track their status as Saved, Applied, or Archived.
- Search and Filters:** Browse results by category, keywords, and remote-work preferences.
- Duplicate Detection:** Normalizes URLs and identifies duplicate listings to keep the results organized.
- Dashboard:** Displays useful statistics, recent discoveries, research progress, and system status.
- Mock Mode:** Includes a mock research engine for testing and development without using live AI research credits.
- Backend Security:** Keeps API keys and other secrets in backend environment variables instead of exposing them in frontend code.

## Tech Stack

These are the main technologies used in the project.

| Technology | Purpose |
|---|---|
| React 18 | Building the frontend |
| Vite | Frontend development and build tooling |
| Tailwind CSS | Styling the user interface |
| Python | Backend development |
| FastAPI | Creating REST APIs |
| SQLite | Storing opportunities and user preferences |
| Pydantic | Data validation |
| Browser Use | AI-assisted browser automation |
| Playwright | Browser interaction and automation |
| n8n | Workflow automation |
| Render | Deployment |

## How It Works

The project follows a simple flow:

1. The user enters their skills, interests, and search preferences in the dashboard.
2. The frontend sends the research request to the FastAPI backend.
3. The backend starts a research run using the configured research engine.
4. Browser Use can navigate supported opportunity websites and collect relevant information.
5. The collected data is validated and processed to remove duplicates.
6. The opportunities are stored in SQLite and displayed on the dashboard.
7. Users can save opportunities and update their application status.

n8n can be used to trigger research workflows and coordinate scheduled runs and email notifications. A background runner is also available for testing without an active n8n instance.

## What I Learned

Building Opportunity Hunter AI gave me an opportunity to work across both frontend and backend development while exploring AI agents and automation.

Some of the key areas I worked with include:

- Connecting a React frontend to a FastAPI backend.
- Designing REST APIs and validating structured data.
- Working with SQLite for persistent storage.
- Exploring browser automation with Browser Use and Playwright.
- Integrating n8n workflows with backend services.
- Handling duplicate records and preserving opportunity statuses.
- Testing backend functionality and deploying a full-stack application on Render.

This project helped me understand how different technologies can work together to build something more practical than a standalone web application.

## About the Project

Opportunity Hunter AI is a personal project built as part of my journey as a Computer Science student. I'm interested in exploring how AI agents and automation can solve everyday problems, especially when it comes to making career opportunities easier to discover.

Feedback and suggestions are always welcome!

---

Built with curiosity, code, and a lot of learning along the way.
