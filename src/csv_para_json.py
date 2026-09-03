# -*- coding: utf-8 -*-
"""Converte o CSV de analytics da Gupshup em dados.json.

    python src/csv_para_json.py "caminho/analytics.csv"

Depois rode `python src/build.py` para regerar as paginas.
As paginas tambem leem o CSV direto no navegador (botao "Importar extrato CSV"),
entao este script so e necessario para atualizar a versao publicada.
"""
import csv
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# A ordem aqui e a mesma que as paginas esperam. Nao reordene sem ajustar o JS.
COLUNAS = [
    "App Name", "App Id", "Customer Id",
    "Session Outgoing Messages", "Session Incoming Messages", "Template Messages",
    "Marketing Templates", "Paid Utility Templates", "Free Utility Templates",
    "Authentication Templates", "Free entry points", "MM Lite",
    "Incoming Voice Minutes",
    "Gupshup Fee", "Gupshup fee for Cloud API – Marketing",
    "WhatsApp Fee", "Discount", "Total Fee",
    "Conversation Service",
]
TEXTO = {0, 1, 2}
DINHEIRO = {13, 14, 15, 16, 17}


def numero(s):
    s = str(s).replace("$", "").replace(",", "").strip()
    try:
        return float(s)
    except ValueError:
        return 0.0


def main():
    if len(sys.argv) < 2:
        sys.exit("uso: python src/csv_para_json.py <analytics.csv>")

    linhas = list(csv.DictReader(io.open(sys.argv[1], encoding="utf-8-sig")))
    if not linhas:
        sys.exit("CSV vazio.")

    faltando = [c for c in COLUNAS if c not in linhas[0]]
    if faltando:
        sys.exit("colunas ausentes no CSV: " + ", ".join(faltando))

    saida = []
    for linha in linhas:
        registro = []
        for i, coluna in enumerate(COLUNAS):
            valor = linha[coluna]
            if i in TEXTO:
                registro.append(valor)
            elif i in DINHEIRO:
                registro.append(round(numero(valor), 4))
            else:
                registro.append(int(round(numero(valor))))
        saida.append(registro)

    saida.sort(key=lambda r: -r[17])

    destino = os.path.join(RAIZ, "dados.json")
    io.open(destino, "w", encoding="utf-8").write(
        json.dumps(saida, ensure_ascii=False, separators=(",", ":"))
    )
    print("dados.json: %d apps, %d bytes" % (len(saida), os.path.getsize(destino)))
    print("agora rode: python src/build.py")


if __name__ == "__main__":
    main()
