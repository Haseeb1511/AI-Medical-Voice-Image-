import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO


import logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)


def record_audio(file_path):
    """This function recognize the audio and convert it mp3 format and then save it to specified file path"""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("adjusting the ambient noise")
            recognizer.adjust_for_ambient_noise(source,duration=1)
            logging.info("start speaking now....")

            audio = recognizer.listen(source=source,timeout=12)
            logging.info("Recording completed")

             # Convert WAV bytes to AudioSegment
            wav_data = audio.get_wav_data()
            audio_segment = AudioSegment.from_file(BytesIO(wav_data),format="wav")

            # Export as mp3
            audio_segment.export(file_path,format="mp3",bitrate="128k")
            logging.info(f"Audio File saved to {file_path}")

    except Exception as e:
        logging.error(f"Error occured: {e}")
    return file_path

record_audio("haseeb.mp3")
