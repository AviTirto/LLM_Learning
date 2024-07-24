from fastapi import FastAPI, UploadFile, Depends, File
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import io

app = FastAPI()
load_dotenv()

def getClient(api_key, azure_endpoint):
    client = AzureOpenAI(
        api_key= os.getenv(api_key),  
        api_version="2024-02-01",
        azure_endpoint = os.getenv(azure_endpoint)
    )
    return client

def getClients():
    return {
        "whisper_client": getClient("AZUREOPENAI_WHISPERMODEL", "AZUREOPENAI_WHISPERMODEL_ENDPOINT"),
        "chat_client": getClient("AZUREOPENAI_CHATMODEL", "AZUREOPENAI_CHATMODEL_ENDPOINT"),
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
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{text}"},
            ],
            temperature=0.2,
            stream=False
        )
    return response.choices[0].message.content

@app.post("/talk")
async def talk(file: UploadFile = File(...), clients:getClients = Depends()):
    audio = await file.read()
    buffer = io.BytesIO(audio)
    buffer.name = 'audio.m4a'
    
    transcription = transcribe_audio(buffer, clients["whisper_client"])
    print(transcription)
    response = generate_response(transcription.text, clients["chat_client"])
    print(response)

    return response