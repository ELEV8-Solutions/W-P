#!/usr/bin/env python3
import tempfile
import os
import math
import re
import pandas as pd
from datetime import datetime
from typing import Optional, Tuple

def detect_abrechnungsmonat(file_path: str) -> Optional[str]:
    """Erkennt den Abrechnungsmonat aus der Excel-Datei"""
    try:
        raw = pd.read_excel(file_path, sheet_name="Tabelle1", header=None)
        for r in range(min(3, raw.shape[0])):
            for c in range(raw.shape[1]):
                v = raw.iloc[r, c]
                if pd.isna(v):
                    continue
                if isinstance(v, (pd.Timestamp, datetime)):
                    dt = pd.to_datetime(v)
                    return f"{dt.year}{dt.month:02d}"
                if isinstance(v, str):
                    m = re.search(r"(\d{4})[.\-/](\d{2})[.\-/](\d{2})", v)
                    if m:
                        return f"{int(m.group(1))}{int(m.group(2)):02d}"
    except Exception as e:
        print(f"Fehler beim Erkennen des Abrechnungsmonats: {str(e)}")
    return None

def is_number(val) -> bool:
    """Prüft ob ein Wert eine Nummer ist"""
    return isinstance(val, (int, float)) and not (isinstance(val, float) and math.isnan(val))

def format_number_german(val) -> str:
    """Formatiert Zahlen im deutschen Format"""
    try:
        num = float(val)
        s = f"{num:,.2f}"  
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return s
    except Exception:
        return str(val)

def convert_excel_to_csv(input_file_path: str, mandant: str, abrechnungsmonat: Optional[str], sheet_name: str) -> Tuple[str, int, str]:
    """Konvertiert Excel zu CSV"""
    # Abrechnungsmonat ermitteln
    if abrechnungsmonat is None:
        abrechnungsmonat = detect_abrechnungsmonat(input_file_path)
    if not abrechnungsmonat:
        abrechnungsmonat = f"{datetime.now().year}{datetime.now().month:02d}"

    # Excel einlesen
    df = pd.read_excel(input_file_path, sheet_name=sheet_name, header=3)
    header_row = df.iloc[0].astype(str).fillna("")
    data = df.iloc[1:].reset_index(drop=True).copy()

    # Lohnart-Spalten finden
    lohnart_cols = [i for i, h in enumerate(header_row) if str(h).strip().lower() == "lohnart"]

    rows_out = []
    
    for ridx in range(len(data)):
        row = data.iloc[ridx]
        
        # Personalnummer
        personal_raw = row.iloc[0]
        if pd.isna(personal_raw):
            personalnummer = ""
        else:
            if isinstance(personal_raw, (int, float)) and float(personal_raw).is_integer():
                personalnummer = str(int(personal_raw))
            else:
                personalnummer = str(personal_raw).strip()
        
        # Kostenstelle
        kostenstelle = "" if pd.isna(row.iloc[1]) else str(row.iloc[1]).strip()

        # Lohnarten sammeln
        row_lohn_codes = set()
        for i in lohnart_cols:
            v = row.iloc[i]
            if pd.notna(v) and isinstance(v, (int, float)) and float(v).is_integer():
                row_lohn_codes.add(int(v))

        # Für jede Lohnart
        for i in lohnart_cols:
            lohn_val = row.iloc[i]
            if pd.isna(lohn_val):
                continue
            
            try:
                lohnart = str(int(float(lohn_val)))
            except Exception:
                lohnart = str(lohn_val).strip()

            betrag = ""
            einheit = ""
            
            # Betrag und Einheit suchen
            offsets = [1, -1, 2, -2, 3, -3]
            for off in offsets:
                j = i + off
                if j < 0 or j >= len(row) or j in lohnart_cols:
                    continue
                
                val = row.iloc[j]
                if pd.isna(val):
                    continue
                
                hdr = str(header_row[j]).strip().lower()

                # Stunden-Erkennung
                if isinstance(val, str) and val.strip().lower() == "h":
                    left = row.iloc[j - 1] if j - 1 >= 0 else None
                    right = row.iloc[j + 1] if j + 1 < len(row) else None
                    
                    if pd.notna(left) and is_number(left) and int(left) not in row_lohn_codes:
                        betrag = format_number_german(left)
                        einheit = "STD"
                        break
                    if pd.notna(right) and is_number(right) and int(right) not in row_lohn_codes:
                        betrag = format_number_german(right)
                        einheit = "STD"
                        break
                    continue

                if is_number(val):
                    if isinstance(val, (int, float)) and float(val).is_integer() and int(val) in row_lohn_codes:
                        continue
                    
                    if ("stunden" in hdr) or ("urlaubs" in hdr) or ("krankheit" in hdr):
                        betrag = format_number_german(val)
                        einheit = "STD"
                        break
                    
                    if ("euro" in hdr) or ("betrag" in hdr) or ("beleg" in hdr):
                        betrag = format_number_german(val)
                        einheit = "EUR"
                        break
                    
                    if isinstance(val, float) and not float(val).is_integer():
                        betrag = format_number_german(val)
                        einheit = "EUR"
                        break
                    
                    betrag = format_number_german(val)
                    einheit = "EUR"
                    break

            rows_out.append([mandant, personalnummer, abrechnungsmonat, lohnart, betrag, einheit, kostenstelle])

    # DataFrame erstellen
    out_df = pd.DataFrame(
        rows_out,
        columns=["Mandant", "Personalnummer", "Abrechnungsmonat", "Lohnart", "Betrag", "Einheit", "Kostenstelle"],
    )
    out_df = out_df[(out_df["Betrag"].astype(str).str.strip() != "") & (out_df["Einheit"].astype(str).str.strip() != "")]

    # CSV schreiben
    output_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8')
    output_file_path = output_file.name
    output_file.close()
    
    out_df.to_csv(output_file_path, sep=";", index=False, encoding="utf-8")
    
    return output_file_path, len(out_df), abrechnungsmonat
