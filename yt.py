import yt_dlp
import os
import subprocess
import time
from tqdm import tqdm

# ✅ Progress Hook for Real-time Updates
def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', d.get('total_bytes_estimate', 0))
        downloaded_bytes = d.get('downloaded_bytes', 0)
        if total_bytes > 0:
            percentage = (downloaded_bytes / total_bytes) * 100
            tqdm.write(f"📥 Downloading: {percentage:.2f}% completed", end="\r")

# ✅ Function to Download and Merge Audio-Video
def download_youtube_video(url, format_code):
    """Download YouTube video with proper audio merge and progress bar."""
    output_path = "downloads/%(title)s.%(ext)s"
    final_output = "downloads/output.mp4"

    ydl_opts = {
        'format': f"{format_code}+bestaudio",
        'outtmpl': output_path,
        'quiet': True,
        'progress_hooks': [progress_hook]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_title = info.get('title', 'output')
        final_output = f"downloads/{video_title}.mp4"

    return final_output
