from openai import OpenAI
import os
import base64
import streamlit as st
api_key = os.getenv("openai_api_key")

client = OpenAI(api_key=api_key)
import requests
#import neuralspace as ns
import assemblyai as aai
from dotenv import load_dotenv


load_dotenv()





def get_answer(messages):
    system_message = [{"role": "system", "content": "You are an helpful AI chatbot, that answers questions asked by User."}]
    messages = system_message + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        temperature=0.5,
        messages=messages
    )
    return response.choices[0].message.content

def speech_to_text(audio_data):
    with open(audio_data, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            response_format="text",
            file=audio_file
        )
    return transcript

def speech_to_text_hindi(audio_data):
           
        aai.settings.api_key = os.getenv("assemblyai_api_key")
        config = aai.TranscriptionConfig(language_code="hi")
        transcriber = aai.Transcriber(config=config)

        transcript = transcriber.transcribe(audio_data)
       
        return transcript.text

def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)