from gtts import gTTS
import os

def text_to_speech(text, output_path):
    tts = gTTS(text=text, lang='en')
    tts.save(output_path)
    return output_path

def generate_audio_for_segments(segments_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    audio_files = []

    for filename in sorted(os.listdir(segments_folder)):
        if filename.endswith(".txt"):
            text = open(os.path.join(segments_folder, filename), "r").read()
            audio_path = os.path.join(output_folder, filename.replace(".txt", ".mp3"))
            text_to_speech(text, audio_path)
            audio_files.append(audio_path)

    return audio_files
