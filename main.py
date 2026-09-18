from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from pydantic import BaseModel
from fastapi import HTTPException
from better_profanity import profanity
import os
import uuid

app= FastAPI()
app.mount("/audio",  StaticFiles(directory="audio"),name="audio")

class SpeakRequest(BaseModel):
    text:str
    lang:str = "en"

profanity.load_censor_words()  # loads default English list
profanity.add_censor_words(["Idiot", "fool", "stupid"])

@app.get("/")
def serve_home():
    return FileResponse("index.html")

@app.post("/tts")
async def text_speech(req: SpeakRequest):
    if profanity.contains_profanity(req.text):
        raise HTTPException(
            status_code=400,
            detail="Text contains inappropriate language"
        )

@app.post("/tts")
async def text_to_speech(text: str):
    if not text or text.strip() == "":
        raise HTTPException(status_code=400, detail="Text input cannot be empty")

@app.post("/speak")
def speak(req: SpeakRequest):
    if profanity.contains_profanity(req.text):
        raise HTTPException(status_code=400, detail="Text contains inappropriate language")
    if len(req.text) > 600:
        raise HTTPException(status_code=400, detail="Text exceeds 600 character limit")

    if profanity.contains_profanity(req.text):
        raise HTTPException(status_code=400, detail="Text contains inappropriate language")

    lang_code = req.lang.split("-")[0]
    print("CONVERTED TO:", lang_code)
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    lang_code = req.lang.split("-")[0]

    tts = gTTS(text=req.text, lang=lang_code)  
    filename= f"{uuid.uuid4()}.mp3"
    filepath= f"audio/{filename}"
  
    tts.save(filepath)

    return FileResponse(path=filepath, media_type="audio/mpeg" , filename=filename)

