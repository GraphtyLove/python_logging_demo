import logging
import requests
from typing import List
from bs4 import BeautifulSoup

from db_logging import add_to_db
from datetime import datetime


# Define basic config for logs (date format,...)
# Will search for a LOG_LEVEL venv variable, if there is not, it will set "DEBUG" by default.
logging.basicConfig(
    level=logging.CRITICAL,
    handlers=[
        # Write logs to file
        logging.FileHandler(f"logs/{datetime.now().strftime('%d-%m-%Y_%H:%M')}.log"),
        # Allow the logger to also log in console
        logging.StreamHandler(),
    ],
    format="%(asctime)s %(levelname)-8s %(name)-20s -> %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
)
logger = logging.getLogger("HLN_SCRAPER")
logger.setLevel(logging.WARNING)
    

def get_article_title(
    url, 
    session: requests.Session, 
    article_number: int, 
) -> str | None:
    
    article_response = session.get(url)
    if article_response.status_code != 200:
        logger.error(f"Error fetching article {article_number} with status code: {article_response.status_code}")
        return None
    
    article_html = article_response.text
    soup = BeautifulSoup(article_html, 'html.parser')
    h1_tag = soup.find('h1')

    if h1_tag:
        title = h1_tag.text.strip()
        logger.debug(f"Title article {article_number}: {title}")
        add_to_db(title)
        return title
    else:
        logger.warning("H1 tag not found in article: {article_number}")
        return None

def get_all_articles(articles_url: List[str]) -> List[str]:
    articles_title = []
    session = requests.Session()
    # Fetch cookies
    session.get("https://www.hln.be/")

    for i, article_url in enumerate(articles_url):
        logger.debug(f"Scraping article {i+1}/{len(articles_url)}")
        article_title = get_article_title(article_url, session, i+1)
        articles_title.append(article_title)

    return articles_title

if __name__ == "__main__":
    logger.info("Start scraping...")
    articles_url = [
        "https://www.hln.be/deinze/na-levensbedreigende-slangenbeet-in-kroatie-bekomt-thibaut-6-nu-in-het-uz-gent-hij-zal-hier-nog-minstens-tot-het-einde-van-de-week-blijven~a21ad545/",
        "https://www.hln.be/deinze/zwembad-palaestra-gesloten-door-technisch-defect~af94047d/",
        "https://www.hln.be/deinze/acteurs-uit-vikings-en-game-of-thrones-te-gast-op-elftopia~a4b6e9b8/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
        "https://www.hln.be/deinze/skatekamp-aan-briel~a72c1f81/",
    ]
    logger.info(f"Scraping {len(articles_url)}")
    articles_title = get_all_articles(articles_url)
    logger.info(f"Done Scraping, found {len(articles_title)} articles' title")

