#!/usr/bin/env python3
import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import Optional

def send_email_smtp(recipient_email: str, file_path: str, abrechnungsmonat: str, rows_count: int) -> bool:
    """Sendet die CSV-Datei per E-Mail über SMTP (Mailgun SMTP)"""
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not all([sender_email, sender_password, smtp_server]):
            print("SMTP-Konfiguration unvollständig")
            return False
        
        # E-Mail erstellen
        msg = MIMEMultipart()
        msg['From'] = f"Lohnabrechnung OTQ <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"Lohnabrechnung {abrechnungsmonat}"
        
        body = f"""
Ihre Lohnabrechnung wurde konvertiert.

Abrechnungsmonat: {abrechnungsmonat}
Verarbeitete Zeilen: {rows_count}

Die CSV-Datei finden Sie im Anhang.

Mit freundlichen Grüßen,
OTQ GmbH
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Datei anhängen
        if os.path.exists(file_path):
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            filename = f"lohnabrechnung_{abrechnungsmonat}.csv"
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)
        
        # E-Mail senden
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ E-Mail erfolgreich gesendet via SMTP")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Fehler: {str(e)}")
        return False

def send_simple_email_smtp(recipient_email: str, subject: str, body: str) -> bool:
    """Sendet eine einfache Text-E-Mail über SMTP"""
    try:
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not all([sender_email, sender_password, smtp_server]):
            print("SMTP-Konfiguration unvollständig")
            return False
        
        msg = MIMEMultipart()
        msg['From'] = f"Lohnabrechnung OTQ <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        print(f"✅ Test-E-Mail erfolgreich gesendet via SMTP")
        return True
        
    except Exception as e:
        print(f"❌ SMTP Fehler: {str(e)}")
        return False

def send_email_mailgun(recipient_email: str, file_path: str, abrechnungsmonat: str, rows_count: int) -> bool:
    """Sendet die CSV-Datei per E-Mail über Mailgun API"""
    try:
        # Mailgun Konfiguration
        api_key = os.getenv("MAILGUN_API_KEY")
        domain = os.getenv("MAILGUN_DOMAIN")
        base_url = os.getenv("MAILGUN_API_BASE_URL", "https://api.mailgun.net/v3")
        from_email = os.getenv("MAILGUN_FROM")
        
        if not all([api_key, domain, from_email]):
            print("Mailgun-Konfiguration unvollständig")
            return False
        
        # E-Mail Inhalt
        subject = f"Lohnabrechnung {abrechnungsmonat}"
        text_body = f"""
Ihre Lohnabrechnung wurde konvertiert.

Abrechnungsmonat: {abrechnungsmonat}
Verarbeitete Zeilen: {rows_count}

Die CSV-Datei finden Sie im Anhang.

Mit freundlichen Grüßen,
OTQ GmbH
        """
        
        # Datei für Anhang vorbereiten
        files = []
        if os.path.exists(file_path):
            filename = f"lohnabrechnung_{abrechnungsmonat}.csv"
            with open(file_path, 'rb') as f:
                files = [("attachment", (filename, f.read(), "text/csv"))]
        
        # Mailgun API Request
        url = f"{base_url}/{domain}/messages"
        
        response = requests.post(
            url,
            auth=("api", api_key),
            files=files,
            data={
                "from": from_email,
                "to": recipient_email,
                "subject": subject,
                "text": text_body
            }
        )
        
        if response.status_code == 200:
            print(f"✅ E-Mail erfolgreich gesendet via Mailgun")
            return True
        else:
            print(f"❌ Mailgun Fehler: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Mailgun Fehler: {str(e)}")
        return False

def send_simple_email_mailgun(recipient_email: str, subject: str, body: str) -> bool:
    """Sendet eine einfache Text-E-Mail über Mailgun"""
    try:
        # Mailgun Konfiguration
        api_key = os.getenv("MAILGUN_API_KEY")
        domain = os.getenv("MAILGUN_DOMAIN")
        base_url = os.getenv("MAILGUN_API_BASE_URL", "https://api.mailgun.net/v3")
        from_email = os.getenv("MAILGUN_FROM")
        
        if not all([api_key, domain, from_email]):
            print("Mailgun-Konfiguration unvollständig")
            return False
        
        # Mailgun API Request
        url = f"{base_url}/{domain}/messages"
        
        response = requests.post(
            url,
            auth=("api", api_key),
            data={
                "from": from_email,
                "to": recipient_email,
                "subject": subject,
                "text": body
            }
        )
        
        if response.status_code == 200:
            print(f"✅ Test-E-Mail erfolgreich gesendet via Mailgun")
            return True
        else:
            print(f"❌ Mailgun Fehler: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Mailgun Fehler: {str(e)}")
        return False

# Hauptfunktionen - versuchen SMTP zuerst, dann Mailgun
def send_email(recipient_email: str, file_path: str, abrechnungsmonat: str, rows_count: int) -> bool:
    """Hauptfunktion für E-Mail-Versand - versucht SMTP zuerst, dann Mailgun"""
    # Prüfen welche Konfiguration verfügbar ist
    smtp_available = all([
        os.getenv("SENDER_EMAIL"),
        os.getenv("SENDER_PASSWORD"), 
        os.getenv("SMTP_SERVER")
    ])
    
    mailgun_available = all([
        os.getenv("MAILGUN_API_KEY"),
        os.getenv("MAILGUN_DOMAIN"),
        os.getenv("MAILGUN_FROM")
    ])
    
    # SMTP zuerst versuchen (falls konfiguriert)
    if smtp_available:
        if send_email_smtp(recipient_email, file_path, abrechnungsmonat, rows_count):
            return True
        print("SMTP fehlgeschlagen, versuche Mailgun...")
    
    # Fallback zu Mailgun
    if mailgun_available:
        return send_email_mailgun(recipient_email, file_path, abrechnungsmonat, rows_count)
    
    print("❌ Keine E-Mail-Konfiguration verfügbar")
    return False

def send_simple_email(recipient_email: str, subject: str, body: str) -> bool:
    """Hauptfunktion für einfache E-Mails - versucht SMTP zuerst, dann Mailgun"""
    # Prüfen welche Konfiguration verfügbar ist
    smtp_available = all([
        os.getenv("SENDER_EMAIL"),
        os.getenv("SENDER_PASSWORD"), 
        os.getenv("SMTP_SERVER")
    ])
    
    mailgun_available = all([
        os.getenv("MAILGUN_API_KEY"),
        os.getenv("MAILGUN_DOMAIN"),
        os.getenv("MAILGUN_FROM")
    ])
    
    # SMTP zuerst versuchen (falls konfiguriert)
    if smtp_available:
        if send_simple_email_smtp(recipient_email, subject, body):
            return True
        print("SMTP fehlgeschlagen, versuche Mailgun...")
    
    # Fallback zu Mailgun
    if mailgun_available:
        return send_simple_email_mailgun(recipient_email, subject, body)
    
    print("❌ Keine E-Mail-Konfiguration verfügbar")
    return False
