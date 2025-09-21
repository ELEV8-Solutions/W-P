# Lohnabrechnung Konverter API

Eine FastAPI-Anwendung für die Konvertierung von Lohnabrechnungs-Excel-Dateien zu CSV mit automatischem E-Mail-Versand. Optimiert für Vercel Deployment.

## 🚀 Features

- **Excel zu CSV Konvertierung**: Automatische Verarbeitung von Lohnabrechnungsdaten
- **E-Mail-Versand**: Automatischer Versand der konvertierten Datei
- **Automatische Erkennung**: Abrechnungsmonat wird automatisch aus Excel-Datei erkannt
- **Deutsche Formatierung**: Korrekte Zahlenformatierung mit Komma als Dezimaltrennzeichen
- **RESTful API**: Einfache Integration in bestehende Systeme
- **Vercel-optimiert**: Serverless deployment ready

## 📁 Projektstruktur

```
/
├── api/
│   └── index.py              # Vercel Entry Point
├── app/
│   ├── api/
│   │   ├── routes.py         # Main Router
│   │   └── endpoints/
│   │       ├── users.py      # Benutzer-Endpoints (Demo)
│   │       ├── items.py      # Items-Endpoints (Demo)
│   │       └── payroll.py    # Lohnabrechnung-Endpoints
│   ├── models/
│   │   ├── user.py           # User Models (Demo)
│   │   ├── item.py           # Item Models (Demo)
│   │   └── payroll.py        # Payroll Models
│   ├── services/
│   │   ├── user_service.py   # User Service (Demo)
│   │   ├── item_service.py   # Item Service (Demo)
│   │   ├── payroll_service.py # Payroll Conversion Logic
│   │   └── email_service.py  # Email Service
│   ├── config.py             # App Configuration
│   ├── database.py           # Database Config
│   └── utils.py              # Utility Functions
├── main.py                   # FastAPI App
├── requirements.txt          # Python Dependencies
├── vercel.json              # Vercel Configuration
├── .env.example             # Environment Variables Template
├── .gitignore
└── README.md
```

## 🛠️ Installation

1. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Umgebungsvariablen konfigurieren:**
   ```bash
   cp .env.example .env
   # Bearbeiten Sie .env mit Ihren Einstellungen
   ```

## 🏃 Lokale Entwicklung

**Server starten:**
```bash
uvicorn main:app --reload
```

Die API ist dann verfügbar unter:
- API: http://localhost:8000
- Dokumentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

## 🌐 Vercel Deployment

1. **Vercel CLI installieren:**
   ```bash
   npm i -g vercel
   ```

2. **Projekt deployen:**
   ```bash
   vercel
   ```

3. **Umgebungsvariablen in Vercel setzen:**
   - Gehen Sie zu Ihrem Vercel Dashboard
   - Navigieren Sie zu Settings > Environment Variables
   - Fügen Sie Ihre Produktionsumgebungsvariablen hinzu

## 📚 API Endpoints

### Lohnabrechnung Konvertierung
- `POST /api/payroll/convert` - Excel zu CSV konvertieren und per E-Mail senden
- `POST /api/payroll/test-email` - E-Mail-Konfiguration testen

### Demo Endpoints (optional)
- `GET/POST /api/users` - Benutzer-Verwaltung
- `GET/POST /api/items` - Item-Verwaltung

## 🔧 API Verwendung

### Excel-Datei konvertieren

```bash
curl -X POST "http://localhost:8000/api/payroll/convert" \
  -F "file=@Lohnabrechnung_August.xlsx" \
  -F "email=empfaenger@beispiel.de" \
  -F "mandant=10001" \
  -F "abrechnungsmonat=202408" \
  -F "sheet_name=Tabelle1"
```

**Parameter:**
- `file` (required): Excel-Datei (.xlsx, .xls)
- `email` (required): E-Mail-Adresse für Versand
- `mandant` (optional): Mandantennummer (Standard: "10001")
- `abrechnungsmonat` (optional): Format YYYYMM (automatisch erkannt wenn leer)
- `sheet_name` (optional): Excel-Arbeitsblatt (Standard: "Tabelle1")

**Response:**
```json
{
  "message": "Konvertierung erfolgreich abgeschlossen",
  "rows_processed": 150,
  "abrechnungsmonat": "202408",
  "email_sent": true,
  "output_filename": "lohnabrechnung_202408_10001.csv"
}
```

### E-Mail testen

```bash
curl -X POST "http://localhost:8000/api/payroll/test-email" \
  -F "email=test@beispiel.de"
```

## 📧 E-Mail Konfiguration

### Gmail Setup:
1. Gmail-Konto mit 2-Faktor-Authentifizierung aktivieren
2. App-Passwort generieren: https://myaccount.google.com/apppasswords
3. App-Passwort in `.env` eintragen:

```env
SENDER_EMAIL=your-gmail@gmail.com
SENDER_PASSWORD=your-16-digit-app-password
```

### Andere E-Mail-Provider:
Passen Sie SMTP-Einstellungen in `app/config.py` an.

## 🔧 Konfiguration

### Vercel-spezifische Dateien:
- `api/index.py` - Entry Point für Vercel
- `vercel.json` - Vercel Deployment-Konfiguration

### Wichtige Einstellungen:
- Python Runtime: 3.9
- Alle Requests werden an `/api/index.py` weitergeleitet
- CORS ist für Entwicklung konfiguriert (anpassen für Produktion)

## 🔒 Sicherheit

- Ändern Sie `SECRET_KEY` in Produktionsumgebung
- Konfigurieren Sie CORS für spezifische Domains
- Implementieren Sie Authentication/Authorization nach Bedarf

## 📝 Nächste Schritte

1. **E-Mail-Konfiguration einrichten:** Gmail App-Passwort generieren
2. **Tests implementieren:** pytest für API-Tests
3. **Logging hinzufügen:** strukturiertes Logging für Debugging
4. **Rate Limiting:** für API-Schutz in Produktion
5. **Authentication:** JWT für geschützte Endpoints
6. **Error Handling:** erweiterte Fehlerbehandlung

## 🤝 Beitragen

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Pushen Sie den Branch
5. Erstellen Sie einen Pull Request

## 📄 Lizenz

MIT License
