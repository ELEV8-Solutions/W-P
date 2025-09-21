import pandas as pd
import re
from fastapi import UploadFile
from tempfile import NamedTemporaryFile
import os

def convert_pfleger_from_upload(file: UploadFile, mandant="10001", abrechnungsmonat=None) -> str:
    """
    Nimmt eine Excel-Datei (UploadFile), konvertiert sie ins gewünschte Format und gibt den Pfad zur Ausgabedatei zurück.
    """
    # Speichere Upload temporär
    with NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        tmp.write(file.file.read())
        tmp_path = tmp.name

    if not abrechnungsmonat:
        abrechnungsmonat = pd.Timestamp.today().strftime("%Y%m")

    df = pd.read_excel(tmp_path, sheet_name="Tabelle1", header=None)
    lohnarts = df.iloc[1].astype(str).fillna("")

    rows_out = []
    for ridx in range(2, len(df)):
        personalnummer = df.iloc[ridx, 0]
        kostenstelle = df.iloc[ridx, 3] if df.shape[1] > 3 else ""
        if pd.isna(personalnummer):
            continue
        for c in range(4, df.shape[1]):
            lohn_code = lohnarts[c]
            lohnart = re.sub(r"\D", "", str(lohn_code))
            if lohnart == "":
                continue
            val = df.iloc[ridx, c]
            if pd.isna(val):
                continue
            if isinstance(val, (int, float)):
                num_val = float(val)
            elif isinstance(val, str):
                try:
                    num_val = float(val.replace(",", "."))
                except ValueError:
                    continue
            else:
                continue
            betrag = f"{num_val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            einheit = "STD" if c in (4, 5) else "EUR"
            rows_out.append([
                mandant,
                str(int(personalnummer)),
                abrechnungsmonat,
                lohnart,
                betrag,
                einheit,
                "" if pd.isna(kostenstelle) else str(kostenstelle)
            ])
    out_df = pd.DataFrame(rows_out, columns=[
        "Mandant","Personalnummer","Abrechnungsmonat","Lohnart","Betrag","Einheit","Kostenstelle"
    ])
    output_path = tmp_path.replace('.xlsx', '_pfleger.txt')
    out_df.to_csv(output_path, sep=";", index=False, encoding="utf-8")
    return output_path
