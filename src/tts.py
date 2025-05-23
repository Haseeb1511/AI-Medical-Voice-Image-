import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
import subprocess
import platform


#-----------------------------------------------AutoPlayAudio------------------------------------------------------------------------------------
def play_audio(file_path):
    system = platform.system()

    try:
        if system == "Windows":
            subprocess.run([
                "powershell",
                "-c",
                f"(New-Object Media.SoundPlayer '{file_path}').PlaySync();"
            ])
        elif system == "Darwin":
            subprocess.run(['afplay', file_path], check=True)
        elif system == "Linux":
            subprocess.run(['mpg123', file_path], check=True)
        else:
            print("Unsupported OS.")
    except Exception as e:
        print(f"Error: {e}")

#--------------------------------------------------------gTTS-----------------------------------------------------------------------------

def text_to_speech_gtts(input_text,file_path):
    audioobj = gTTS(
        text=input_text,
        lang="en",
        slow=False
    )
    audioobj.save(file_path)
    play_audio(file_path)


os.makedirs("ai_audio",exist_ok=True)   # create directory
input_text = "hi my name is haseeb manzoor and i am an AI engineer"  #input text
ai_save_path ="ai_audio/ai.mp3" 

text_to_speech_gtts(input_text=input_text,file_path=ai_save_path)

#-----------------------------------------ElevenLabs------------------------------------------------------------------------------------------

def text_to_speech_elevenlabs(input_text,file_path,auto_play_audio):
    client = ElevenLabs()
    audio = client.text_to_speech.convert(
        text=input_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_turbo_v2",
        output_format="mp3_44100_128"
    )
    with open(file_path,"wb") as f:  # model return generator thats why we save it chunk by chunk
        for chunk in audio:
            f.write(chunk)
    auto_play_audio(file_path)

ai_save_path_elevenlabs ="ai_audio/eleven_labs.mp3" 
text_to_speech_elevenlabs(input_text=input_text,file_path=ai_save_path_elevenlabs)
    
