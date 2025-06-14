import os
import json
import re
from collections import Counter

from utils.common.cloudinary_service import CloudinaryService
from utils.common.gemini_service import GeminiService
from utils.presentation.image_search_service import ImageSearchService
from utils.presentation.presentation_service import PPTXService

"""
AI-Powered Presentation Generator with Image Integration

This module automates the end-to-end creation of visually appealing PowerPoint presentations 
based on a topic string, using:
- Google's Gemini API for content generation
- Wikimedia Commons search (via ImageSearchService) for fetching relevant images
- python-pptx for slide creation
- Cloudinary for file hosting and auto-deletion

The module includes utilities for:
    - Generating structured JSON slide content using a prompt-based Gemini call
    - Fetching and embedding slide-relevant images using keyword-based search
    - Converting the JSON response into a PowerPoint file (.pptx)
    - Uploading the file to Cloudinary and returning a shareable link

Dependencies:
    - GeminiService (for prompt-based text generation)
    - ImageSearchService (for relevant slide image search)
    - PPTXService (for presentation creation)
    - CloudinaryService (for upload & auto-delete)

Functions:
    - build_presentation_prompt(topic): Constructs a formatted prompt for Gemini to generate slides with image prompts.
    - simplify_image_prompt(prompt): Extracts key keywords from verbose image prompts for better search results.
    - generate_presentation_from_topic(topic): Full pipeline to create, save, upload, and return a presentation.
"""


def build_presentation_prompt(topic: str) -> str:
    return f"""
Create a well-structured presentation on the topic: "{topic}". 
Respond in JSON format with a list of slides. Each slide should contain:
- "title": the slide title
- "bullet_points": a list of 3-6 concise bullet points
- "image_prompt": a short phrase describing an image relevant to the slide

Example:
[
  {{
    "title": "Introduction",
    "bullet_points": ["Definition", "Importance", "Brief history"],
    "image_prompt": "A timeline showing key historical events"
  }}
]
Only return the JSON. No extra explanations or ```json.
"""



def simplify_image_prompt(prompt: str) -> str:
    words = re.findall(r'\b\w+\b', prompt.lower())
    stop_words = {
        "a", "an", "the", "of", "in", "on", "with", "to", "and", "for", "from",
        "showing", "illustrating", "representation", "diagram", "image", "prompt"
    }
    filtered = [w for w in words if w not in stop_words and len(w) > 2]
    common = Counter(filtered).most_common(3)
    return " ".join([word for word, _ in common]) or "technology diagram"


gemini = GeminiService()
cloudinary = CloudinaryService()
pptx = PPTXService()
image_search = ImageSearchService()


def generate_presentation_from_topic(topic: str) -> dict:
    if not topic:
        return {"status": "error", "error": "Topic is required"}

    try:
        image_dir = "/home/pranav/PycharmProjects/BrainBox/img"
        os.makedirs(image_dir, exist_ok=True)

        prompt = build_presentation_prompt(topic)
        response_text = gemini.get_response(prompt)
        cleaned = re.sub(r"^```json|```$", "", response_text, flags=re.IGNORECASE).strip()
        slides = json.loads(cleaned)

        for i, slide in enumerate(slides):
            image_prompt = slide.get("image_prompt")
            if image_prompt:
                simplified_prompt = simplify_image_prompt(image_prompt)
                print(f"Slide {i} image prompt: '{image_prompt}' ➜ '{simplified_prompt}'")

                image_path = os.path.join(image_dir, f"slide_image_{i}.jpg")
                try:
                    image_search.fetch_image(simplified_prompt, image_path)
                    slide["image_path"] = image_path
                except Exception as e:
                    print(f"Image fetch failed for slide {i}: {e}")
                    slide["image_path"] = None

        file_name = f"{topic.replace(' ', '_')}.pptx"
        local_path = os.path.join("/tmp", file_name)
        pptx.create_presentation(topic, slides, local_path)

        url, public_id = cloudinary.upload_file(local_path, public_id=topic.replace(" ", "_"))

        for slide in slides:
            image_path = slide.get("image_path")
            if image_path and os.path.exists(image_path):
                os.remove(image_path)
        os.rmdir(image_dir)

        return {
            "status": "success",
            "topic": topic,
            "slides": slides,
            "presentation_url": url
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}
