import time
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import SpeechRecognitionEventArgs
from multiprocessing import Queue

from log.config_log import logger


def speech_to_text_continuous(message_queue: Queue, api_key: str, speech_region: str):
    """
    Converts speech to text non-stop
    Documentation: https://learn.microsoft.com/en-gb/azure/ai-services/speech-service/how-to-recognize-speech?pivots=programming-language-python

    This section will need some changes fo you to solve the challenges
    This logic is called by spawning a sub-process from the main game view.
    The main process and this speech recognition process communicate in a one-way manner using Queues.
    The Speech recognition process can send message to the queue which can be then retrieved by the main process.
    """
    done = False

    def stop_cb(evt):
        logger.info(f'CLOSING on {evt}')
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

    def recognized_speech(event: SpeechRecognitionEventArgs):
        logger.info(f"Recognized: {event.result.text}")

        if "Hello World" in event.result.text.lower():
            logger.info("hello world")
            message_queue.put("hello world")

    # Init engine
    speech_config = speechsdk.SpeechConfig(subscription=api_key, region=speech_region)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Define Callbacks
    speech_recognizer.recognizing.connect(lambda evt: logger.info(f'RECOGNIZING: {evt.result.text}'))
    speech_recognizer.recognized.connect(recognized_speech)

    speech_recognizer.session_started.connect(lambda evt: logger.info(f'SESSION STARTED: {evt}'))
    speech_recognizer.session_stopped.connect(lambda evt: logger.info(f'SESSION STOPPED {evt}'))
    speech_recognizer.canceled.connect(lambda evt: logger.info(f'CANCELED {evt}'))

    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    speech_recognizer.start_continuous_recognition()
    
    while not done:
        time.sleep(.5)
