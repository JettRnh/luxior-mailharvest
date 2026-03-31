# Luxior MailHarvest — Email Intelligence Tool

**Owner:** Jet  
**GitHub:** https://github.com/JettRnh  
**Repository:** https://github.com/JettRnh/luxior-mailharvest.git  
**TikTok:** https://www.tiktok.com/@jettinibos_?_r=1&_t=ZS-957TcwUzSWf  
**Discord:** @jeet07685  

---

## What is Luxior MailHarvest?

Luxior MailHarvest is a Python-based email intelligence tool designed for security researchers, penetration testers, and OSINT investigators. It helps discover, validate, and analyze email addresses from various sources.

---

## Key Features

- Web Scraping — Extract emails from websites with recursive crawling  
- Domain Enumeration — Generate email patterns from common formats  
- Google Dorking — Search for emails using advanced queries  
- Email Validation — Check format validity and MX records  
- Breach Detection — Identify emails found in data breaches  
- Multi-Format Reports — Export results as JSON, TXT, or CSV  

---

## Quick Start

### Installation

    git clone https://github.com/JettRnh/Luxior-OSINT-2.git
    cd Luxior-OSINT-2
    pip install -r requirements.txt

### Basic Usage

    # Interactive mode (recommended)
    python mailharvest.py

    # Scrape a website
    python mailharvest.py -u https://example.com

    # Harvest from domain
    python mailharvest.py -d example.com

    # Validate emails from file
    python mailharvest.py -f emails.txt --validate

    # Check breach status
    python mailharvest.py -f emails.txt --breach

    # Full scan with all methods
    python mailharvest.py -u https://example.com --validate --breach -o json

---

## Command Line Options

| Option | Description |
|--------|------------|
| -u, --url | Target URL to scrape |
| -d, --domain | Target domain to harvest |
| -g, --dork | Google dork query |
| -f, --file | File containing emails |
| -o, --output | Output format: json, txt, csv (default: json) |
| --validate | Validate email addresses |
| --breach | Check breach status |
| --depth | Crawl depth (default: 2) |

---

## Interactive Mode

Run:

    python mailharvest.py

Interface:

    ╔═══════════════════════════════════════════════════════════════╗
    ║  LUXIOR MAILHARVEST — Email Intelligence Tool                ║
    ║  Owner: Jet | GitHub: JettRnh | TikTok: @jettinibos_         ║
    ╚═══════════════════════════════════════════════════════════════╝

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

---

## Project Structure

    luxior-mailharvest/
    ├── mailharvest.py
    ├── modules/
    │   ├── __init__.py
    │   ├── scraper.py
    │   ├── dork.py
    │   ├── validator.py
    │   ├── breach.py
    │   └── reporter.py
    ├── wordlists/
    │   ├── common_names.txt
    │   └── dorks.txt
    ├── output/
    ├── requirements.txt
    ├── README.md
    ├── LICENSE
    └── .gitignore

---

## Output Examples

JSON:

    {
      "target": "example.com",
      "timestamp": "2024-01-15T10:30:00",
      "emails": ["admin@example.com", "contact@example.com"],
      "valid_emails": ["admin@example.com", "contact@example.com"],
      "breached_emails": ["admin@example.com"],
      "sources": {
        "website": ["admin@example.com"],
        "domain_patterns": ["contact@example.com"]
      }
    }

TXT:

    Luxior MailHarvest Report
    Target: example.com
    Timestamp: 2024-01-15 10:30:00
    ============================================================

    Total Emails Found: 2

    Valid Emails: 2
      admin@example.com
      contact@example.com

    Breached Emails: 1
      admin@example.com [BREACHED]

    ============================================================

---

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- dnspython

---

## License

MIT License

Copyright (c) 2024 Jet (JettRnh)

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

---

## Disclaimer

This tool is intended for educational and authorized security testing only.  
Use only on systems you own or have explicit permission to test.  
The author is not responsible for misuse or damage.

---

## Credits

Built by Jet for the security research community.

GitHub: JettRnh  
TikTok: @jettinibos_
