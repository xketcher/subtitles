import os
import uuid
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
from deep_translator import GoogleTranslator

def extract_audio_from_video(video_path, output_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(output_path)

def speech_to_text(audio_path, language="en-US"):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_path)
    audio.export("temp.wav", format="wav")
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data, language=language)
    os.remove("temp.wav")
    return text

def translate_text(text, source="en", target="my"):
    return GoogleTranslator(source=source, target=target).translate(text)

def generate_srt(translated_text):
    lines = translated_text.split(". ")
    srt_content = ""
    for i, line in enumerate(lines):
        start = f"00:00:{i*5:02},000"
        end = f"00:00:{(i+1)*5:02},000"
        srt_content += f"{i+1}\n{start} --> {end}\n{line.strip()}\n\n"
    return srt_content
