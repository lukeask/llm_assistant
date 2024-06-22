from utils import REDIS_HOST, REDIS_DB, REDIS_PORT, LIVE_AUDIO_QUEUE, REDIS_PASSWORD, REDIS_USERNAME, LIVE_AUDIO_QUEUE, SPEECH_TO_TEXT_QUEUE, TEXT_TO_SPEECH_QUEUE, CHAT_COMPLETION_QUEUE
import redis


db = redis(host = REDIS_HOST, port = REDIS_PORT, username=REDIS_USERNAME, password=REDIS_PASSWORD, decode_responses=True, db=REDIS_DB)

redis_queues = {
    "live_audio": LIVE_AUDIO_QUEUE,
    "speech_to_text": SPEECH_TO_TEXT_QUEUE,
    "text_to_speech": TEXT_TO_SPEECH_QUEUE,
    "chat_completion": CHAT_COMPLETION_QUEUE
}

def add_to_queue(queue_name, data):
    db.rpush(redis_queues[queue_name], data)

def get_from_queue(queue_name):
    return db.lpop(redis_queues[queue_name])

def get_queue_length(queue_name):
    return db.llen(redis_queues[queue_name])

