"""Pydantic data models for Opportunity Hunter AI."""
from enum import Enum
from typing import List, Optional, Any, Dict
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field, HttpUrl


class OpportunityType(str, Enum):
    INTERNSHIP = "internship"
    HACKATHON = "hackathon"
    RESEARCH = "research"
    JOB = "job"


class OpportunityStatus(str, Enum):
    NEW = "new"
    SAVED = "saved"
    INTERESTED = "interested"
    APPLIED = "applied"
    REJECTED = "rejected"


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"


class OpportunityBase(BaseModel):
    title: str = Field(..., description="Title of the role, competition, or position")
    organization: str = Field(..., description="Company, lab, or organizing entity")
    type: OpportunityType = Field(default=OpportunityType.INTERNSHIP, description="Category of the opportunity")
    description: str = Field(..., description="Summary of requirements, scope, and responsibilities")
    required_skills: List[str] = Field(default_factory=list, description="List of relevant skills, tools, or stacks")
    location: str = Field(default="Remote", description="Geographic location or Remote designation")
    remote: bool = Field(default=True, description="Whether the opportunity is remote/hybrid friendly")
    deadline: Optional[str] = Field(default=None, description="Application or submission deadline (ISO or text)")
    application_url: str = Field(..., description="Direct application or registration link")
    source_url: str = Field(..., description="Webpage where this opportunity was discovered")
    status: OpportunityStatus = Field(default=OpportunityStatus.NEW, description="Tracking status of the opportunity")
    verification_status: VerificationStatus = Field(default=VerificationStatus.UNVERIFIED, description="Verification confidence")


class OpportunityCreate(OpportunityBase):
    pass


class OpportunityUpdate(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    type: Optional[OpportunityType] = None
    description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    deadline: Optional[str] = None
    application_url: Optional[str] = None
    source_url: Optional[str] = None
    status: Optional[OpportunityStatus] = None
    verification_status: Optional[VerificationStatus] = None


class Opportunity(OpportunityBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    discovered_at: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class ResearchRunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchRequest(BaseModel):
    skills: List[str] = Field(default_factory=lambda: ["Python", "React"])
    opportunity_types: List[str] = Field(default_factory=lambda: ["internship", "hackathon"])
    location: str = Field(default="Remote")
    experience: str = Field(default="Beginner")
    keywords: List[str] = Field(default_factory=list)
    preferred_domains: List[str] = Field(default_factory=list)
    max_results: int = Field(default=10, ge=1, le=50)
    mode: str = Field(default="mock", description="'mock' for instant mock research, 'live' for real browser-use agent")


class ResearchRun(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: ResearchRunStatus = Field(default=ResearchRunStatus.PENDING)
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    results_count: int = 0
    error_message: Optional[str] = None
    mode: str = "mock"
    request_params: Optional[Dict[str, Any]] = None


class UserPreferences(BaseModel):
    id: str = "default"
    skills: List[str] = Field(default_factory=lambda: ["Python", "React", "JavaScript", "SQL"])
    opportunity_types: List[str] = Field(default_factory=lambda: ["internship", "hackathon", "entry-level job"])
    location: str = Field(default="Remote")
    experience: str = Field(default="Beginner")
    keywords: List[str] = Field(default_factory=lambda: ["AI", "Full Stack", "Data Science"])
    preferred_domains: List[str] = Field(
        default_factory=lambda: [
            "news.ycombinator.com",
            "devpost.com",
            "github.com",
            "wellfound.com",
            "internshala.com"
        ]
    )
    max_results: int = Field(default=10, ge=1, le=50)
    email_notifications_enabled: bool = Field(default=False)
    notification_email: str = Field(default="student@example.com")
    cron_schedule: str = Field(default="0 8 * * *")
    llm_provider: str = Field(default="openrouter")
    llm_model: str = Field(default="meta-llama/llama-3.3-70b-instruct")
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# Structured output model used by Browser Use agent
class ExtractedOpportunity(BaseModel):
    title: str = Field(..., description="Specific opportunity or job/hackathon title")
    organization: str = Field(..., description="Organization, employer, or host name")
    type: str = Field(default="internship", description="One of: internship, hackathon, research, job")
    description: str = Field(..., description="Concise description of the opportunity and eligibility")
    required_skills: List[str] = Field(default_factory=list, description="Key skills or languages required")
    location: str = Field(default="Remote", description="Location or Remote")
    remote: bool = Field(default=True, description="True if remote or hybrid")
    deadline: Optional[str] = Field(default=None, description="Actual deadline if found, else null. Never invent deadlines.")
    application_url: str = Field(..., description="Direct application link or page link found on the website")
    source_url: str = Field(..., description="The URL of the listing page where this was found")
    verification_status: str = Field(default="verified", description="verified or unverified")


class OpportunityListOutput(BaseModel):
    opportunities: List[ExtractedOpportunity] = Field(
        default_factory=list,
        description="List of real extracted opportunities matching the query. Leave missing values as null."
    )
