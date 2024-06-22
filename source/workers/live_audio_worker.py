"""
Detects voice data and moves audio requests to the live queue
"""
import tempfile
import os
import asyncio
from asyncio import subprocess
import torchaudio
import torch
from pydub import AudioSegment
import time
import redis

from setup import LIVE_AUDIO_CUDA_DEVICE
from utils.redis import add_to_queue, get_from_queue, get_queue_length

device = torch.device(LIVE_AUDIO_CUDA_DEVICE)
vad_model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad')
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils

def _is_speech_present(wav_file_path, min_speech_duration=0.2):
    # Load the WAV file
    wav, sample_rate = torchaudio.load(wav_file_path)
    timestamps = get_speech_timestamps(wav, vad_model, sampling_rate=sample_rate)
    print(f"sample_rate: {sample_rate}")
    total_speech_duration = 0
    for timestamp in timestamps:
        total_speech_duration += (timestamp['end'] - timestamp['start']) / sample_rate

    print(f"Total speech duration: {total_speech_duration} seconds")
    return total_speech_duration >= min_speech_duration

def detect_and_concatinate_audio(webm_file_location, working_directory, current_concatenated_audio = None):
        """
        updates the current_concatenated_audio with the audio from the webm file if speech is detected
        if no speech is detected (user done speaking), sends the current_concatenated_audio to the transcription queue
        """
        wav_file_location = f"{working_directory}/audio.wav"
        # Convert webm to wav
        os.system(f"ffmpeg -i {webm_file_location} {wav_file_location}")
        os.system.remove(webm_file_location)
        
        if _is_speech_present(wav_file_location):
            if current_concatenated_audio is None:
                    current_concatenated_audio = AudioSegment.from_wav(wav_file_location)
            else:
                current_concatenated_audio += AudioSegment.from_wav(wav_file_location)
        else:
            if current_concatenated_audio is not None:
                output_filename = f"{time.now()}.wav"
                current_concatenated_audio.export(f"./data/needs_transcription/{output_filename}", format="wav")
                add_to_queue("speech_to_text", f"./data/transcription_files/{time.now()}.wav")
                current_concatenated_audio = None
            else:
                 pass # current audio is none, and no speech detected, do nothing
        return current_concatenated_audio

def main():
     current_concatenated_audio = None
     with tempfile.TemporaryDirectory() as temp_dir:
        while True:
            if get_queue_length("live_audio") > 0:
                webm_file_location = get_from_queue("live_audio")
                current_concatenated_audio = detect_and_concatinate_audio(webm_file_location, temp_dir, current_concatenated_audio)
            else:
                time.sleep(0.1)

if __name__ == "__main__":
     main()