import torch
import numpy as np
from kokoro import KPipeline
import sounddevice as sd
import speech_recognition as sr
import threading

torch.cuda.empty_cache()

kokoro_pipeline = KPipeline(lang_code="b")


def speak(text: str):
    """
    Function to convert text to speech using Kokoro.
    """
    generator = kokoro_pipeline(
        text=text,
        voice="af_bella",
        speed=1.3,
    )

    for i, (gs, ps, audio) in enumerate(generator):
        # sf.write(f"output_{i}.wav", audio, 22050)
        # display(Audio(audio, rate=22050, autoplay=i==0))
        sd.play(audio, samplerate=22050)
        sd.wait()


def listen(timeout=5):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=timeout)
    try:
        command = recognizer.recognize_google(audio).lower()
        print("Heard:", command)
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError as e:
        return f"[Error: {e}]"


def wait_for_command_or_timeout(duration):
    response = None

    def listen_thread():
        nonlocal response
        while not response:
            cmd = listen(timeout=duration)
            if cmd in ["next", "skip", "pause", "repeat", "stop"]:
                response = cmd

    t = threading.Thread(target=listen_thread)
    t.start()
    t.join(timeout=duration)
    return response or "next"
