#!/usr/bin/env python3
"""
Email Validator Module — Check if email is valid
"""

import re
import socket
import dns.resolver

class EmailValidator:
    def __init__(self):
        self.pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def is_valid_format(self, email):
        """Check email format"""
        return bool(self.pattern.match(email))
    
    def has_valid_domain(self, email):
        """Check if domain has MX record"""
        try:
            domain = email.split('@')[1]
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    
    def is_valid(self, email):
        """Full email validation"""
        if not self.is_valid_format(email):
            return False
        
        if not self.has_valid_domain(email):
            return False
        
        return True
