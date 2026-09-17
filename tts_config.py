import yaml

CLASS_MEMEBERS = ['audio_device', 'tts_voice']
class TTS_CONFIG():
    def __init__(self):
        self.initialized = False
        self.audio_device = None
        self.tts_voice = None
        self._initialize_variables()

    def _initialize_variables(self):
        try:            
            with open('config.yaml', 'r') as file:
                service = yaml.safe_load(file)
                for key, value in service.items():
                    setattr(self, key, value)
        except FileNotFoundError:
            self.initialized = True

    def _write_config(self):
        config = {
            'audio_device': self.audio_device,
            'tts_voice': self.tts_voice
        }

        with open('config.yaml', 'w') as config_file:
            yaml.dump(config, config_file, default_flow_style=False)

    def get_audio_device(self):
        return self.audio_device

    def get_tts_voice(self):
        return self.tts_voice

    def update_config(self, audio_device, tts_voice):
        update = False
        if self.audio_device != audio_device or self.tts_voice != tts_voice:
            update = True
            self.audio_device = audio_device
            self.tts_voice = tts_voice
        if update:
            self._write_config()