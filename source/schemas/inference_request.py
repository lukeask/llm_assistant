from pydantic import BaseModel
from typing import List, Literal
from schemas.messages import Message


class InferenceRequest(BaseModel):
    model: Literal["openai", "command-r", "llama3-8b", "phi3" ]
    messages: List[Message]