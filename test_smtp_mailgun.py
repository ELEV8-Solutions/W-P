#!/usr/bin/env python3
"""
Test-Script für SMTP E-Mail Integration (Mailgun SMTP)
"""
import os
from dotenv import load_dotenv

# Environment laden
load_dotenv()

# Email service importieren
from workflows.email_service import send_simple_email_smtp

def test_smtp():
    """Testet die SMTP-Integration"""
    print("🧪 Teste SMTP E-Mail Service...")
    
    # Konfiguration prüfen
    required_vars = ["SENDER_EMAIL", "SENDER_PASSWORD", "SMTP_SERVER", "SMTP_PORT"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Fehlende Umgebungsvariablen: {', '.join(missing_vars)}")
        return False
    
    print("✅ SMTP-Konfiguration vollständig")
    print(f"📧 SMTP Server: {os.getenv('SMTP_SERVER')}:{os.getenv('SMTP_PORT')}")
    print(f"👤 Sender: {os.getenv('SENDER_EMAIL')}")
    
    # Test-E-Mail senden
    test_email = input("Geben Sie eine Test-E-Mail-Adresse ein: ").strip()
    
    if not test_email:
        print("❌ Keine E-Mail-Adresse eingegeben")
        return False
    
    subject = "SMTP Test - Lohnabrechnung API"
    body = """
Hallo!

Dies ist eine Test-E-Mail von der Lohnabrechnung API über SMTP.

Wenn Sie diese E-Mail erhalten, funktioniert die SMTP-Integration korrekt.

Mit freundlichen Grüßen,
OTQ GmbH
    """
    
    print(f"📧 Sende Test-E-Mail an {test_email}...")
    
    success = send_simple_email_smtp(test_email, subject, body)
    
    if success:
        print(f"✅ Test-E-Mail erfolgreich gesendet!")
        print(f"📬 Prüfen Sie das Postfach von {test_email}")
        return True
    else:
        print("❌ E-Mail-Versand fehlgeschlagen")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("SMTP E-MAIL TEST")
    print("=" * 50)
    
    try:
        test_smtp()
    except KeyboardInterrupt:
        print("\n⏹️  Test abgebrochen")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {str(e)}")
    
    print("\nTest beendet.")
