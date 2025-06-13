import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")
UNSPLASH_URL = "https://api.unsplash.com/search/photos"

if not GEMINI_API_KEY:
    raise Exception("GEMINI_API_KEY is not set")

if not CLOUDINARY_CLOUD_NAME or not CLOUDINARY_API_KEY or not CLOUDINARY_API_SECRET:
    raise Exception("CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY or CLOUDINARY_API_SECRET is not set")
