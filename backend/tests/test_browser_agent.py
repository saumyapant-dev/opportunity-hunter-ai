"""Tests for Browser Use agent integration, schema validation, and mock research engine."""
import unittest
import asyncio
from datetime import datetime

from backend.app.models.opportunity import (
    ResearchRequest,
    Opportunity,
    OpportunityType,
    OpportunityStatus,
    VerificationStatus,
    OpportunityListOutput,
    ExtractedOpportunity,
)
from backend.app.agents.browser_researcher import (
    _generate_mock_opportunities,
    execute_research,
    get_llm_status,
    get_browser_status,
)


class TestBrowserResearcher(unittest.TestCase):
    def test_01_schema_conformance(self):
        """Verify that ExtractedOpportunity and OpportunityListOutput models validate properly."""
        extracted = ExtractedOpportunity(
            title="Software Engineering Intern",
            organization="Tech Pioneers",
            type="internship",
            description="Summer software engineering internship program.",
            required_skills=["Python", "React"],
            location="Remote",
            remote=True,
            deadline=None,  # Null deadline allowed and required when missing
            application_url="https://techpioneers.com/apply/intern",
            source_url="https://techpioneers.com/careers",
            verification_status="verified",
        )
        output = OpportunityListOutput(opportunities=[extracted])
        self.assertEqual(len(output.opportunities), 1)
        self.assertIsNone(output.opportunities[0].deadline)
        self.assertEqual(output.opportunities[0].title, "Software Engineering Intern")

    def test_02_mock_research_generation(self):
        """Verify that mock generator accurately mirrors user search criteria and produces valid opportunities."""
        req = ResearchRequest(
            skills=["Machine Learning", "Python"],
            opportunity_types=["research", "hackathon"],
            location="Remote",
            experience="Intermediate",
            max_results=4,
            mode="mock",
        )
        results = _generate_mock_opportunities(req)
        self.assertLessEqual(len(results), 4)
        self.assertGreater(len(results), 0)

        for opp in results:
            self.assertIsInstance(opp, Opportunity)
            self.assertIn(opp.type, [OpportunityType.RESEARCH, OpportunityType.HACKATHON])
            self.assertTrue(opp.application_url.startswith("http"))
            self.assertTrue(opp.source_url.startswith("http"))
            # Verification status should be unverified for mock
            self.assertEqual(opp.verification_status, VerificationStatus.UNVERIFIED)
            self.assertTrue("[MOCK RESEARCH RESULT]" in opp.description)

    def test_03_execute_research_mock_mode_async(self):
        """Verify execute_research correctly executes asynchronously in mock mode."""
        req = ResearchRequest(
            skills=["React", "TypeScript"],
            opportunity_types=["internship"],
            location="Remote",
            max_results=3,
            mode="mock",
        )
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(execute_research(req))
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].type, OpportunityType.INTERNSHIP)
        finally:
            loop.close()

    def test_04_status_diagnostics(self):
        """Verify that LLM and Browser status checks report accurate metadata without leaking secrets."""
        llm_stat = get_llm_status()
        self.assertIn("provider", llm_stat)
        self.assertIn("configured", llm_stat)
        self.assertIn("model", llm_stat)
        self.assertNotIn("api_key", llm_stat)

        browser_stat = get_browser_status()
        self.assertIn("browser_engine", browser_stat)
        self.assertIn("headless", browser_stat)
        self.assertIn("available", browser_stat)


if __name__ == "__main__":
    unittest.main()
