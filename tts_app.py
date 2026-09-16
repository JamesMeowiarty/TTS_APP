import os
import pyaudio
#import string

from glob import glob
from os import path
from piper.voice import PiperVoice

class TTS_APP():
    def __init__(self):
        self.update_voices()
        self.voice = None
        self.prev_voice = None

        # special handling to drop warnings when running PyAudio on Linux
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        try:
            os.dup2(devnull, 2)
            self.py_audio = pyaudio.PyAudio()
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            os.close(devnull)

    def get_audio_devices(self):
        # special handling to drop warnings when running PyAudio on Linux
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        try:
            os.dup2(devnull, 2)
            p = pyaudio.PyAudio()
        finally:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            os.close(devnull)

        info = p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        audio_devices = {}
        for i in range(0, numdevices):
            if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
                audio_devices[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i
        return audio_devices    

    def get_voices(self):
        return self.available_models

    def update_voices(self):
        self.available_models = [path.basename(x) for x in glob(path.join('Voices', '*.onnx'))]

    def play_tts(self, text, voice, audio_output_index):
        if voice != self.voice:
            self.voice = PiperVoice.load(path.join('Voices', voice))
            self.prev_voice = voice
        chunks = self.voice.synthesize(text)
        first_chunk = next(chunks)

        stream = self.py_audio.open( # Open audio stream with correct settings
            format=self.py_audio.get_format_from_width(first_chunk.sample_width),
            channels=first_chunk.sample_channels,
            rate=first_chunk.sample_rate,
            output=True,
            output_device_index=audio_output_index
        )

        stream.write(first_chunk.audio_int16_bytes)

        for chunk in chunks:
            stream.write(chunk.audio_int16_bytes)

        stream.stop_stream()
        stream.close()