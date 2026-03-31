#!/usr/bin/env python3
"""
Luxior MailHarvest — Email Intelligence Tool
Owner: Jet | GitHub: JettRnh | TikTok: @jettinibos_
"""

import os
import sys
import argparse
import json
import time
from datetime import datetime

# Add modules path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.scraper import WebScraper
from modules.dork import GoogleDork
from modules.validator import EmailValidator
from modules.breach import BreachChecker
from modules.reporter import ReportGenerator

class LuxiorMailHarvest:
    def __init__(self):
        self.scraper = WebScraper()
        self.dork = GoogleDork()
        self.validator = EmailValidator()
        self.breach = BreachChecker()
        self.reporter = ReportGenerator()
        self.results = {
            'target': '',
            'timestamp': datetime.now().isoformat(),
            'emails': [],
            'valid_emails': [],
            'breached_emails': [],
            'sources': {}
        }
    
    def banner(self):
        print("""
╔═══════════════════════════════════════════════════════════════╗
║  LUXIOR MAILHARVEST — Email Intelligence Tool                ║
║  Owner: Jet | GitHub: JettRnh | TikTok: @jettinibos_         ║
╚═══════════════════════════════════════════════════════════════╝
        """)
    
    def harvest_from_url(self, url, depth=1):
        """Harvest emails from website"""
        print(f"\n[*] Scraping: {url} (depth: {depth})")
        emails = self.scraper.scrape(url, depth)
        
        if emails:
            print(f"[+] Found {len(emails)} email(s)")
            self.results['emails'].extend(emails)
            self.results['sources']['website'] = emails
        else:
            print("[!] No emails found")
        
        return emails
    
    def harvest_from_domain(self, domain):
        """Harvest emails from domain (common patterns)"""
        print(f"\n[*] Harvesting from domain: {domain}")
        
        common_patterns = [
            f"admin@{domain}",
            f"info@{domain}",
            f"support@{domain}",
            f"contact@{domain}",
            f"webmaster@{domain}",
            f"sales@{domain}",
            f"help@{domain}",
            f"postmaster@{domain}",
            f"hostmaster@{domain}"
        ]
        
        # Load common names
        names_file = os.path.join(os.path.dirname(__file__), 'wordlists', 'common_names.txt')
        if os.path.exists(names_file):
            with open(names_file, 'r') as f:
                names = [line.strip() for line in f.readlines() if line.strip()]
                for name in names[:20]:  # Limit to 20
                    common_patterns.append(f"{name}@{domain}")
                    common_patterns.append(f"{name}.{name}@{domain}")
                    common_patterns.append(f"{name[0]}{name}@{domain}")
        
        print(f"[*] Generated {len(common_patterns)} email patterns")
        self.results['sources']['domain_patterns'] = common_patterns
        
        return common_patterns
    
    def harvest_from_dork(self, query, limit=50):
        """Harvest emails using Google dorks"""
        print(f"\n[*] Google dorking: {query}")
        emails = self.dork.search(query, limit)
        
        if emails:
            print(f"[+] Found {len(emails)} email(s)")
            self.results['emails'].extend(emails)
            self.results['sources']['dork'] = emails
        else:
            print("[!] No emails found")
        
        return emails
    
    def validate_emails(self, emails=None):
        """Validate email addresses"""
        if emails is None:
            emails = self.results['emails']
        
        if not emails:
            print("[!] No emails to validate")
            return []
        
        print(f"\n[*] Validating {len(emails)} email(s)...")
        valid = []
        
        for email in set(emails):
            if self.validator.is_valid(email):
                valid.append(email)
        
        self.results['valid_emails'] = valid
        print(f"[+] {len(valid)} valid email(s)")
        
        return valid
    
    def check_breach(self, emails=None):
        """Check if emails are breached"""
        if emails is None:
            emails = self.results['valid_emails'] or self.results['emails']
        
        if not emails:
            print("[!] No emails to check")
            return []
        
        print(f"\n[*] Checking breach status for {len(set(emails))} email(s)...")
        breached = []
        
        for email in set(emails):
            if self.breach.check(email):
                breached.append(email)
        
        self.results['breached_emails'] = breached
        print(f"[!] {len(breached)} email(s) found in breach database")
        
        return breached
    
    def generate_report(self, output_format='json'):
        """Generate report"""
        output_dir = os.path.join(os.path.dirname(__file__), 'output')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.results['target']}_{timestamp}"
        
        if output_format == 'json':
            filepath = os.path.join(output_dir, f"{filename}.json")
            self.reporter.to_json(self.results, filepath)
        elif output_format == 'txt':
            filepath = os.path.join(output_dir, f"{filename}.txt")
            self.reporter.to_text(self.results, filepath)
        elif output_format == 'csv':
            filepath = os.path.join(output_dir, f"{filename}.csv")
            self.reporter.to_csv(self.results, filepath)
        
        print(f"\n[+] Report saved: {filepath}")
        return filepath
    
    def run_interactive(self):
        """Interactive mode"""
        self.banner()
        
        print("""
╔═══════════════════════════════════════════════════════════════╗
║  MODES                                                       ║
╠═══════════════════════════════════════════════════════════════╣
║  1. Harvest from Website (URL)                               ║
║  2. Harvest from Domain (pattern guessing)                   ║
║  3. Harvest from Google Dork                                 ║
║  4. Full Scan (all methods)                                  ║
║  5. Validate Emails from file                                ║
║  6. Check Breach from file                                   ║
║  0. Exit                                                     ║
╚═══════════════════════════════════════════════════════════════╝
        """)
        
        choice = input("[?] Choose mode: ")
        
        if choice == "0":
            print("[+] Exiting...")
            sys.exit(0)
        
        elif choice == "1":
            url = input("[?] Target URL: ")
            depth = int(input("[?] Crawl depth [1]: ") or "1")
            self.results['target'] = url
            self.harvest_from_url(url, depth)
            
            if self.results['emails']:
                validate = input("[?] Validate emails? (y/n): ").lower()
                if validate == 'y':
                    self.validate_emails()
                    
                check_breach = input("[?] Check breach? (y/n): ").lower()
                if check_breach == 'y':
                    self.check_breach()
            
            self.generate_report()
        
        elif choice == "2":
            domain = input("[?] Domain (example.com): ")
            self.results['target'] = domain
            self.harvest_from_domain(domain)
            
            if self.results['sources']['domain_patterns']:
                validate = input("[?] Validate emails? (y/n): ").lower()
                if validate == 'y':
                    self.validate_emails(self.results['sources']['domain_patterns'])
                    
                check_breach = input("[?] Check breach? (y/n): ").lower()
                if check_breach == 'y':
                    self.check_breach()
            
            self.generate_report()
        
        elif choice == "3":
            query = input("[?] Google dork query: ")
            limit = int(input("[?] Max results [50]: ") or "50")
            self.results['target'] = query
            self.harvest_from_dork(query, limit)
            
            if self.results['emails']:
                validate = input("[?] Validate emails? (y/n): ").lower()
                if validate == 'y':
                    self.validate_emails()
                    
                check_breach = input("[?] Check breach? (y/n): ").lower()
                if check_breach == 'y':
                    self.check_breach()
            
            self.generate_report()
        
        elif choice == "4":
            target = input("[?] Target (domain or URL): ")
            self.results['target'] = target
            
            # Check if target is URL or domain
            if target.startswith('http'):
                depth = int(input("[?] Crawl depth [2]: ") or "2")
                self.harvest_from_url(target, depth)
            else:
                self.harvest_from_domain(target)
            
            # Google dork
            dork = input("[?] Google dork (optional, press Enter to skip): ")
            if dork:
                self.harvest_from_dork(dork, 30)
            
            # Validate
            self.validate_emails()
            
            # Check breach
            self.check_breach()
            
            # Report
            self.generate_report()
        
        elif choice == "5":
            filepath = input("[?] Email file path: ")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    emails = [line.strip() for line in f.readlines() if line.strip()]
                self.validate_emails(emails)
                
                output = input("[?] Save results? (y/n): ").lower()
                if output == 'y':
                    self.results['target'] = filepath
                    self.generate_report()
            else:
                print("[!] File not found")
        
        elif choice == "6":
            filepath = input("[?] Email file path: ")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    emails = [line.strip() for line in f.readlines() if line.strip()]
                self.check_breach(emails)
                
                output = input("[?] Save results? (y/n): ").lower()
                if output == 'y':
                    self.results['target'] = filepath
                    self.generate_report()
            else:
                print("[!] File not found")
        
        else:
            print("[!] Invalid choice")
        
        input("\n[*] Press Enter to continue...")
        self.run_interactive()

def main():
    tool = LuxiorMailHarvest()
    
    if len(sys.argv) > 1:
        # Command line mode
        parser = argparse.ArgumentParser(description='Luxior MailHarvest - Email Intelligence Tool')
        parser.add_argument('-u', '--url', help='Target URL to scrape')
        parser.add_argument('-d', '--domain', help='Target domain')
        parser.add_argument('-g', '--dork', help='Google dork query')
        parser.add_argument('-f', '--file', help='File with emails to validate')
        parser.add_argument('-o', '--output', choices=['json', 'txt', 'csv'], default='json', help='Output format')
        parser.add_argument('--validate', action='store_true', help='Validate emails')
        parser.add_argument('--breach', action='store_true', help='Check breach status')
        parser.add_argument('--depth', type=int, default=2, help='Crawl depth')
        
        args = parser.parse_args()
        
        if args.url:
            tool.results['target'] = args.url
            tool.harvest_from_url(args.url, args.depth)
        elif args.domain:
            tool.results['target'] = args.domain
            tool.harvest_from_domain(args.domain)
        elif args.dork:
            tool.results['target'] = args.dork
            tool.harvest_from_dork(args.dork)
        elif args.file:
            with open(args.file, 'r') as f:
                emails = [line.strip() for line in f.readlines() if line.strip()]
            if args.validate:
                tool.validate_emails(emails)
            if args.breach:
                tool.check_breach(emails)
            sys.exit(0)
        else:
            parser.print_help()
            sys.exit(1)
        
        if args.validate and tool.results['emails']:
            tool.validate_emails()
        if args.breach and tool.results['emails']:
            tool.check_breach()
        
        tool.generate_report(args.output)
    else:
        tool.run_interactive()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
        sys.exit(0)
