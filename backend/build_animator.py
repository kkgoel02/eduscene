import os
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, concatenate_videoclips

def create_zone_videos(scene_paths, file_id, fps=2, duration=3):
    """
    For every slide, divide into 3 vertical zones and produce 3 short animated videos:
    - zone 0 (top)
    - zone 1 (middle)
    - zone 2 (bottom)

    Each animation highlights a specific zone.4
    """

    out_dir = "storage/pointer_scenes"
    os.makedirs(out_dir, exist_ok=True)

    zone_videos = []  # store video paths for integration

    for idx, scene_path in enumerate(scene_paths):

        # Load slide image
        img = Image.open(scene_path)
        w, h = img.size

        # Compute heights of each zone
        zone_height = h // 3

        # Generate 3 animations
        for zone in range(3):
            frames = []
            y0 = zone * zone_height
            y1 = (zone + 1) * zone_height

            # Create animation frames
            for f in range(duration * fps):

                frame = img.copy()
                draw = ImageDraw.Draw(frame)

                # Semi-transparent highlight rectangle
                highlight_color = (255, 255, 0, 120)  # yellow transparent

                # PIL doesn't support alpha on RGB image, so fake highlight using outline + fill trick
                rect_fill = (255, 255, 0, 80)  
                draw.rectangle([(0, y0), (w, y1)], outline="yellow", width=6)
                draw.rectangle([(0, y0), (w, y1)], fill=rect_fill)

                # Save each frame temporarily
                frame_path = os.path.join(out_dir, f"{file_id}_{idx}_zone{zone}_frame{f}.png")
                frame.save(frame_path)
                frames.append(frame_path)

            # Convert frames → video clip
            clips = [ImageClip(f).set_duration(1 / fps) for f in frames]
            final_clip = concatenate_videoclips(clips, method="compose")

            video_path = os.path.join(out_dir, f"{file_id}_{idx}_zone{zone}.mp4")
            final_clip.write_videofile(video_path, fps=fps)

            zone_videos.append(video_path)

            # Clean temporary frames
            for f in frames:
                os.remove(f)

    return zone_videos
