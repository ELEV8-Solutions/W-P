#!/usr/bin/env python3
from fastapi import UploadFile, File, Form, HTTPException
import tempfile
import os
from typing import Optional
from workflows.payroll_converter import convert_excel_to_csv
from workflows.email_service import send_email

async def process_payroll_conversion(
    file: UploadFile,
    email: str,
    mandant: str = "10001",
    abrechnungsmonat: Optional[str] = None,
    sheet_name: str = "Tabelle1"
) -> dict:
    """
    Hauptfunktion für die Lohnabrechnung-Konvertierung
    """
    # Validierungen
    if not file.filename:
        raise HTTPException(status_code=400, detail="Keine Datei ausgewählt")
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Nur Excel-Dateien (.xlsx, .xls) sind erlaubt")
    
    if not email or "@" not in email:
        raise HTTPException(status_code=400, detail="Gültige E-Mail-Adresse erforderlich")
    
    # Temporäre Datei erstellen
    input_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.xlsx', delete=False)
    output_file_path = None
    
    try:
        # Datei speichern
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Datei ist leer")
        
        input_file.write(content)
        input_file.close()
        
        # Konvertieren
        output_file_path, rows_count, detected_abrechnungsmonat = convert_excel_to_csv(
            input_file.name, mandant, abrechnungsmonat, sheet_name
        )
        
        if rows_count == 0:
            raise HTTPException(status_code=400, detail="Keine gültigen Daten in der Excel-Datei gefunden")
        
        # E-Mail senden
        email_sent = send_email(email, output_file_path, detected_abrechnungsmonat, rows_count)
        
        return {
            "message": "Erfolgreich konvertiert",
            "rows_processed": rows_count,
            "abrechnungsmonat": detected_abrechnungsmonat,
            "email_sent": email_sent,
            "filename": f"lohnabrechnung_{detected_abrechnungsmonat}.csv"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unerwarteter Fehler: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fehler bei der Verarbeitung: {str(e)}")
    
    finally:
        # Aufräumen
        try:
            if os.path.exists(input_file.name):
                os.unlink(input_file.name)
            if output_file_path and os.path.exists(output_file_path):
                os.unlink(output_file_path)
        except Exception as e:
            print(f"Fehler beim Aufräumen: {str(e)}")
