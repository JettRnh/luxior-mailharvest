#!/usr/bin/env python3
"""
Report Generator Module
"""

import json
import csv
from datetime import datetime

class ReportGenerator:
    def to_json(self, data, filename):
        """Save as JSON"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def to_text(self, data, filename):
        """Save as text"""
        with open(filename, 'w') as f:
            f.write(f"Luxior MailHarvest Report\n")
            f.write(f"Target: {data['target']}\n")
            f.write(f"Timestamp: {data['timestamp']}\n")
            f.write(f"{'='*60}\n\n")
            
            f.write(f"Total Emails Found: {len(data['emails'])}\n\n")
            
            if data['valid_emails']:
                f.write(f"Valid Emails: {len(data['valid_emails'])}\n")
                for email in data['valid_emails']:
                    f.write(f"  {email}\n")
                f.write("\n")
            
            if data['breached_emails']:
                f.write(f"Breached Emails: {len(data['breached_emails'])}\n")
                for email in data['breached_emails']:
                    f.write(f"  {email} [BREACHED]\n")
                f.write("\n")
            
            f.write(f"{'='*60}\n")
    
    def to_csv(self, data, filename):
        """Save as CSV"""
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Email', 'Valid', 'Breached', 'Source'])
            
            for email in data['emails']:
                valid = 'Yes' if email in data['valid_emails'] else 'No'
                breached = 'Yes' if email in data['breached_emails'] else 'No'
                source = self._find_source(email, data['sources'])
                writer.writerow([email, valid, breached, source])
    
    def _find_source(self, email, sources):
        """Find source of email"""
        for source_type, emails in sources.items():
            if email in emails:
                return source_type
        return 'Unknown'
