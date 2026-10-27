from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AssistantResponse(BaseModel):
    intent: str = Field(description="What the user wants to do")
    target: str | None = None
    message: str = Field(description="Short response to the user")


class AgentAction(BaseModel):
    tool: str
    action: str
    target: str | None = None
    risk_level: RiskLevel = RiskLevel.LOW


class PermissionResult(BaseModel):
    allowed: bool
    confirmation_required: bool
    message: str


class MemoryItem(BaseModel):
    category: str
    content: str

class EmailRequest(BaseModel):
    to_email: str
    subject: str
    body: str