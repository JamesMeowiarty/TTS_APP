import tkinter as tk

from tkinter import ttk, messagebox
from tts_app import TTS_APP
from tts_config import TTS_CONFIG


class GUI_INTERFACE():
    def __init__(self):
        self.tts_app = TTS_APP()
        self.tts_config = TTS_CONFIG()
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
        if self.tts_app.play_tts(text, self.combobox_piper_voice.get(), self.audio_devices[self.combobox_audio_output.get()]):
            self.text_text_box.delete('1.0', tk.END)
        else:
            messagebox.showerror("ERROR", "Can't play audio through selected device.\nPlaease select a different audio device")
            pass

    def refresh_piper(self):
        self.tts_app.update_voices()
        piper_voices = self.tts_app.get_voices()
        self.combobox_piper_voice['values'] = piper_voices
        if len(piper_voices) > 0:
            try:
                self.combobox_piper_voice.current(piper_voices.index(self.tts_config.get_tts_voice()))
            except ValueError:
                self.combobox_piper_voice.current(0)

    def refresh_audio(self):
        audio_outputs = self.tts_app.get_audio_devices()
        self.combobox_audio_output['values'] = list(audio_outputs.keys())
        try:
            self.combobox_audio_output.current(list(self.audio_devices.keys()).index(self.tts_config.get_audio_device()))
        except ValueError:
            self.combobox_audio_output.current(0)

    def on_close(self):
        self.tts_config.update_config(self.combobox_audio_output.get(), self.combobox_piper_voice.get())
        self.root.destroy()

    def create_gui(self):
        self.root = tk.Tk()
        self.root.title("TTS Player")
        self.root.geometry("500x250")

        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)

        ttk.Label(self.root, text="Audio Outout").grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.combobox_audio_output = ttk.Combobox(self.root, values=list(self.audio_devices.keys()), state="readonly")
        self.refresh_audio()
        self.combobox_audio_output.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        button_audio_refresh = tk.Button(self.root, text="Refresh", command=self.refresh_audio)
        button_audio_refresh.grid(row=0, column=2, pady=10, sticky="ew")

        ttk.Label(self.root, text="Piper TTS Voice").grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.combobox_piper_voice = ttk.Combobox(self.root, state="readonly")
        self.refresh_piper()
        self.combobox_piper_voice.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        button_piper_refresh = tk.Button(self.root, text="Refresh", command=self.refresh_piper)
        button_piper_refresh.grid(row=1, column=2, pady=10, sticky="ew")

        self.text_text_box = tk.Text(self.root, height=5, wrap="word")
        self.text_text_box.grid(row=2, column=0, columnspan=3, padx=10, pady=10,sticky="nsew")

        button_play = ttk.Button(self.root, text="Play TTS", command=self.play_tts)
        button_play.grid(row=3, column=1, padx=10, pady=10, sticky="e")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.root.mainloop()

if __name__ == '__main__':
    a = GUI_INTERFACE()