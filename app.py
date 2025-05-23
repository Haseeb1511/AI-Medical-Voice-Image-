import streamlit as st
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
load_dotenv()
from groq import Groq
import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs
import speech_recognition as sr
from pydub import AudioSegment
import subprocess
import platform


os.makedirs("streamlit_audio",exist_ok=True)

def main():
    st.title("AI Doctor")
    uploaded_file = st.file_uploader("Upload your image here",type="JPEG")
    if uploaded_file is not None:
        uploaded_image = Image.open(uploaded_file)
        st.sidebar.image(uploaded_image,caption="User Uploaded Image")

        #-----------------------------------------Recording Audio------------------------------------------
        if uploaded_image:
            if st.button("Start Recording"):
                with st.spinner("Recording Audio"):
                    def record_audio(file_path):
                        """This function recognize the audio and convert it mp3 format and then save it to specified file path"""
                        recognizer = sr.Recognizer()
                        try:
                            with sr.Microphone() as source:
                                st.info("adjusting the ambient noise")
                                recognizer.adjust_for_ambient_noise(source,duration=1)
                                st.info("start speaking now....")

                                audio = recognizer.listen(source=source,timeout=10)
                                st.info("Recording completed")

                                # Convert WAV bytes to AudioSegment
                                wav_data = audio.get_wav_data()
                                audio_segment = AudioSegment.from_file(BytesIO(wav_data),format="wav")

                                # Export as mp3
                                audio_segment.export(file_path,format="mp3",bitrate="128k")
                                st.info(f"Audio File saved to {file_path}")
                        except Exception as e:
                            st.error(f"Error occured: {e}")

                    audio_path = "streamlit_audio/input_audio.mp3"
                    record_audio(audio_path)
    #------------------------------------Audio to Text----------------------------------------------------------------------------                
                client = Groq()
                model_stt = "whisper-large-v3-turbo"
                audio_file = open(audio_path,"rb")
                transcription = client.audio.transcriptions.create(
                            model=model_stt,
                            file = audio_file,
                            language="en"
                            )
                input_user_text = transcription.text
                st.sidebar.markdown(f"**User audio text:** {input_user_text}")
    #----------------------------------------------passing input to model ------------------------------------------------------
                def extract_text_from_image(image,format):
                    buffered = BytesIO()  # load in RAM
                    image.save(buffered,format=format)
                    image_base64 = base64.b64encode(buffered.getvalue()).decode()
                    return f"data:image/{format.lower()};base64,{image_base64}"
                        
                pic = extract_text_from_image(uploaded_image,format="JPEG")
                client = Groq() 
                model = "meta-llama/llama-4-scout-17b-16e-instruct"
                query = input_user_text
                messages = [{"role":"user",
                                    "content":[
                                        {"type":"text","text":query},
                                        {"type":"image_url","image_url":{"url":pic}}]}]
                chat_completion = client.chat.completions.create(
                            messages=messages,
                            model=model)
                model_output = chat_completion.choices[0].message.content
                st.markdown(model_output)

                #-------------------------------------------------------Text-To-Speech------------------------------------------------------------
                with st.spinner("converting text to audio"):


                    def text_to_speech_gtts(input_text,file_path):
                        audioobj = gTTS(
                                    text=input_text,
                                    lang="en",
                                    slow=False
                                )
                        audioobj.save(file_path)




                    ai_save_path ="streamlit_audio/ai.mp3" 
                    text_to_speech_gtts(input_text=model_output,file_path=ai_save_path)

                    with open("streamlit_audio/ai.mp3", "rb") as audio_file:
                        st.audio(audio_file.read(), format="audio/mp3")            




    





if __name__=="__main__":
    main()

