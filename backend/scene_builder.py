import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_scenes(segment_paths, file_id):
    """
    Creates simple slide images (PNG) from text segments.

    Parameters:
        segment_paths (list): list of text segment file paths.
        file_id (str): parent file ID for naming outputs.

    Returns:
        list: paths of generated scene image files.
    """

    out_dir = "storage/scenes"
    os.makedirs(out_dir, exist_ok=True)

    scene_paths = []

    # Choose a basic font — PIL default works everywhere
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()

    for idx, seg_path in enumerate(segment_paths):

        # Read segment text
        with open(seg_path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        # Create blank slide
        img = Image.new("RGB", (1280, 720), color="white")
        draw = ImageDraw.Draw(img)

        # Wrap text nicely
        wrapped_text = textwrap.fill(text, width=55)

        # Position text
        draw.text((60, 60), wrapped_text, fill="black", font=font)

        # Save slide
        out_path = os.path.join(out_dir, f"{file_id}_{idx}.png")
        img.save(out_path)
        scene_paths.append(out_path)

    return scene_paths