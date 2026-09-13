import os
import pyaudio
import string
import tkinter as tk

from tkinter import ttk
from glob import glob
from os import path
from piper.voice import PiperVoice


class TTS_APP():
    def __init__(self):
        self.available_models = [path.basename(x) for x in glob(path.join('Voices', '*.onnx'))]
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

    def get_voices(self):
        return self.available_models

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


def get_audio_devices():
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
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            audio_devices[p.get_device_info_by_host_api_device_index(0, i).get('name')] = i
    return audio_devices

def play_tts():
    text = text_text_box.get('1.0', 'end-1c')
    if text.strip() == "":
        # Clears Text Box since the box may be filled with spaces or tabs
        text_text_box.delete('1.0', tk.END)
        return
    tts_app.play_tts(text, combobox_piper_voice.get(), audio_outputs[combobox_audio_output.get()])
    text_text_box.delete('1.0', tk.END)

if __name__ == '__main__':
    tts_app = TTS_APP()

    # Main window
    root = tk.Tk()
    root.title("TTS Player")
    root.geometry("500x250")

    # Make the second column expandable
    root.columnconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)

    ttk.Label(root, text="Audio Outout").grid(
        row=0, column=0, padx=10, pady=10, sticky="w"
    )

    audio_outputs = get_audio_devices()
    combobox_audio_output = ttk.Combobox(
        root,
        values=list(audio_outputs.keys()),
        state="readonly"
    )
    try:
        combobox_audio_output.current(list(audio_outputs.keys()).index('default'))
    except:
        combobox_audio_output.current(0)
    combobox_audio_output.grid(
        row=0, column=1, padx=10, pady=10, sticky="ew"
    )

    ttk.Label(root, text="Piper TTS Voice").grid(
        row=1, column=0, padx=10, pady=10, sticky="w"
    )

    piper_voices = tts_app.get_voices()
    combobox_piper_voice = ttk.Combobox(
        root,
        values=piper_voices,
        state="readonly"
    )
    combobox_piper_voice.current(0)
    combobox_piper_voice.grid(
        row=1, column=1, padx=10, pady=10, sticky="ew"
    )

    text_text_box = tk.Text(root, height=5, wrap="word")
    text_text_box.grid(
        row=2, column=0, columnspan=2,
        padx=10, pady=10,
        sticky="nsew"
    )

    button_play = ttk.Button(
        root,
        text="Play TTS",
        command=play_tts
    )
    button_play.grid(
        row=3, column=1,
        padx=10, pady=10,
        sticky="e"
    )

    root.mainloop()