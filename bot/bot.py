import os
import re
import requests
import mysql.connector
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import DB_CONFIG, TELEGRAM_BOT_TOKEN
from utils.logger import logger

# Text cleaning function
def clean_description(description):
    """Clean the description by removing unnecessary text."""
    # Remove unwanted phrases
    unwanted_phrases = [
        "Download. Listen. Share. Be Transformed.",
        "PlayStopNext»«Prev",
        "HIDE PLAYLIST",
        "X",
        "Topics:",
        "«",
        "»"
    ]
    for phrase in unwanted_phrases:
        description = description.replace(phrase, "")

    # Remove extra spaces and line breaks
    description = re.sub(r"\s+", " ", description).strip()
    return description

# Database connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

def load_data():
    """Load data from the database for search."""
    cursor.execute("SELECT id, title, description, date, mp3_link, image_url FROM messages")
    return cursor.fetchall()

def search_messages(query):
    """Search messages using TF-IDF and cosine similarity."""
    data = load_data()
    texts = [f"{row[1]} {row[2]}" for row in data]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    sorted_indices = similarities.argsort()[::-1]
    return [data[i] for i in sorted_indices[:5]]  # Return top 5 results

async def start(update: Update, context: CallbackContext):
    """Handle the /start command."""
    await update.message.reply_text("Welcome! Use /search <query> to find sermons.")

async def search(update: Update, context: CallbackContext):
    """Handle the /search command."""
    try:
        query = " ".join(context.args)
        if not query:
            await update.message.reply_text("Please provide a search query. Example: /search power")
            return

        await update.message.reply_text("Searching for sermons...")

        results = search_messages(query)
        if not results:
            await update.message.reply_text("No sermons found. Try different keywords.")
            return

        for result in results:
            message_id, title, description, date, mp3_link, image_url = result

            # Clean up the description
            description = clean_description(description)

            # Format the response
            response = (
                f"*{title}*\n\n"
                f"**Date:** {date}\n"
                f"**Description:**\n{description}\n\n"
                f"[MP3 Link]({mp3_link})"
            )

            # Send the image (if available)
            if image_url:
                try:
                    await update.message.reply_photo(photo=image_url, caption=response, parse_mode="Markdown")
                except Exception as e:
                    logger.error(f"Failed to send image: {e}")
                    await update.message.reply_markdown(response)
            else:
                await update.message.reply_markdown(response)

            # Download and send the audio file
            try:
                # Download the MP3 file
                audio_file = f"temp_{message_id}.mp3"
                with requests.get(mp3_link, stream=True) as r:
                    r.raise_for_status()
                    with open(audio_file, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

                # Send the audio file
                with open(audio_file, "rb") as audio:
                    await update.message.reply_audio(audio, title=title)

                # Delete the temporary file
                os.remove(audio_file)
            except Exception as e:
                logger.error(f"Failed to send audio: {e}")
                await update.message.reply_text("Unable to send the audio file. Please use the MP3 link.")
    except Exception as e:
        logger.error(f"Error in search: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

def main():
    """Start the Telegram bot."""
    try:
        application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("search", search))

        # Start the bot
        logger.info("Starting the bot...")
        application.run_polling()
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()