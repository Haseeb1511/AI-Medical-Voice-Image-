from dotenv import load_dotenv
load_dotenv()
from groq import Groq



audio_path = "output.mp3"
client = Groq()
model_stt = "whisper-large-v3-turbo"
audio_file = open(audio_path,"rb")

transcription = client.audio.transcriptions.create(
    model=model_stt,
    file = audio_file,
    language="en"
    )
print(transcription.text)