"""Unit and integration tests for Opportunity Hunter FastAPI endpoints."""
import os
import unittest
import tempfile
import uuid
from pathlib import Path
from starlette.testclient import TestClient

# Use isolated temp database for tests
temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
temp_db_path = temp_db.name
temp_db.close()
os.environ["DATABASE_PATH"] = temp_db_path
os.environ["LLM_PROVIDER"] = "mock"

from backend.app.main import app
from backend.app.database.db import (
    init_db,
    save_opportunity,
    get_opportunity,
    list_opportunities,
    find_duplicate,
)
from backend.app.models.opportunity import (
    Opportunity,
    OpportunityType,
    OpportunityStatus,
    VerificationStatus,
)
from backend.app.services.deduplication import normalize_url, process_and_deduplicate_opportunities


class TestOpportunityHunterAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(temp_db_path):
            try:
                os.remove(temp_db_path)
            except Exception:
                pass

    def test_01_health_check(self):
        """Verify the health check endpoint returns 200 OK and healthy status."""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "opportunity-hunter-backend")

    def test_02_workflow_status(self):
        """Verify the system diagnostics and workflow status endpoint."""
        resp = self.client.get("/api/workflows/status")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("n8n", data)
        self.assertIn("browser_agent", data)
        self.assertIn("llm", data)
        self.assertIn("system", data)

    def test_03_url_normalization(self):
        """Verify tracking parameters and formatting are stripped correctly."""
        raw_url = "https://www.company.com/jobs/ai-intern/?utm_source=twitter&utm_medium=social&ref=camp#overview"
        normalized = normalize_url(raw_url)
        self.assertEqual(normalized, "https://www.company.com/jobs/ai-intern")

        # Port normalization
        port_url = "http://localhost:80/path/?b=2&a=1"
        self.assertEqual(normalize_url(port_url), "http://localhost/path?a=1&b=2")

    def test_04_deduplication_engine(self):
        """Verify that duplicate opportunities are identified and do not clobber user status."""
        opp1 = Opportunity(
            id=str(uuid.uuid4()),
            title="Frontend Engineering Intern",
            organization="Acme Innovations",
            type=OpportunityType.INTERNSHIP,
            description="Build web applications.",
            required_skills=["React", "TypeScript"],
            location="Remote",
            remote=True,
            application_url="https://acme.io/careers/eng-intern?utm_source=linkedin",
            source_url="https://acme.io/careers",
            status=OpportunityStatus.APPLIED,  # User applied!
            verification_status=VerificationStatus.VERIFIED,
        )
        saved_items, new_count, dup_count = process_and_deduplicate_opportunities([opp1])
        self.assertEqual(new_count, 1)
        self.assertEqual(dup_count, 0)

        # Re-encounter same opportunity via different tracking URL
        opp2 = Opportunity(
            id=str(uuid.uuid4()),
            title="Frontend Engineering Intern",
            organization="Acme Innovations",
            type=OpportunityType.INTERNSHIP,
            description="Updated description of the internship.",
            required_skills=["React"],
            location="Remote",
            remote=True,
            application_url="https://acme.io/careers/eng-intern?ref=newsletter",
            source_url="https://acme.io/careers",
            status=OpportunityStatus.NEW,
            verification_status=VerificationStatus.VERIFIED,
        )
        saved_items2, new_count2, dup_count2 = process_and_deduplicate_opportunities([opp2])
        self.assertEqual(dup_count2, 1)
        self.assertEqual(new_count2, 0)

        # Check that user's APPLIED status was preserved
        persisted = get_opportunity(opp1.id)
        self.assertIsNotNone(persisted)
        self.assertEqual(persisted.status, OpportunityStatus.APPLIED)

    def test_05_research_request_validation(self):
        """Verify input validation rejecting out-of-range parameters."""
        # max_results exceeds allowable range
        invalid_payload = {
            "skills": ["Python"],
            "opportunity_types": ["internship"],
            "max_results": 100,  # Max is 50
        }
        resp = self.client.post("/api/research", json=invalid_payload)
        self.assertEqual(resp.status_code, 422)

    def test_06_trigger_research_mock_mode(self):
        """Verify triggering research creates a run and returns 202 with run_id."""
        valid_payload = {
            "skills": ["Python", "React"],
            "opportunity_types": ["internship", "hackathon"],
            "location": "Remote",
            "experience": "Beginner",
            "max_results": 5,
            "mode": "mock",
        }
        resp = self.client.post("/api/research", json=valid_payload)
        self.assertEqual(resp.status_code, 202)
        data = resp.json()
        self.assertIn("run_id", data)
        self.assertEqual(data["mode"], "mock")

        # Verify run can be fetched
        run_id = data["run_id"]
        run_resp = self.client.get(f"/api/research/{run_id}")
        self.assertEqual(run_resp.status_code, 200)
        run_data = run_resp.json()
        self.assertEqual(run_data["id"], run_id)

    def test_07_n8n_webhook_results_receiver(self):
        """Verify that n8n webhook results receiver saves opportunities and updates run."""
        fake_run_id = str(uuid.uuid4())
        webhook_payload = {
            "run_id": fake_run_id,
            "status": "completed",
            "opportunities": [
                {
                    "title": "Quantum Algorithm Hackathon",
                    "organization": "Quantum Hub",
                    "type": "hackathon",
                    "description": "Compete to solve optimization problems.",
                    "required_skills": ["Python", "Linear Algebra"],
                    "location": "Remote",
                    "remote": True,
                    "deadline": "2026-12-01",
                    "application_url": "https://quantumhub.org/hackathon-2026",
                    "source_url": "https://quantumhub.org",
                    "verification_status": "verified",
                }
            ],
        }
        resp = self.client.post("/api/webhooks/n8n/results", json=webhook_payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["processed_count"], 1)

    def test_08_opportunities_crud(self):
        """Verify listing, updating status, and deleting opportunities."""
        # List opportunities
        resp = self.client.get("/api/opportunities")
        self.assertEqual(resp.status_code, 200)
        items = resp.json()
        self.assertIsInstance(items, list)
        self.assertGreater(len(items), 0)

        target_id = items[0]["id"]

        # Update status to 'saved'
        patch_resp = self.client.patch(
            f"/api/opportunities/{target_id}",
            json={"status": "saved"},
        )
        self.assertEqual(patch_resp.status_code, 200)
        self.assertEqual(patch_resp.json()["status"], "saved")

        # Delete opportunity
        del_resp = self.client.delete(f"/api/opportunities/{target_id}")
        self.assertEqual(del_resp.status_code, 204)

        # Confirm deleted
        get_resp = self.client.get(f"/api/opportunities/{target_id}")
        self.assertEqual(get_resp.status_code, 404)

    def test_09_user_preferences(self):
        """Verify getting and updating user preferences."""
        resp = self.client.get("/api/preferences")
        self.assertEqual(resp.status_code, 200)
        prefs = resp.json()
        self.assertIn("skills", prefs)

        prefs["skills"] = ["Rust", "Go", "Kubernetes"]
        prefs["notification_email"] = "developer@test.com"

        put_resp = self.client.put("/api/preferences", json=prefs)
        self.assertEqual(put_resp.status_code, 200)
        updated_data = put_resp.json()
        self.assertEqual(updated_data["skills"], ["Rust", "Go", "Kubernetes"])
        self.assertEqual(updated_data["notification_email"], "developer@test.com")


if __name__ == "__main__":
    unittest.main()
