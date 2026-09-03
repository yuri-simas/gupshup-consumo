# -*- coding: utf-8 -*-
"""Injeta dados.json (e o logo) nos templates e gera as paginas publicadas.

    python src/build.py

Rode a partir da raiz do projeto, depois de atualizar dados.json.
Para gerar dados.json a partir de um extrato novo, use src/csv_para_json.py.
"""
import io
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ler(*partes):
    return io.open(os.path.join(RAIZ, *partes), encoding="utf-8").read()


def escrever(nome, conteudo):
    caminho = os.path.join(RAIZ, nome)
    io.open(caminho, "w", encoding="utf-8").write(conteudo)
    print("  %-16s %8d bytes" % (nome, os.path.getsize(caminho)))


def main():
    dados = ler("dados.json").strip()
    logo = ler("src", "logo.txt").strip()

    print("gerando:")

    # O deck e a pagina principal do site.
    deck = ler("src", "deck.template.html")
    assert "__DATA__" in deck and "__LOGO__" in deck, "deck.template.html sem marcadores"
    escrever("index.html", deck.replace("__DATA__", dados).replace("__LOGO__", logo))

    rateio = ler("src", "rateio.template.html")
    assert "__DATA__" in rateio, "rateio.template.html sem marcador __DATA__"
    escrever("rateio.html", rateio.replace("__DATA__", dados))


if __name__ == "__main__":
    main()
