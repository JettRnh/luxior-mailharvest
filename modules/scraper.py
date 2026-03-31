#!/usr/bin/env python3
"""
Web Scraper Module — Extract emails from websites
"""

import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Luxior MailHarvest'
        })
        self.email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        self.visited = set()
        self.emails = set()
    
    def extract_emails(self, text):
        """Extract emails from text"""
        return set(self.email_pattern.findall(text))
    
    def scrape(self, url, depth=1, current_depth=0):
        """Recursively scrape website for emails"""
        if current_depth >= depth:
            return []
        
        if url in self.visited:
            return []
        
        self.visited.add(url)
        
        try:
            print(f"[*] Scraping: {url}")
            r = self.session.get(url, timeout=10)
            
            if r.status_code == 200:
                # Extract emails
                found = self.extract_emails(r.text)
                self.emails.update(found)
                
                if found:
                    for email in found:
                        print(f"    [+] Found: {email}")
                
                # Extract links for deeper crawl
                if current_depth + 1 < depth:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        full_url = urljoin(url, href)
                        
                        # Only crawl same domain
                        if urlparse(full_url).netloc == urlparse(url).netloc:
                            self.scrape(full_url, depth, current_depth + 1)
        
        except Exception as e:
            print(f"[!] Error scraping {url}: {e}")
        
        return list(self.emails)
