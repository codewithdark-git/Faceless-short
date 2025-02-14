import time
import os
import tempfile
import zipfile
import platform
import subprocess
import logging
from pathlib import Path
from moviepy.editor import (AudioFileClip, CompositeVideoClip, CompositeAudioClip, ImageClip,
                            TextClip, VideoFileClip)
from moviepy.audio.fx.audio_loop import audio_loop
from moviepy.audio.fx.audio_normalize import audio_normalize
import requests

logger = logging.getLogger(__name__)


def download_file(url, filename):
    with open(filename, 'wb') as f:
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        f.write(response.content)

def search_program(program_name):
    try: 
        search_cmd = "where" if platform.system() == "Windows" else "which"
        return subprocess.check_output([search_cmd, program_name]).decode().strip()
    except subprocess.CalledProcessError:
        return None

def get_program_path(program_name):
    program_path = search_program(program_name)
    return program_path

def get_output_media(audio_file_path, timed_captions, background_video_data, video_server):
    """Generate final video with audio and captions
    
    Args:
        audio_file_path (str): Path to audio file
        timed_captions (list): List of timed captions
        background_video_data (list): List of background video data
        video_server (str): Video server URL
        
    Returns:
        str: Path to output video file
        
    Raises:
        Exception: If video rendering fails
    """
    OUTPUT_FILE_NAME = "rendered_video.mp4"
    from utility.conf import IMAGEMAGICK_BINARY
    from moviepy.config import change_settings
    
    try:
        # Validate input files
        if not Path(audio_file_path).exists():
            raise FileNotFoundError(f"Audio file not found at {audio_file_path}")
            
        try:
            change_settings({"IMAGEMAGICK_BINARY": IMAGEMAGICK_BINARY})
            logger.info(f"Using ImageMagick from: {IMAGEMAGICK_BINARY}")
        except Exception as e:
            logger.error(f"Error configuring ImageMagick: {str(e)}")
            raise Exception(f"ImageMagick configuration failed: {str(e)}")
    except Exception as e:
        logger.error(f"Error in initial setup: {str(e)}")
        raise Exception(f"Initial setup failed: {str(e)}")





    
    visual_clips = []
    for (t1, t2), video_url in background_video_data:
        try:
            # Download the video file
            video_filename = tempfile.NamedTemporaryFile(delete=False).name
            logger.info(f"Downloading video from {video_url}")
            download_file(video_url, video_filename)
            
            if not Path(video_filename).exists():
                raise FileNotFoundError(f"Failed to download video from {video_url}")
                
            # Create VideoFileClip from the downloaded file
            video_clip = VideoFileClip(video_filename)
            if video_clip is None:
                raise ValueError(f"Failed to create video clip from {video_filename}")
                
            video_clip = video_clip.set_start(t1)
            video_clip = video_clip.set_end(t2)
            visual_clips.append(video_clip)
            logger.info(f"Added video clip from {video_url} ({t1}-{t2}s)")
            
        except Exception as e:
            logger.error(f"Error processing video {video_url}: {str(e)}")
            raise Exception(f"Failed to process video {video_url}: {str(e)}")

    
    audio_clips = []
    try:
        # Verify audio file exists and is valid
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
            
        audio_file_clip = AudioFileClip(audio_file_path)
        if audio_file_clip is None:
            raise ValueError(f"Failed to create audio clip from {audio_file_path}")
            
        # Normalize audio volume
        audio_file_clip = audio_normalize(audio_file_clip)
        
        # Verify audio duration
        if audio_file_clip.duration <= 0:
            raise ValueError("Audio file has zero or negative duration")
            
        audio_clips.append(audio_file_clip)
        logger.info(f"Added audio clip from {audio_file_path} (duration: {audio_file_clip.duration:.2f}s)")

    except Exception as e:
        logger.error(f"Error processing audio: {str(e)}")
        raise Exception(f"Failed to process audio: {str(e)}")


    for (t1, t2), text in timed_captions:
        try:
            # Updated caption style: changed font, fontsize, and position.
            text_clip = TextClip(
                txt=text, 
                fontsize=70, 
                font="Arial-Bold", 
                color="white", 
                stroke_width=2, 
                stroke_color="black", 
                method="label"
            )
            # Set the text to appear at the bottom-center
            text_clip = text_clip.set_start(t1).set_end(t2).set_position(('center','bottom'))
            visual_clips.append(text_clip)
            logger.info(f"Added text clip: {text} ({t1}-{t2}s)")
        except Exception as e:
            logger.error(f"Error creating text clip: {str(e)}")
            raise Exception(f"Failed to create text clip: {str(e)}")


    try:
        if not visual_clips:
            raise ValueError("No visual clips available for rendering")
            
        video = CompositeVideoClip(visual_clips)
        
        if audio_clips:
            audio = CompositeAudioClip(audio_clips)
            # Ensure video duration matches audio and update video with audio properly
            if video.duration < audio.duration:
                last_clip = visual_clips[-1]
                extended_clip = last_clip.set_end(audio.duration)
                visual_clips[-1] = extended_clip
                video = CompositeVideoClip(visual_clips)
                
            video = video.set_duration(audio.duration)
            # Updated audio application using set_audio
            video = video.set_audio(audio)
            logger.info(f"Audio synchronized with video (duration: {video.duration:.2f}s)")


        logger.info(f"Rendering final video to {OUTPUT_FILE_NAME}")
        video.write_videofile(OUTPUT_FILE_NAME, codec='libx264', audio_codec='aac', fps=25, preset='veryfast')
        
        # Clean up downloaded files
        for (t1, t2), video_url in background_video_data:
            video_filename = tempfile.NamedTemporaryFile(delete=False).name
            if Path(video_filename).exists():
                os.remove(video_filename)
                logger.info(f"Cleaned up temporary file: {video_filename}")

        if not Path(OUTPUT_FILE_NAME).exists():
            raise FileNotFoundError(f"Failed to create output video at {OUTPUT_FILE_NAME}")
            
        logger.info(f"Successfully rendered video at {OUTPUT_FILE_NAME}")
        return OUTPUT_FILE_NAME
        
    except Exception as e:
        logger.error(f"Error rendering video: {str(e)}")
        raise Exception(f"Video rendering failed: {str(e)}")
