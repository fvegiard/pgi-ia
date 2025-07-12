#!/usr/bin/env python3
"""Email Watcher Service for PGI-IA"""

import os
import sys
import time
import json
import logging
from datetime import datetime
from pathlib import Path

# Pour Windows/Outlook
try:
    import win32com.client
    OUTLOOK_AVAILABLE = True
except ImportError:
    OUTLOOK_AVAILABLE = False

# Pour Linux/IMAP
import imaplib
import email
from email.header import decode_header

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("EmailWatcher")

class EmailWatcher:
    def __init__(self, backend_url="http://localhost:5000"):
        self.backend_url = backend_url
        self.processed_emails = set()
        
    def watch_outlook(self):
        """Watch Outlook emails on Windows"""
        if not OUTLOOK_AVAILABLE:
            logger.error("Outlook not available on this system")
            return
            
        outlook = win32com.client.Dispatch("Outlook.Application")
        namespace = outlook.GetNamespace("MAPI")
        inbox = namespace.GetDefaultFolder(6)
        
        logger.info("Watching Outlook inbox...")
        
        while True:
            for mail in inbox.Items:
                if mail.EntryID not in self.processed_emails:
                    if self.is_project_email(mail.Subject, mail.Body):
                        self.process_email({
                            "id": mail.EntryID,
                            "from": mail.SenderEmailAddress,
                            "subject": mail.Subject,
                            "body": mail.Body,
                            "attachments": [att.FileName for att in mail.Attachments],
                            "received": str(mail.ReceivedTime)
                        })
                        self.processed_emails.add(mail.EntryID)
            
            time.sleep(30)  # Check every 30 seconds
    
    def watch_imap(self, server, username, password):
        """Watch IMAP emails"""
        logger.info(f"Connecting to IMAP server {server}...")
        
        mail = imaplib.IMAP4_SSL(server)
        mail.login(username, password)
        mail.select("inbox")
        
        while True:
            _, messages = mail.search(None, "UNSEEN")
            
            for num in messages[0].split():
                _, msg = mail.fetch(num, "(RFC822)")
                email_body = msg[0][1]
                email_message = email.message_from_bytes(email_body)
                
                subject = decode_header(email_message["Subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                if self.is_project_email(subject, ""):
                    self.process_email({
                        "id": num.decode(),
                        "from": email_message["From"],
                        "subject": subject,
                        "body": self.get_email_body(email_message),
                        "received": email_message["Date"]
                    })
            
            time.sleep(30)
    
    def is_project_email(self, subject, body):
        """Check if email is project-related"""
        keywords = ["plan", "électrique", "electrical", "dwg", "pdf", "kahnawake", "alexis-nihon"]
        text = (subject + " " + body).lower()
        return any(keyword in text for keyword in keywords)
    
    def process_email(self, email_data):
        """Send email to backend for processing"""
        logger.info(f"Processing email: {email_data['subject']}")
        
        import requests
        try:
            response = requests.post(
                f"{self.backend_url}/api/emails/process",
                json=email_data
            )
            if response.status_code == 200:
                logger.info("Email processed successfully")
            else:
                logger.error(f"Failed to process email: {response.text}")
        except Exception as e:
            logger.error(f"Error sending email to backend: {e}")
    
    def get_email_body(self, email_message):
        """Extract email body"""
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()
        return body

if __name__ == "__main__":
    watcher = EmailWatcher()
    
    # Try Outlook first (Windows)
    if OUTLOOK_AVAILABLE:
        watcher.watch_outlook()
    else:
        # Fallback to IMAP
        logger.info("Outlook not available, using IMAP mock mode")
        # In production, get credentials from environment
        # watcher.watch_imap("imap.gmail.com", "user@gmail.com", "password")
        
        # For now, just log
        logger.info("Email watcher in standby mode (no email server configured)")
        while True:
            time.sleep(60)
