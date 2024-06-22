ACTIVATION_PHRASES = ["hey landslide", "landslide", "hey land slide", "land slide", "hey land", "land"]

# CUDA Devices
LIVE_AUDIO_DEVICE = "cpu"
TRANSCRIPTION_DEVICE = "cuda:1"
TTS_DEVICE = "cuda:1"

# LLM Endpoints

LOCAL_LLM_URL = "http://localhost:11434/v1"

#LOCAL_LLM_URL_2 = "http://tsunami:11434/v1" # This is the URL for the second LLM service

# Webserver

WEB_SERVER_URL = "landslide:8011"

# Redis

REDIS_HOST = "landslide"
REDIS_PORT = "6379"
REDIS_URL = "landslide:6379"
REDIS_USERNAME = "redis_username"
REDIS_PASSWORD = "redis_password"
REDIS_DB = 0

LIVE_AUDIO_QUEUE = "live_transcription"
SPEECH_TO_TEXT_QUEUE = "speech_to_text"
TEXT_TO_SPEECH_QUEUE = "text_to_speech"
