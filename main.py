#!/usr/bin/env python3
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from workflows.payroll_workflow import process_payroll_conversion
from workflows.email_service import send_simple_email

app = FastAPI(
    title="Lohnabrechnung Konverter",
    description="API für Excel zu CSV Konvertierung mit E-Mail-Versand",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """API Info"""
    return {
        "message": "Lohnabrechnung Konverter API",
        "version": "1.0.0",
        "endpoints": {
            "convert": "/convert",
            "test_email": "/test-email",
            "health": "/health",
            "docs": "/docs"
        },
        "status": "ready"
    }

@app.get("/health")
async def health_check():
    """Health Check für Monitoring"""
    return {"status": "healthy", "service": "lohnabrechnung-konverter"}

@app.post("/convert")
async def convert_payroll(
    file: UploadFile = File(..., description="Excel-Datei"),
    email: str = Form(..., description="E-Mail-Adresse"),
    mandant: str = Form("10001", description="Mandant"),
    abrechnungsmonat: Optional[str] = Form(None, description="Abrechnungsmonat YYYYMM"),
    sheet_name: str = Form("Tabelle1", description="Arbeitsblatt")
):
    """Excel zu CSV konvertieren und per E-Mail senden"""
    return await process_payroll_conversion(file, email, mandant, abrechnungsmonat, sheet_name)

@app.post("/test-email")
async def test_email(
    email: str = Form(..., description="Test E-Mail-Adresse")
):
    """E-Mail-Konfiguration testen"""
    try:
        success = send_simple_email(
            recipient_email=email,
            subject="Test E-Mail - Lohnabrechnung Service",
            body="Dies ist eine Test-E-Mail. Wenn Sie diese erhalten, funktioniert die E-Mail-Konfiguration."
        )
        
        if success:
            return {"message": f"Test-E-Mail erfolgreich an {email} gesendet"}
        else:
            raise HTTPException(
                status_code=500,
                detail="E-Mail konnte nicht gesendet werden. Überprüfen Sie die Konfiguration."
            )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"E-Mail-Test fehlgeschlagen: {str(e)}")
