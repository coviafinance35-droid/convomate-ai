from typing import Literal, Optional, List
from pydantic import BaseModel, Field

class SessionCreate(BaseModel):
    summary: str = Field(min_length=12, max_length=6000)
    who: Optional[str] = Field(default=None, max_length=80)
    relationship: Optional[str] = Field(default=None, max_length=300)
    tone: str = Field(default="Natural", max_length=50)
    goal: Optional[str] = Field(default=None, max_length=240)

class SessionUpdate(BaseModel):
    summary: Optional[str] = Field(default=None, min_length=12, max_length=6000)
    who: Optional[str] = Field(default=None, max_length=80)
    relationship: Optional[str] = Field(default=None, max_length=300)
    tone: Optional[str] = Field(default=None, max_length=50)
    goal: Optional[str] = Field(default=None, max_length=240)

class GenerationRequest(BaseModel):
    session_id: str
    incoming_message: Optional[str] = Field(default=None, max_length=4000)
    intention: Optional[str] = Field(default=None, max_length=2000)
    tone: Optional[str] = Field(default=None, max_length=50)
    instruction: Optional[str] = Field(default=None, max_length=500)

class AskRequest(BaseModel):
    session_id: Optional[str] = None
    question: str = Field(min_length=2, max_length=4000)

class ReviseRequest(BaseModel):
    session_id: str
    draft: str = Field(min_length=1, max_length=4000)
    instruction: str = Field(min_length=2, max_length=500)

class ReplyResult(BaseModel):
    primary_reply: str
    alternatives: List[str] = []
    tone: str
    short_explanation: Optional[str] = None
    draft_id: Optional[str] = None

class TopicResult(BaseModel):
    suggested_message: str
    rationale: str
    follow_up_question: Optional[str] = None
    alternative_topic: str
    draft_id: Optional[str] = None

class AdviceResult(BaseModel):
    answer: str
    practical_options: List[str] = []
    relevant_caveats: List[str] = []
    optional_next_action: Optional[str] = None

class ChatMessage(BaseModel):
    role: Literal['user','assistant']
    content: str

class SessionOut(BaseModel):
    id: str
    title: str
    summary: str
    who: Optional[str]
    relationship: Optional[str]
    tone: str
    goal: Optional[str]
    created_at: str
    updated_at: str
