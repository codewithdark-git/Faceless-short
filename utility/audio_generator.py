import edge_tts
import os
import logging

logger = logging.getLogger(__name__)

async def generate_audio(text, outputFilename):
    """Generate audio from text using edge_tts
    
    Args:
        text (str): Text to convert to speech
        outputFilename (str): Path to save the audio file
        
    Raises:
        Exception: If audio generation fails
    """
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(outputFilename), exist_ok=True)
        
        logger.info(f"Generating audio for text length: {len(text)}")
        # Updated voice parameter below:
        communicate = edge_tts.Communicate(text, "en-US-GuyNeural")
        await communicate.save(outputFilename)
        
        if not os.path.exists(outputFilename):
            raise Exception(f"Failed to create audio file at {outputFilename}")
            
        logger.info(f"Successfully generated audio at {outputFilename}")
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise Exception(f"Audio generation failed: {str(e)}")
