import json

import requests
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from summarizer import summarize_text
from text_to_speech import text_to_speech
from web_scraper import scrape_article
import boto3
import logging
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET = os.getenv("AWS_S3_BUCKET")

# ✅ Initialize AWS S3 Client
s3_client = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Initialize Bedrock Client
bedrock_client = boto3.client(
    "bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# Set the correct model ID (run AWS CLI to verify)
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

app = FastAPI()

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

logging.basicConfig(level=logging.INFO)

# ✅ Define input models
class TopicInput(BaseModel):
    topic: str

class URLInput(BaseModel):
    url: str

class TextInput(BaseModel):
    text: str


# ✅ 1️⃣ Generate Podcast from Topic
@app.post("/generate-podcast/")
def generate_podcast(input_data: TopicInput):
    """Scrapes the web, summarizes an article, and converts to speech."""
    try:
        # 🔹 Scrape the first relevant article (Use Bing Search API instead of Google)
        scraped_text = scrape_article(f"https://www.bing.com/search?q={input_data.topic}")

        if not scraped_text:
            raise HTTPException(status_code=404, detail="No relevant articles found.")

        # 🔹 Summarize the extracted text
        summary = summarize_text(scraped_text)

        # 🔹 Convert the summary to speech
        audio_file = text_to_speech(summary)

        # 🔹 Upload to S3
        s3_client.upload_file(audio_file, S3_BUCKET, audio_file, ExtraArgs={'ACL': 'public-read'})
        s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{audio_file}"

        return {"summary": summary, "audio_url": s3_url}

    except Exception as e:
        logging.error(f"Error in podcast generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 2️⃣ Summarize Text from an Article URL
@app.post("/summarize-url/")
def summarize_from_url(input_data: URLInput):
    """Extracts text from a URL and summarizes it."""
    try:
        article_text = scrape_article(input_data.url)

        if not article_text:
            raise HTTPException(status_code=404, detail="Could not extract text from the URL.")

        summary = summarize_text(article_text)
        return {"summary": summary}

    except Exception as e:
        logging.error(f"Error summarizing URL: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 3️⃣ Summarize User-Provided Text
@app.post("/summarize-text/")
def summarize_text_api(input_data: TextInput):
    """Summarizes user-provided text using AWS Bedrock AI."""
    try:
        if not input_data.text:
            raise HTTPException(status_code=400, detail="Invalid text input.")

        summary = summarize_text(input_data.text)  # Call AWS Bedrock summarizer
        return {"summary": summary}

    except Exception as e:
        print(f"❌ Error in text summarization: {str(e)}")
        raise HTTPException(status_code=500, detail="Summarization failed.")

# ✅ 4️⃣ Convert Any Text to Speech
@app.post("/text-to-speech/")
def convert_text_to_audio(input_data: TextInput):
    """Converts text to speech and uploads to S3."""
    try:
        if not input_data.text or not isinstance(input_data.text, str):
            raise HTTPException(status_code=400, detail="Invalid text input.")

        audio_file = text_to_speech(input_data.text)

        # 🔹 Upload to AWS S3
        s3_client.upload_file(audio_file, S3_BUCKET, audio_file, ExtraArgs={'ACL': 'public-read'})
        s3_url = f"https://{S3_BUCKET}.s3.amazonaws.com/{audio_file}"

        return {"audio_url": s3_url}

    except Exception as e:
        logging.error(f"Error in text-to-speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ✅ 5️⃣ Upload and Summarize a File (Future Feature)
@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    """Uploads and processes a file for summarization."""
    try:
        file_path = f"uploads/{file.filename}"

        # Save file locally
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Read file content (assuming it's a text file)
        with open(file_path, "r") as file_content:
            text = file_content.read()

        summary = summarize_text(text)

        return {"filename": file.filename, "summary": summary}

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))
