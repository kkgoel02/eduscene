import os

def segment_text(text_path: str, file_id: str, chunk_size: int = 120):
    """
    Segments extracted text into smaller chunks for scene generation.

    Parameters:
        text_path (str): path to the extracted text file.
        file_id (str): unique ID for the file.
        chunk_size (int): approx number of words per segment.

    Returns:
        list: paths of segment text files.
    """

    # Read the extracted text
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean up
    text = text.replace("\n", " ").strip()
    words = text.split()

    segments = []
    current = []

    # Split into ~chunk_size word chunks
    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            segments.append(" ".join(current))
            current = []

    # Add remaining words
    if current:
        segments.append(" ".join(current))

    # Output directory
    out_dir = "storage/segments"
    os.makedirs(out_dir, exist_ok=True)

    paths = []
    for idx, seg in enumerate(segments):
        seg_path = os.path.join(out_dir, f"{file_id}_{idx}.txt")
        with open(seg_path, "w", encoding="utf-8") as f:
            f.write(seg)
        paths.append(seg_path)

    return paths
