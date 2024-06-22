import time
import requests

from utils.redis import add_to_queue, get_from_queue, get_queue_length
from schemas.unanswered_user_message import UnansweredUserMessage
from schemas.inference_request import InferenceRequest
from message_templates.chat_template import FORMAT_CHAT_TEMPLATE
from setup import activation_phrases, WEB_SERVER_URL
from utils.llm_manager import get_llm_completion
from data.sql import message_db

def handle_user_message(user_message: UnansweredUserMessage):
    """
    The logic to handle the user message is as follows:
    - If the user message came from live_audio, determine if user was even talking to the bot
    TODO - If the source of the user message is live_audio or web_interface, the user is using the web client so has client info
    TODO - another process is constantly assembling good context to include with llm completion queries when there is client info, so we request that information

    """
    if user_message.source == "live_audio":
        # determine if user was even talking to the bot
        if any (phrase in user_message.text.lower() for phrase in activation_phrases):
            pass
        else:
            return "User was not talking to the bot. Ignoring message."

    message_db.add_message(user_message.as_message())

    if user_message.source == "live_audio" or user_message.source == "web_interface":
        # get current_web_interface info
        # if viewing document, add document to immediate_context_string
    
        # TODO
        pass

    # TODO, add rag context to  system messagee

    system_message = FORMAT_CHAT_TEMPLATE()
    # TEMPORARY

    inference_request = InferenceRequest(model="command-r", messages=[system_message, user_message.as_message()])
    assistant_message = get_llm_completion(inference_request)

    message_db.add_message(assistant_message)

    if user_message.source == "live_audio":
        # add the llm message to the live_audio queue
        add_to_queue("text_to_speech", assistant_message.text)

    



def main():
    while True:
        if get_queue_length("unanswered_user_messages") > 0:
            user_message = get_from_queue("unanswered_user_messages")
            user_message = UnansweredUserMessage(user_message)
            handle_user_message(user_message)
        else:
            time.sleep(0.1)

if __name__ == "__main__":
    main()