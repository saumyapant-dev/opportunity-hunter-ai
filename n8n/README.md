# n8n Workflows for Opportunity Hunter AI

This folder contains pre-configured, importable workflow definitions for **n8n** that orchestrate Opportunity Hunter AI.

---

## Workflows Included

| File | Purpose | Trigger | Nodes Included |
|---|---|---|---|
| `workflows/manual_opportunity_discovery.json` | Manual on-demand research triggered from dashboard | Webhook (`POST /webhook/opportunity-research`) | Input Validation, Browser Agent HTTP, Deduplication, SQLite Storage, Webhook Response |
| `workflows/scheduled_opportunity_discovery.json` | Automated daily research loop | Schedule Trigger (`0 8 * * *` - 8:00 AM daily) | Get Preferences, Browser Agent HTTP, Deduplication, Notification Router |
| `workflows/email_notifications.json` | Formatted responsive HTML email digest | Webhook (`POST /webhook/opportunity-notifications`) | Template Formatter, Send Email (SMTP / Gmail) |

---

## Quick Setup Instructions

### 1. Start n8n
If n8n is not already installed, launch it easily via npx:

```bash
npx n8n
```

Or via Docker:
```bash
docker run -it --rm --name n8n -p 5678:5678 -v ~/.n8n:/home/node/.n8n docker.n8n.io/n8nio/n8n
```

Access the n8n editor at `http://localhost:5678`.

### 2. Import Workflows into n8n

1. In the n8n left sidebar, click **Workflows**.
2. Click the **+ Add Workflow** button (top right).
3. Open the top-right menu (three dots `...`) and select **Import from File**.
4. Select each JSON file from `n8n/workflows/`:
   - `manual_opportunity_discovery.json`
   - `scheduled_opportunity_discovery.json`
   - `email_notifications.json`
5. Click **Save** and toggle the workflow to **Active** (green switch in top right).

---

### 3. Setting Up Email Credentials (Safe & Secure)

In n8n, credentials are managed through the encrypted Credential Store and are never hardcoded inside workflow JSON.

1. In n8n, navigate to **Credentials** -> **New Credential**.
2. Search for **SMTP** (or **Gmail OAuth2** / **SendGrid**).
3. Fill in your SMTP host, port, user, and app password.
4. Open the `Opportunity Hunter - Email Digest Notifications` workflow.
5. Click on the **Send Email** node, select your newly created SMTP credential, and save.

---

### 4. Testing the Webhooks Locally

Test the manual research webhook from your terminal:

```bash
curl -X POST http://localhost:5678/webhook/opportunity-research \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "React"],
    "opportunity_types": ["internship", "hackathon"],
    "location": "Remote",
    "experience": "Beginner",
    "max_results": 5,
    "mode": "mock"
  }'
```

Test the email notification webhook with simulated listings:

```bash
curl -X POST http://localhost:5678/webhook/opportunity-notifications \
  -H "Content-Type: application/json" \
  -d '{
    "recipient_email": "your-email@example.com",
    "new_count": 1,
    "opportunities": [
      {
        "title": "Machine Learning Research Intern",
        "organization": "OpenAI Frontiers",
        "type": "internship",
        "description": "Work on automated agent reasoning and evaluations.",
        "required_skills": ["Python", "PyTorch"],
        "location": "Remote",
        "deadline": "2026-11-15",
        "application_url": "https://careers.example.com/apply/ml-intern",
        "source_url": "https://careers.example.com"
      }
    ]
  }'
```
