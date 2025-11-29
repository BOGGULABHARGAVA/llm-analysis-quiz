"""
Browser handler for rendering JavaScript-based quiz pages
"""
import asyncio
import logging
from typing import Optional
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeout
from config import Config

logger = logging.getLogger(__name__)


class BrowserHandler:
    """Handles headless browser operations for rendering quiz pages"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.playwright = None
        
    async def initialize(self):
        """Initialize the browser"""
        try:
            if not self.playwright:
                self.playwright = await async_playwright().start()
                self.browser = await self.playwright.chromium.launch(
                    headless=Config.HEADLESS,
                    args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
                )
                logger.info("Browser initialized successfully")
                
                # Verify browser is working
                if not self.browser:
                    raise RuntimeError("Browser initialization returned None")
                    
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            # Cleanup on failure
            if self.browser:
                try:
                    await self.browser.close()
                except:
                    pass
            if self.playwright:
                try:
                    await self.playwright.stop()
                except:
                    pass
            self.browser = None
            self.playwright = None
            raise
    
    async def close(self):
        """Close the browser"""
        try:
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")
    
    async def render_page(self, url: str, wait_for_selector: str = "#result") -> tuple[str, str]:
        """
        Render a page with JavaScript execution
        
        Args:
            url: URL to render
            wait_for_selector: CSS selector to wait for (optional)
            
        Returns:
            tuple: (html_content, text_content)
        """
        page: Optional[Page] = None
        
        try:
            if not self.browser:
                await self.initialize()
            
            page = await self.browser.new_page()
            
            # Navigate to the page
            logger.info(f"Navigating to: {url}")
            await page.goto(url, wait_until='networkidle', timeout=Config.BROWSER_TIMEOUT)
            
            # Wait for specific selector if provided
            if wait_for_selector:
                try:
                    await page.wait_for_selector(wait_for_selector, timeout=10000)
                except PlaywrightTimeout:
                    logger.warning(f"Selector {wait_for_selector} not found, continuing anyway")
            
            # Additional wait for JavaScript execution
            await page.wait_for_timeout(2000)
            
            # Get both HTML and text content
            html_content = await page.content()
            text_content = await page.inner_text('body')
            
            logger.info(f"Page rendered successfully: {len(html_content)} chars")
            
            return html_content, text_content
            
        except Exception as e:
            logger.error(f"Error rendering page {url}: {e}")
            raise
        
        finally:
            if page:
                await page.close()
    
    async def get_element_text(self, url: str, selector: str) -> Optional[str]:
        """Get text content of a specific element"""
        page: Optional[Page] = None
        
        try:
            if not self.browser:
                await self.initialize()
            
            page = await self.browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=Config.BROWSER_TIMEOUT)
            
            await page.wait_for_selector(selector, timeout=10000)
            text = await page.inner_text(selector)
            
            return text
            
        except Exception as e:
            logger.error(f"Error getting element text: {e}")
            return None
        
        finally:
            if page:
                await page.close()
    
    async def screenshot(self, url: str, full_page: bool = True) -> Optional[bytes]:
        """Take a screenshot of the page"""
        page: Optional[Page] = None
        
        try:
            if not self.browser:
                await self.initialize()
            
            page = await self.browser.new_page()
            await page.goto(url, wait_until='networkidle', timeout=Config.BROWSER_TIMEOUT)
            
            screenshot_bytes = await page.screenshot(full_page=full_page)
            
            return screenshot_bytes
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
        
        finally:
            if page:
                await page.close()


# Singleton instance
_browser_handler: Optional[BrowserHandler] = None


async def get_browser_handler() -> BrowserHandler:
    """Get or create the browser handler singleton"""
    global _browser_handler
    
    if _browser_handler is None:
        _browser_handler = BrowserHandler()
        try:
            await _browser_handler.initialize()
        except Exception as e:
            logger.error(f"Failed to initialize browser handler: {e}")
            _browser_handler = None
            raise RuntimeError(f"Browser initialization failed: {e}") from e
    
    if _browser_handler.browser is None:
        # Browser was created but somehow became None, reinitialize
        try:
            await _browser_handler.initialize()
        except Exception as e:
            logger.error(f"Failed to reinitialize browser: {e}")
            _browser_handler = None
            raise RuntimeError(f"Browser reinitialization failed: {e}") from e
    
    return _browser_handler


async def render_quiz_page(url: str) -> tuple[str, str]:
    """
    Convenience function to render a quiz page
    
    Returns:
        tuple: (html_content, text_content)
    """
    handler = await get_browser_handler()
    return await handler.render_page(url)


# Cleanup function
async def cleanup_browser():
    """Cleanup browser resources"""
    global _browser_handler
    
    if _browser_handler:
        await _browser_handler.close()
        _browser_handler = None
