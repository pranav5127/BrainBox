import cloudinary
import cloudinary.uploader
import logging
import asyncio
from typing import Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from utils.config import (
    CLOUDINARY_API_KEY,
    CLOUDINARY_API_SECRET,
    CLOUDINARY_CLOUD_NAME
)

"""
Cloudinary Upload Module

This module provides functionality for uploading files to Cloudinary with automatic scheduled deletion.

The `CloudinaryService` class manages:
    - Uploading files to Cloudinary
    - Generating secure URLs and public IDs
    - Scheduling automatic deletion of files after a specified time interval

Configuration is handled via the `CloudinaryConfig` dataclass.

Classes:
    - CloudinaryConfig: Holds configuration parameters like credentials, folder name, and deletion delay.
    - CloudinaryService: Main service class for uploading and deleting files asynchronously.

Functions:
    - _configure_cloudinary(): Initializes Cloudinary with provided credentials.
    - _schedule_file_deletion(public_id, delay_minutes): Schedules deletion of a file after a delay.
    - upload_file(local_path, public_id=None): Uploads a file to Cloudinary and schedules its deletion.

Workflow:
    1. Configure Cloudinary with API credentials.
    2. Upload a file to the specified Cloudinary folder.
    3. Get the file’s secure URL and public ID.
    4. Automatically schedule deletion after a delay (default: 5 minutes).
    5. Return the secure URL and public ID for downstream use.

Usage:
    config = CloudinaryConfig(
        cloud_name="your_cloud_name",
        api_key="your_api_key",
        api_secret="your_api_secret"
    )
    service = CloudinaryService(config)
    url, public_id = service.upload_file("path/to/file.pdf")

Notes:
    - Only raw files are supported for upload (resource_type="raw").
    - Deletion is handled asynchronously using `asyncio.create_task`.

"""


@dataclass
class CloudinaryConfig:
    cloud_name: str
    api_key: str
    api_secret: str
    upload_folder: str = "presentations"
    auto_delete_delay: int = 5  # minutes


class CloudinaryService:
    def __init__(self, config: Optional[CloudinaryConfig] = None):
        self.logger = logging.getLogger(__name__)
        self.config = config or CloudinaryConfig(
            cloud_name=CLOUDINARY_CLOUD_NAME,
            api_key=CLOUDINARY_API_KEY,
            api_secret=CLOUDINARY_API_SECRET
        )
        self._configure_cloudinary()

    def _configure_cloudinary(self) -> None:
        cloudinary.config(
            cloud_name=self.config.cloud_name,
            api_key=self.config.api_key,
            api_secret=self.config.api_secret
        )

    async def _schedule_file_deletion(self, public_id: str, delay_minutes: int) -> None:
        try:
            await asyncio.sleep(delay_minutes * 60)
            result = cloudinary.uploader.destroy(public_id)
            if result.get('result') == 'ok':
                self.logger.info(f"Successfully deleted file: {public_id}")
            else:
                self.logger.error(f"Failed to delete file: {public_id}")
        except Exception as e:
            self.logger.error(f"Error during scheduled deletion of {public_id}: {str(e)}")

    def upload_file(self, local_path: str, public_id: Optional[str] = None) -> Tuple[str, str]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_public_id = public_id or f"temp_{timestamp}"

            result = cloudinary.uploader.upload(
                local_path,
                resource_type="raw",
                public_id=final_public_id,
                folder=self.config.upload_folder
            )

            secure_url = result.get("secure_url", "")
            full_public_id = result.get("public_id", "")

            asyncio.create_task(
                self._schedule_file_deletion(
                    full_public_id,
                    self.config.auto_delete_delay
                )
            )

            return secure_url, full_public_id

        except Exception as e:
            self.logger.error(f"Error uploading file {local_path}: {str(e)}")
            return None
