from moviepy.editor import *
import os

def create_video_scene(text, audio_path, output_path):
    # Load audio
    audio = AudioFileClip(audio_path)
    
    # Create text clip
    txt_clip = TextClip(
        text,
        fontsize=40,
        color='white',
        size=(720, 1280),
        method='caption'
    ).set_duration(audio.duration)

    txt_clip = txt_clip.set_position("center")

    # Solid background
    bg = ColorClip(size=(720, 1280), color=(0, 0, 0))\
            .set_duration(audio.duration)

    final = CompositeVideoClip([bg, txt_clip])
    final = final.set_audio(audio)

    final.write_videofile(output_path, fps=24)

    return output_path


def generate_video_scenes(segment_folder, audio_files, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    video_files = []

    segments = sorted(os.listdir(segment_folder))

    for i, filename in enumerate(segments):
        if filename.endswith(".txt"):
            text = open(os.path.join(segment_folder, filename)).read()
            audio_path = audio_files[i]
            video_path = os.path.join(output_folder, filename.replace(".txt", ".mp4"))

            create_video_scene(text, audio_path, video_path)
            video_files.append(video_path)

    return video_files

def merge_videos(video_files, output_path):
    clips = [VideoFileClip(v) for v in video_files]
    final = concatenate_videoclips(clips)
    final.write_videofile(output_path, fps=24)
    return output_path
