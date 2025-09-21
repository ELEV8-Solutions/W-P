import pandas as pd
import os
from fastapi import UploadFile
from tempfile import NamedTemporaryFile

def convert_essensgeld_from_upload(file: UploadFile, mandant="10001", abrechnungsmonat=None) -> str:
    """
    Nimmt eine Excel-Datei (UploadFile), konvertiert sie ins gewünschte Format und gibt den Pfad zur Ausgabedatei zurück.
    """
    # Speichere Upload temporär
    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    df = pd.read_excel(tmp_path, sheet_name="Tabelle1")
    df.columns = df.columns.astype(str).str.strip()

    if not abrechnungsmonat:
        abrechnungsmonat = pd.Timestamp.today().strftime("%Y%m")

    rows_out = []
    for _, row in df.iterrows():
        personalnummer = str(row["Personalnummer"]).strip() if pd.notna(row["Personalnummer"]) else ""
        if "Summe Essensgeld PK" in df.columns:
            betrag_val = row["Summe Essensgeld PK"]
        else:
            betrag_col = [c for c in df.columns if "Essensgeld" in c][0]
            betrag_val = row[betrag_col]

        if pd.notna(betrag_val) and float(betrag_val) != 0:
            betrag = f"{float(betrag_val):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            einheit = "EUR"
            lohnart = "111"
            kostenstelle = ""
            rows_out.append([
                mandant, personalnummer, abrechnungsmonat, lohnart, betrag, einheit, kostenstelle
            ])

    out_df = pd.DataFrame(rows_out, columns=[
        "Mandant","Personalnummer","Abrechnungsmonat","Lohnart","Betrag","Einheit","Kostenstelle"
    ])

    # Speichere als temporäre CSV
    output_path = tmp_path.replace('.xlsx', '_essensgeld.txt')
    out_df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    return output_path
