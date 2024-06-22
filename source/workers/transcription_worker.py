"""
When there is audio in the transcription queue, the transcription worker will transcribe the audio and add the transcription to the unanswered_user_messages queue.
"""
import torch
import whisper
import time

from utils.redis import add_to_queue, get_from_queue, get_queue_length
from setup import TRANSCRIPTION_DEVICE
from schemas.unanswered_user_message import UnansweredUserMessage

device = torch.device(TRANSCRIPTION_DEVICE)

transcription_model = whisper.load_model("medium.en", device=device)
def transcribe_audio(wav_file_path):
    result = transcription_model.transcribe(wav_file_path, prompt = "Squirrel")
    return result["text"]

def main():
    while True:
        if get_queue_length("speech_to_text") > 0:
            wav_file_path = get_from_queue("speech_to_text")
            transcription = transcribe_audio(wav_file_path)
            new_user_message = UnansweredUserMessage(source="live_audio", text=transcription)
            add_to_queue("unanswered_user_messages", new_user_message.dict())
        else:
            time.sleep(0.1)