# main.py
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
import models
from pydantic import BaseModel
from typing import Dict
import openai
from deep_translator import GoogleTranslator
from langdetect import detect
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
# Create tables in database
Base.metadata.create_all(bind=engine)

# Initialize app
app = FastAPI()

# Enable CORS so frontend can talk to backend
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request bodies
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Home endpoint
@app.get("/")
def home():
    return {"message": "Server running successfully"}

# Register endpoint
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        return {"message": "Email already registered"}
    
    new_user = models.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# Login endpoint
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.password == user.password
    ).first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    return {"message": f"Login successful. Welcome {db_user.name}!"}

# Step 1: Load your downloaded GPT4All model

# Initialize the Flan-T5 model properly
model_name = "google/flan-t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

generator = pipeline("text2text-generation", model=model, tokenizer=tokenizer)

@app.post("/chat")
async def chat_endpoint(payload: Dict):
    user_message = payload.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="No message provided")

    try:
        # Detect language
        detected_lang = detect(user_message)

        # Translate input to English
        if detected_lang != "en":
            translated_input = GoogleTranslator(source=detected_lang, target="en").translate(user_message)
        else:
            translated_input = user_message

        # Generate response
        response = generator(translated_input, max_length=100)
        ai_response = response[0]['generated_text']

        # Translate back to original language if needed
        if detected_lang != "en":
            final_response = GoogleTranslator(source="en", target=detected_lang).translate(ai_response)
        else:
            final_response = ai_response

        return {"response": final_response}

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))