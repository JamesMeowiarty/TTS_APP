import tkinter as tk
import os

from tkinter import ttk
from tts_app import TTS_APP


class GUI_INTERFACE():
    def __init__(self):
        self.tts_app = TTS_APP()
        self.audio_devices = None
        self.get_audio_devices()
        self.create_gui()

    def get_audio_devices(self):
        self.audio_devices = self.tts_app.get_audio_devices()

    def play_tts(self):
        text = self.text_text_box.get('1.0', 'end-1c')
        if text.strip() == "":
            # Clears Text Box since the box may be filled with spaces or tabs
            self.text_text_box.delete('1.0', tk.END)
            return
        self.tts_app.play_tts(text, self.combobox_piper_voice.get(), self.audio_devices[self.combobox_audio_output.get()])
        self.text_text_box.delete('1.0', tk.END)

    def refresh_piper(self):
        self.tts_app.update_voices()
        piper_voices = self.tts_app.get_voices()
        self.combobox_piper_voice['values'] = piper_voices
        if len(piper_voices) > 0:
            self.combobox_piper_voice.current(0)

    def refresh_audio(self):
        audio_outputs = self.tts_app.get_audio_devices()
        self.combobox_audio_output['values'] = list(audio_outputs.keys())
        try:
            self.combobox_audio_output.current(list(self.audio_devices.keys()).index('default'))
        except ValueError:
            self.combobox_audio_output.current(0)

    def create_gui(self):
        root = tk.Tk()
        root.title("TTS Player")
        root.geometry("500x250")

        root.columnconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)

        ttk.Label(root, text="Audio Outout").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.combobox_audio_output = ttk.Combobox(root, values=list(self.audio_devices.keys()), state="readonly")
        self.refresh_audio()
        self.combobox_audio_output.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        button_audio_refresh = tk.Button(root, text="Refresh", command=self.refresh_audio)
        button_audio_refresh.grid(row=0, column=2, pady=10, sticky="ew")

        ttk.Label(root, text="Piper TTS Voice").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        piper_voices = self.tts_app.get_voices()
        self.combobox_piper_voice = ttk.Combobox(root, values=piper_voices, state="readonly")
        if len(piper_voices) > 0:
            self.combobox_piper_voice.current(0)
        self.combobox_piper_voice.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        button_piper_refresh = tk.Button(root, text="Refresh", command=self.refresh_piper)
        button_piper_refresh.grid(row=1, column=2, pady=10, sticky="ew")

        self.text_text_box = tk.Text(root, height=5, wrap="word")
        self.text_text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")

        button_play = ttk.Button(root, text="Play TTS", command=self.play_tts)
        button_play.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        root.mainloop()

if __name__ == '__main__':
    a = GUI_INTERFACE()