import sys
import os
from bs4 import XMLParsedAsHTMLWarning
import warnings

# Suppress the XMLParsedAsHTMLWarning
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Add the root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.config import DB_CONFIG, WEBSITE_URL, SITEMAP_URL
import requests
from bs4 import BeautifulSoup
import mysql.connector
from datetime import datetime
from utils.logger import logger

# Database connection
db = mysql.connector.connect(**DB_CONFIG)
cursor = db.cursor()

def parse_sitemap(sitemap_url):
    """Fetch and parse the sitemap to extract URLs."""
    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, features="xml")  # Use "xml" parser

        # Extract all <loc> tags
        loc_tags = soup.find_all("loc")
        urls = [loc.text for loc in loc_tags]

        # Debug: Print the URLs found in the sitemap
        logger.debug(f"Found {len(urls)} URLs in the sitemap: {urls}")

        return urls
    except Exception as e:
        logger.error(f"Error parsing sitemap: {e}")
        return []

def scrape_sermon_page(url):
    """Scrape a single sermon page for data."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract title
        title_element = soup.find("h2", class_="wpfc-sermon-single-title")
        title = title_element.text.strip() if title_element else "No Title"

        # Extract description
        description_element = soup.find("div", class_="wpfc-sermon-single-main")
        description = description_element.text.strip() if description_element else "No Description"

        # Extract date
        date_element = soup.find("div", class_="wpfc-sermon-single-meta-date")
        date_str = date_element.text.strip() if date_element else None
        date = datetime.strptime(date_str, "%dth %B %Y").date() if date_str else None

        # Extract MP3 link
        mp3_link_element = soup.find("a", class_="wpfc-sermon-single-audio-download")
        mp3_link = mp3_link_element["href"] if mp3_link_element else "No MP3 Link"

        # Extract image URL
        image_element = soup.find("img", class_="wpfc-sermon-single-image-img")
        image_url = image_element["src"] if image_element else "No Image URL"

        return {
            "title": title,
            "description": description,
            "date": date,
            "mp3_link": mp3_link,
            "image_url": image_url
        }
    except Exception as e:
        logger.error(f"Error scraping {url}: {e}")
        return None

def save_to_database(data):
    """Save scraped data to the database."""
    sql = """
    INSERT INTO messages (title, description, date, mp3_link, image_url)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (data["title"], data["description"], data["date"], data["mp3_link"], data["image_url"])
    cursor.execute(sql, values)
    db.commit()

def scrape_website():
    """Main function to scrape the website."""
    logger.info("Starting to scrape the website...")

    # Parse the main sitemap
    main_sitemap_urls = parse_sitemap(SITEMAP_URL)
    logger.info(f"Found {len(main_sitemap_urls)} URLs in the main sitemap.")

    # Filter for the sermon sitemap
    sermon_sitemap_urls = [url for url in main_sitemap_urls if "wp-sitemap-posts-wpfc_sermon" in url]
    logger.info(f"Found {len(sermon_sitemap_urls)} sermon sitemap URLs.")

    # Parse the sermon sitemap to extract sermon URLs
    sermon_urls = []
    for sitemap_url in sermon_sitemap_urls:
        urls = parse_sitemap(sitemap_url)
        sermon_urls.extend(urls)

    logger.info(f"Found {len(sermon_urls)} sermon URLs.")

    # Scrape each sermon URL
    for url in sermon_urls:
        logger.info(f"Scraping URL: {url}")
        data = scrape_sermon_page(url)
        if data:
            save_to_database(data)
            logger.info(f"Scraped and saved: {data['title']}")
        else:
            logger.warning(f"Failed to scrape data from URL: {url}")

    logger.info("Scraping completed.")

if __name__ == "__main__":
    scrape_website()