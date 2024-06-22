from Pydantic import BaseModel
import time
from typing import Literal
from schemas.messages import Message

class UnansweredUserMessage(BaseModel):
    source: Literal["live_audio", "web_interface", "written"]
    text: str
    time_created: float = time.time()

    def as_oai_message(self):
        return {
            "role": "user",
            "content": self.text,
        }

    def as_message(self):
        return Message(role="user", content=self.text, time_created=self.time_created)