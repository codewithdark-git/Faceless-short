import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ImageMagick configuration
IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

# Validate ImageMagick path
if not Path(IMAGEMAGICK_BINARY).exists():
    error_msg = f"ImageMagick not found at {IMAGEMAGICK_BINARY}. Please install ImageMagick and update the path."
    logger.error(error_msg)
    raise FileNotFoundError(error_msg)
