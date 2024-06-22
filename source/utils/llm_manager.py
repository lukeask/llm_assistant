from openai import OpenAI
from pydantic import BaseModel
from typing import List, Literal
from schemas.inference_request import InferenceRequest
from schemas.messages import Message
from setup import LOCAL_LLM_URL


OAI_API_KEY = "sk-"

def _get_openai_completion(self, messages: List[str]) -> str:
    raise NotImplementedError

def _get_command_r_completion(self, messages) -> Message:
    landslide_ollama_client = OpenAI(api_key="ollama", base_url = LOCAL_LLM_URL )
    response = landslide_ollama_client.chat.completions.create(
        model="command-r",
        messages=[message.as_oai_message() for message in messages],
    )
    return Message(content= response.choices[0].message.content, role = response.choices[0].message.role)

def _get_llama3_8b_completion(self, messages: List[str]) -> str:
    raise NotImplementedError

def _get_phi3_completion(self, messages: List[str]) -> str:
    raise NotImplementedError

def get_llm_completion(llm_request = InferenceRequest) -> Message:
    if llm_request.model == "openai":
        return _get_openai_completion(llm_request.messages)

    if llm_request.model == "command-r":
        return _get_command_r_completion(llm_request.messages)
    
    if llm_request.model == "llama3-8b":
        return _get_llama3_8b_completion(llm_request.messages)
    
    if llm_request.model == "phi3":
        return _get_phi3_completion(llm_request.messages)


