# Messages Bot  

**Messages Bot** is a Telegram bot for bulk messaging and web scraping. It scrapes data from websites, cleans it, saves it to a MySQL database, and sends messages via Telegram.  

---

## Features  

- **Bulk Messaging:** Send messages to multiple users/groups.  
- **Web Scraping:** Extract data using Beautiful Soup and Scrapy.  
- **Data Cleaning:** Clean and structure scraped data.  
- **MySQL Integration:** Save data to a MySQL database.  
- **Error Handling:** Logs for failed message deliveries.  

---

## How It Works  

1. **Web Scraping:**  
   The bot scrapes data (e.g., audio sermons, transcripts, images) from a specified website using Beautiful Soup.  

2. **Data Cleaning:**  
   The scraped data is cleaned by removing special characters, standardizing text, and handling missing entries.  

3. **MySQL Integration:**  
   The cleaned data is saved to a MySQL database for efficient storage and retrieval.  

4. **Telegram Bot:**  
   The bot uses the Telegram API to send messages to users or groups based on the data stored in the database.  

---

# messages-bot

## How to Run  

### 1. Clone the Repository  
```bash  
git clone https://github.com/Xtley001/messages-bot.git  
cd messages-bot  
```  

### 2. Install Dependencies  
Install the required Python packages:  
```bash  
pip install -r requirements.txt  
```  

### 3. Set Up Environment Variables  
- Rename `.env.example` to `.env`.  
- Replace `YOUR_BOT_TOKEN_HERE` with your Telegram bot token.  
- Update the MySQL credentials in `.env`:  

```ini  
DB_HOST=your_database_host  
DB_USER=your_database_user  
DB_PASSWORD=your_database_password  
DB_NAME=your_database_name  
```  

### 4. Run the Bot  
Start the bot by running:  
```bash  
python main.py  
```  

### 5. Interact with the Bot  
- Open Telegram and search for your bot.  
- Use the `/start` command to initiate the bot.  
- Follow the bot’s prompts to send messages or manage data.  

---

## File Structure  

- **`main.py`** – Main script to run the bot.  
- **`scraper.py`** – Web scraping script.  
- **`database.py`** – MySQL database operations.  
- **`requirements.txt`** – List of dependencies.  
- **`.env.example`** – Example environment variable file.  
- **`logs/`** – Directory for error logs.  

---

## License  
This project is licensed under the **MIT License**. See the `LICENSE` file for details.  

---

## Support  
For questions or issues, open an issue on GitHub or contact the developer directly.  

---

## Acknowledgments  
- Thanks to the `python-telegram-bot` library for simplifying Telegram bot development.  
- Inspired by the need for efficient bulk messaging and data extraction solutions.  

