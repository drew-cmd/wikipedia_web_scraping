import aiohttp
from aiohttp import web
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import sqlite3
import logging
import aiohttp_cors
import asyncio
import time
import tracemalloc
import aiosqlite


tracemalloc.start()


# Initialize SQLite database
DATABASE = 'wiki_data.db'

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLite database
def initialize_database():
    try:
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS wiki_data (wikilink TEXT PRIMARY KEY, page_name TEXT, content TEXT)')
    except sqlite3.Error as e:
        logger.error(f"Error initializing database: {e}")

# Check if the data exists in the database
def check_database(page_name):
    try:
        with sqlite3.connect(DATABASE) as db:
            cursor = db.cursor()
            cursor.execute('SELECT content FROM wiki_data WHERE page_name = ?', (page_name,))
            result = cursor.fetchone()
            return result[0] if result else None
    except sqlite3.Error as e:
        logger.error(f"Error checking database: {e}")
        return None

# Save data to the database
async def save_to_database_async(wikilink, page_name, content):
    try:
        logger.info(f"Saving data to database: {wikilink}, {page_name}")
        async with aiosqlite.connect(DATABASE) as db:
            await db.execute('INSERT INTO wiki_data (wikilink, page_name, content) VALUES (?, ?, ?)', (wikilink, page_name, content))
            await db.commit()  # Commit changes to the database
        logger.info("Data saved successfully")
    except sqlite3.Error as e:
        logger.error(f"Error saving to database: {e}")

async def save_to_database(wikilink, page_name, content):
    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, save_to_database_async, wikilink, page_name, content)
    except Exception as e:  # Catch any exception
        logger.error(f"Error occurred while calling save_to_database_async: {e}")

# Web Scraping with BeautifulSoup
async def webScraping(wikilink):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(wikilink) as response:
                content = await response.text()
                soup = BeautifulSoup(content, 'html.parser')

                # Your web scraping logic here

                # Remove unwanted elements
                unwanted_ids = ['right-navigation', 'vector-toc', 'vector-page-titlebar-toc', 'p-lang-btn']
                for unwanted_id in unwanted_ids:
                    unwanted_elem = soup.find(id=unwanted_id)
                    if unwanted_elem:
                        unwanted_elem.decompose()

                # Remove elements with aria-label="Namespaces"
                unwanted_aria = soup.find_all(attrs={"aria-label": "Namespaces"})
                for elem in unwanted_aria:
                    elem.decompose()

                # Check if the start tag exists
                start_element = soup.find(class_="mw-page-container")
                if start_element:
                    # Extract the HTML content starting from the start tag
                    content = str(start_element)
                else:
                    content = str(soup)

                return content
    except aiohttp.ClientError as e:
        logger.error(f"Error scraping website: {e}")
        return None

async def checkSaveToDb(wikilink):
    # Extract page name from the URL
    page_name = urlparse(wikilink).path.split('/')[-1]

    try:
        # Check if data exists in the database
        content = check_database(page_name)
        if content:
            logger.info("Data found in the database")
        else:
            logger.info("Data not found in the database, scraping website...")
            # Data not found, perform web scraping
            content = await webScraping(wikilink)
            if content:
                # Save data to the database
                logger.info("Saving data to database...")
                await save_to_database_async(wikilink, page_name, content)
            else:
                logger.error("Failed to retrieve content from Wikipedia")
    except Exception as e:
        logger.error(f"Error in checkSaveToDb: {e}")
    
    return content


def run_server():
    initialize_database()
    app = web.Application()

    # Define the handle function
    async def handle(request):
        start_time = time.time()  # Record the start time

        wikilink = request.query.get('wikilink', '')

        content = await checkSaveToDb(wikilink)

        if content:
            end_time = time.time()  # Record the end time
            duration = end_time - start_time  # Calculate the duration
            logger.info(f"Request processed in {duration:.2f} seconds")

            return web.Response(text=content)
        else:
            return web.Response(text="Error: Failed to retrieve content from Wikipedia")

    # Add CORS handling to the server function
    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/server/process_form"))
    cors.add(resource.add_route("GET", handle), {"*": aiohttp_cors.ResourceOptions()})

    # Run the server
    web.run_app(app, port=8000)

if __name__ == '__main__':
    run_server()