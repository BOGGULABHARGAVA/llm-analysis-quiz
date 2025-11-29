"""
Browser handler - simplified to use requests only
"""
import logging
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def render_quiz_page(url: str) -> tuple[str, str]:
    """Fetch page using HTTP request"""
    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(separator='\n', strip=True)
        
        logger.info(f"Page fetched: {len(html_content)} chars")
        return html_content, text_content
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


class BrowserHandler:
    async def initialize(self): pass
    async def close(self): pass

_browser_handler = None
async def get_browser_handler():
    global _browser_handler
    if not _browser_handler:
        _browser_handler = BrowserHandler()
    return _browser_handler

async def cleanup_browser(): pass
