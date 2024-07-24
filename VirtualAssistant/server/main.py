from fastapi import FastAPI, UploadFile, Depends, File
from fastapi.responses import StreamingResponse
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
from io import BytesIO
import time

app = FastAPI()
load_dotenv()

def getClient(api_key, api_version, azure_endpoint):
    client = AzureOpenAI(
        api_key= os.getenv(api_key),  
        api_version=os.getenv(api_version),
        azure_endpoint = os.getenv(azure_endpoint)
    )
    return client

def getClients():
    return {
        "whisper_client": getClient("AZUREOPENAI_SPEECHMODEL", "TRANSCRIPTIONMODEL_VERSION", "AZUREOPENAI_SPEECHMODEL_ENDPOINT"),
        "chat_client": getClient("AZUREOPENAI_CHATMODEL", "CHATMODEL_VERSION", "AZUREOPENAI_CHATMODEL_ENDPOINT"),
        "tts_client": getClient("AZUREOPENAI_SPEECHMODEL", "TTSMODEL_VERSION", "AZUREOPENAI_SPEECHMODEL_ENDPOINT"),
    }

def transcribe_audio(audio_file, whisper_client):
    
    response = whisper_client.audio.transcriptions.create(
        file=audio_file,            
        model=os.getenv("WHISPERMODEL_DEPLOYMENT_MODEL")
    )
        
    return response

def generate_response(text: str, chat_client):
    response = chat_client.chat.completions.create(
            model=os.getenv("CHATMODEL_DEPLOYMENT_MODEL"),
            messages=[
                {"role": "system", "content": """
                You work for mandiri sekuritas. We just released our new trading platform called growin.
                Growin offers a comprehensive range of features for stock trading, mutual fund investment, and commodities trading.
                Growin offers an investment experience to you, that is now better, easier, and more convenient.
                """},
                {"role": "user", "content": f"{text}"},
            ],
            temperature=0.2,
            stream=False
        )
    return response.choices[0].message.content

def TTS(text: str, tts_client):
    response = tts_client.audio.speech.create(
        model=os.getenv("TTS_DEPLOYMENT_MODEL"),
        voice="alloy",
        input=text
    )
    audio_stream = BytesIO(response.content)
    return StreamingResponse(audio_stream, media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=speech.mp3"})

@app.post("/talk")
async def talk(file: UploadFile = File(...), clients:getClients = Depends()):
    start = time.time()
    audio = await file.read()
    buffer = BytesIO(audio)
    buffer.name = 'audio.m4a'
    end = time.time()
    print("Parsing Input File: ", end-start)
    
    start = time.time()
    transcription = transcribe_audio(buffer, clients["whisper_client"])
    end = time.time()
    print("Transcription: ", end-start)

    start = time.time()
    response = generate_response(transcription.text, clients["chat_client"])
    end = time.time()
    print("ChatGPT Conversation: ", end-start)

    start = time.time()
    output = TTS(response, clients["tts_client"])
    end = time.time()
    print("TTS: ", end-start)
    return output