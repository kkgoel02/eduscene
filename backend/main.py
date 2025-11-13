import os
from tts import generate_audio_for_segments
from video_renderer import generate_video_scenes, merge_videos

SEGMENTS_DIR = "storage/segments"
AUDIOS_DIR = "storage/audios"
VIDEOS_DIR = "storage/videos"

def run_pipeline():
    print("Generating audio...")
    audio_files = generate_audio_for_segments(SEGMENTS_DIR, AUDIOS_DIR)

    print("Generating video scenes...")
    video_files = generate_video_scenes(SEGMENTS_DIR, audio_files, VIDEOS_DIR)

    print("Merging videos...")
    final_output = merge_videos(video_files, "storage/final_video.mp4")

    print("Done! Final video saved at:", final_output)

if __name__ == "__main__":
    
    run_pipeline()
