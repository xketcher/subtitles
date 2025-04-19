import os
from fastapi import FastAPI
from telegram import Update, File
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from utils import extract_audio_from_video, speech_to_text, translate_text, generate_srt

app = FastAPI()

BOT_TOKEN = "7755299955:AAEoUVRxOvdS3yn2YaZzz88aVGYlEbh2Ptc"
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        msg = update.message.caption or ""
        if "audio=en" in msg and "sub=my" in msg:
            file_id = update.message.video.file_id
            new_file: File = await context.bot.get_file(file_id)
            video_path = f"{TEMP_DIR}/{file_id}.mp4"
            audio_path = f"{TEMP_DIR}/{file_id}.mp3"
            srt_path = f"{TEMP_DIR}/{file_id}.srt"

            await new_file.download_to_drive(video_path)
            extract_audio_from_video(video_path, audio_path)
            text = speech_to_text(audio_path)
            translated = translate_text(text)
            srt = generate_srt(translated)
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(srt)

            await update.message.reply_document(document=open(srt_path, "rb"), filename="subtitle.srt")

app_telegram = ApplicationBuilder().token(BOT_TOKEN).build()
app_telegram.add_handler(MessageHandler(filters.VIDEO & filters.CaptionRegex("audio=en.*sub=my"), handle_video))

@app.on_event("startup")
async def startup():
    await app_telegram.initialize()
    await app_telegram.start()
    await app_telegram.updater.start_polling()

@app.on_event("shutdown")
async def shutdown():
    await app_telegram.updater.stop()
    await app_telegram.stop()
    await app_telegram.shutdown()
