import asyncio
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Set
import logging
from playwright.async_api import async_playwright
import re
from app.core.config import settings

logger = logging.getLogger(__name__)

class WebsiteScraper:
    def __init__(self):
        self.visited_urls: Set[str] = set()
        self.max_pages = settings.MAX_PAGES_TO_SCRAPE
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    async def scrape_website(self, base_url: str) -> List[Dict[str, str]]:
        """Main method to scrape a website"""
        self.visited_urls.clear()
        base_domain = urlparse(base_url).netloc
        
        try:
            # First try static scraping
            pages = await self._scrape_static(base_url, base_domain)
            
            # If static scraping didn't get enough content, try dynamic scraping
            if len(pages) < 5:
                logger.info(f"Static scraping got {len(pages)} pages, trying dynamic scraping")
                dynamic_pages = await self._scrape_dynamic(base_url, base_domain)
                pages.extend(dynamic_pages)
            
            # Remove duplicates and limit pages
            unique_pages = self._deduplicate_pages(pages)
            return unique_pages[:self.max_pages]
            
        except Exception as e:
            logger.error(f"Error scraping website {base_url}: {e}")
            raise

    async def _scrape_static(self, base_url: str, base_domain: str) -> List[Dict[str, str]]:
        """Scrape static content using BeautifulSoup"""
        pages = []
        urls_to_visit = [base_url]
        
        while urls_to_visit and len(pages) < self.max_pages:
            url = urls_to_visit.pop(0)
            
            if url in self.visited_urls:
                continue
                
            self.visited_urls.add(url)
            
            try:
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract text content
                content = self._extract_text_content(soup)
                if content and len(content.strip()) > 100:  # Only add pages with substantial content
                    pages.append({
                        'url': url,
                        'title': self._extract_title(soup),
                        'content': content
                    })
                
                # Find more links to visit
                if len(pages) < self.max_pages:
                    new_urls = self._extract_links(soup, url, base_domain)
                    urls_to_visit.extend(new_urls)
                    
            except Exception as e:
                logger.warning(f"Failed to scrape {url}: {e}")
                continue
        
        return pages

    async def _scrape_dynamic(self, base_url: str, base_domain: str) -> List[Dict[str, str]]:
        """Scrape dynamic content using Playwright"""
        pages = []
        
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Set viewport and user agent
                await page.set_viewport_size({"width": 1280, "height": 720})
                await page.set_extra_http_headers({
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                # Visit the main page
                await page.goto(base_url, wait_until='networkidle', timeout=30000)
                
                # Wait for content to load
                await page.wait_for_timeout(2000)
                
                # Extract content from current page
                content = await self._extract_dynamic_content(page)
                if content:
                    pages.append({
                        'url': base_url,
                        'title': await page.title(),
                        'content': content
                    })
                
                # Find and visit additional pages
                links = await page.query_selector_all('a[href]')
                urls_to_visit = []
                
                for link in links[:20]:  # Limit to first 20 links
                    href = await link.get_attribute('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        if (urlparse(full_url).netloc == base_domain and 
                            full_url not in self.visited_urls and
                            len(pages) < self.max_pages):
                            urls_to_visit.append(full_url)
                
                # Visit additional pages
                for url in urls_to_visit[:10]:  # Limit to 10 additional pages
                    try:
                        await page.goto(url, wait_until='networkidle', timeout=15000)
                        await page.wait_for_timeout(1000)
                        
                        content = await self._extract_dynamic_content(page)
                        if content and len(content.strip()) > 100:
                            pages.append({
                                'url': url,
                                'title': await page.title(),
                                'content': content
                            })
                    except Exception as e:
                        logger.warning(f"Failed to scrape dynamic page {url}: {e}")
                        continue
                
                await browser.close()
                
        except Exception as e:
            logger.error(f"Dynamic scraping failed: {e}")
        
        return pages

    def _extract_text_content(self, soup: BeautifulSoup) -> str:
        """Extract meaningful text content from BeautifulSoup object"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text

    async def _extract_dynamic_content(self, page) -> str:
        """Extract text content from Playwright page"""
        try:
            # Remove unwanted elements
            await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('script, style, nav, footer, header, .nav, .footer, .header');
                    elements.forEach(el => el.remove());
                }
            """)
            
            # Get text content
            text = await page.evaluate("""
                () => {
                    return document.body.innerText;
                }
            """)
            
            # Clean up text
            text = re.sub(r'\s+', ' ', text)
            return text.strip()
            
        except Exception as e:
            logger.warning(f"Failed to extract dynamic content: {e}")
            return ""

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text().strip()
        return ""

    def _extract_links(self, soup: BeautifulSoup, current_url: str, base_domain: str) -> List[str]:
        """Extract links from page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            
            # Only include links from the same domain
            if (urlparse(full_url).netloc == base_domain and 
                full_url not in self.visited_urls and
                not full_url.endswith(('.pdf', '.jpg', '.png', '.gif', '.css', '.js'))):
                links.append(full_url)
        
        return links[:10]  # Limit to 10 links per page

    def _deduplicate_pages(self, pages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Remove duplicate pages based on URL"""
        seen_urls = set()
        unique_pages = []
        
        for page in pages:
            if page['url'] not in seen_urls:
                seen_urls.add(page['url'])
                unique_pages.append(page)
        
        return unique_pages

# Global scraper instance
scraper = WebsiteScraper()

async def scrape_website(url: str) -> List[Dict[str, str]]:
    """Main function to scrape a website"""
    return await scraper.scrape_website(url) 