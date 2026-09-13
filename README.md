# TTS_APP

## Installing
- Install Python
    - https://www.python.org/
    - Click Download and select your Operating System (NOTE: Latest version should work, but was tested with 3.14 and 3.12)
    - Install Python (NOTE: For Windows you can use https://www.pythonguis.com/installation/install-tkinter-windows/ as a Guide)

- Install Application Dependicies
    - Open a Terminal and navigate to the Application directory
    - Run "pip install -r requirements.txt"
    - Download a Voice into the Voices Folder
        - Samples and Voices can be found at https://rhasspy.github.io/piper-samples/
        - Click the "Download" Link on the chosen voice
        - Download both the .onnx and .json files to the Voices directory in the application

## Running the Application
- Running the Application
    - Open a Terminal and navigate to the Application directory
    - run "python main.py"
    - A GUI should pop up

## Usage
- Usage
    - Choose an output device for the TTS to play through
    - Choose a voice for the TTS
    - Enter the text you wish to play
    - Click "Play TTS"

## Setting up a Live2D Model to mouth the TTS
- Having VTube model "mouth" the TTS
    - Recommended: Install VB-CABLE Virtual Audio Device
        - https://vb-audio.com/Cable/
        - This creates a fake Audio device which the application can interface with and the output can be added to VTube Studio and OBS
    - Open VTube Studio
        - Recommende: I recommend making a copy of the model before making changes. This way your have your normal mode and a TTS model
        - Click "Settings"
        - Scroll down to "Microphone Settings" and click "Use microphone
        - Select "Microphone" and choose either your Microphone or "CABLE In 16 Ch (VB-Audio Virtua" if you installed VB-CABLE)"
        - Click "Model Settings"
        - Find the "Mouth Smile" setting (This may not be the exact name as the rigger can choose any name)
        - Change the Input to "VoiceFrequency"
        - Find the "Mouth Open" setting (This may not be the exact name as the rigger can choose any name)
        - Change the Input to "VoiceVolume"