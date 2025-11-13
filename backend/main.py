import uuid
import os
import sys
from fastapi import FastAPI, UploadFile

# Add parent directory for OCR & storage access
sys.path.append(os.path.abspath("../../OCR/app/ocr"))

# OCR import
from ingest import extract_pdf_text

# Backend imports (local files)
from segmentation import segment_text
from scene_builder import generate_scenes
from build_animator import create_zone_videos
from tts import generate_audio
from video_renderer import render_final_video

app = FastAPI()

@app.post("/process")
async def process_pdf(pdf: UploadFile):

    file_id = str(uuid.uuid4())

    # storage paths
    base_storage = os.path.abspath("../storage")
    upload_dir = os.path.join(base_storage, "uploads")
    text_dir = os.path.join(base_storage, "text")

    os.makedirs(upload_dir, exist_ok=True)
    os.makedirs(text_dir, exist_ok=True)

    pdf_path = os.path.join(upload_dir, f"{file_id}.pdf")
    with open(pdf_path, "wb") as f:
        f.write(await pdf.read())

    # OCR
    text = extract_pdf_text(pdf_path)

    text_path = os.path.join(text_dir, f"{file_id}.txt")
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

    # Pipeline
    segment_paths = segment_text(text_path, file_id)
    scene_paths = generate_scenes(segment_paths, file_id)
    zone_videos = create_zone_videos(scene_paths, file_id)
    audio_paths = generate_audio(segment_paths, file_id)
    final_video_path = render_final_video(scene_paths, audio_paths, file_id)

    return {
        "status": "success",
        "file_id": file_id,
        "text_file": text_path,
        "segments": segment_paths,
        "scenes": scene_paths,
        "zone_videos": zone_videos,
        "audio_paths": audio_paths,
        "final_video": final_video_path
    }
