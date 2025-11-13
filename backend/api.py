# app/api.py
from fastapi import FastAPI, File, UploadFile
from app.ocr.ingest import pdf_to_images, extract_pdf_text
from app.ocr.preprocess import preprocess_image
from app.ocr.detect import detect_text_boxes
from app.ocr.recognize import recognize_from_box
from app.ocr.postprocess import normalize_text
import shutil, os, uuid, json

app = FastAPI()

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_dir = f"tmp/{uuid.uuid4().hex}"
    os.makedirs(temp_dir, exist_ok=True)
    pdf_path = os.path.join(temp_dir, file.filename)
    with open(pdf_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    images = pdf_to_images(pdf_path, out_dir=temp_dir)
    results = []
    for img_path in images:
        img_dict = preprocess_image(img_path)
        boxes = detect_text_boxes(img_dict)
        page_texts = []
        for b in boxes:
            txt = recognize_from_box(img_dict, b['bbox'])
            txt = normalize_text(txt)
            page_texts.append({"bbox": b['bbox'], "text": txt})
        results.append(page_texts)
    out = {"pages": results}
    # cleanup optionally
    return out

# run with: uvicorn app.api:app --reload --port 8000
