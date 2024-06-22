from pydantic import BaseModel
from typing import Literal
import time

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    time_created: float = time.time()


    def as_oai_message(self):
        return {
            "role": self.role,
            "content": self.content,
        }
