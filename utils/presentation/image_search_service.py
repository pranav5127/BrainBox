import requests
from PIL import Image
from io import BytesIO
import time

class ImageSearchService:
    HEADERS = {
        "User-Agent": "BrainBoxBot/1.0 (https://sugardevs.in/)"
    }

    @staticmethod
    def fetch_image(query: str, save_path: str):
        """
        Fetches the first Wikimedia Commons image for the given query,
        validates it's an image, retries if needed, and saves it to disk.
        """
        search_url = "https://commons.wikimedia.org/w/api.php"

        # Step 1: Search for file title
        search_params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": f"{query} filetype:bitmap",
            "srlimit": 1,
            "srnamespace": 6  # File namespace
        }

        try:
            search_response = requests.get(
                search_url,
                params=search_params,
                headers=ImageSearchService.HEADERS,
                timeout=10
            )
            search_response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Search request failed: {e}")

        search_data = search_response.json()
        search_results = search_data.get("query", {}).get("search", [])
        if not search_results:
            raise Exception(f"No image found for query: {query}")

        image_title = search_results[0]["title"]

        # Step 2: Get image URL
        info_params = {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "titles": image_title,
            "iiprop": "url"
        }

        try:
            info_response = requests.get(
                search_url,
                params=info_params,
                headers=ImageSearchService.HEADERS,
                timeout=10
            )
            info_response.raise_for_status()
        except requests.RequestException as e:
            raise Exception(f"Image info request failed: {e}")

        pages = info_response.json().get("query", {}).get("pages", {})
        if not pages:
            raise Exception(f"No image info found for: {image_title}")

        imageinfo = next(iter(pages.values())).get("imageinfo", [])
        if not imageinfo:
            raise Exception(f"No image URL found for: {image_title}")

        image_url = imageinfo[0].get("url")
        if not image_url:
            raise Exception(f"No URL found in image info for: {image_title}")

        # Step 3: Download, verify and save image with retry
        for attempt in range(3):
            try:
                img_response = requests.get(
                    image_url,
                    headers=ImageSearchService.HEADERS,
                    timeout=15,
                    stream=True
                )
                img_response.raise_for_status()

                content_type = img_response.headers.get("Content-Type", "")
                if not content_type.startswith("image/"):
                    raise Exception(f"Invalid content type: {content_type}")
                if content_type in ["image/svg+xml", "image/gif"]:
                    raise Exception(f"Unsupported image format: {content_type}")

                # Validate and convert image
                image_bytes = img_response.content
                image = Image.open(BytesIO(image_bytes))
                image.verify()  # verify content

                # Reload for saving
                image = Image.open(BytesIO(image_bytes)).convert("RGB")
                image.save(save_path, format="JPEG", quality=95, optimize=True, progressive=True)
                print(f"Image saved: {save_path}")
                return  # success

            except Exception as e:
                print(f"[Attempt {attempt + 1}/3] Download failed: {e}")
                time.sleep(2 ** attempt)

        # Final failure
        raise Exception(f"Failed to download and save image after 3 attempts: {query}")
