# Rateio Gupshup

Custo de plataforma WhatsApp por Customer ID e por App, a partir do extrato *analytics* da Gupshup.
Duas páginas estáticas, sem backend — todo o cálculo roda no navegador.

**https://yuri-simas.github.io/gupshup-consumo/**

| Página | O que faz |
|---|---|
| [`index.html`](https://yuri-simas.github.io/gupshup-consumo/) | Gerador de apresentação executiva por cliente, na identidade da Orpen. Busca por nome de app, consolida vários Customer Ids e exporta o deck como HTML autônomo |
| [`rateio.html`](https://yuri-simas.github.io/gupshup-consumo/rateio.html) | Rateio geral: custo por cliente e por app, aberto por categoria de mensagem, em dólar e real |

Base publicada: extrato de **90 dias**, 888 apps em 391 Customer IDs. Os valores aparecem em **média mensal** (total ÷ 3) por padrão.

---

## Como o custo é montado

```
Total = Taxa Gupshup + Cloud API Marketing + WhatsApp Fee
```

Confere nas 888 linhas do extrato.

**Taxa Gupshup** é `US$ 0,001` por mensagem trocada — entradas, saídas e templates, tudo. Por isso quase não depende da categoria.

**Teto Gupshup:** `US$ 75 por app, por mês` — equivale a 75.000 mensagens ao preço unitário. Num extrato de 90 dias o teto vale `US$ 75 × 3 = US$ 225` por app.

> Validação: aplicar `min(taxa, US$ 225)` na base inteira dá US$ 34.342,56, contra US$ 34.481,08 do líquido real do extrato — 0,4% de diferença. A folga vem de apps que passaram de 75.000 mensagens em apenas alguns dos três meses.

## Custo Meta por categoria

O extrato traz a `WhatsApp Fee` como um número único, sem quebra por categoria. A quebra é calculada como `volume × tarifa`, com as tarifas inferidas do próprio extrato — isolando apps que enviaram uma única categoria no período:

| Categoria | Tarifa | Como foi obtida |
|---|---|---|
| Marketing | US$ 0,0625 | 32 apps isolados, p10 = p90 |
| MM Lite | US$ 0,0625 | 64 apps isolados — é marketing pela API Lite, em coluna separada |
| Utility paga | US$ 0,0068 | 34 apps isolados, p10 = p90 |
| Autenticação | US$ 0,0315 | não foi possível isolar (2.016 msg em 90 dias); tarifa de referência do Brasil |

O modelo fecha em **879 das 888 linhas** dentro de 3%. O resíduo da base é 4,8%, e US$ 3.482 dele vêm de um único app que envia para fora do Brasil — mensagens internacionais têm tarifa própria, que o extrato não mostra. Esse resíduo aparece nas páginas como **Outros / internacional**.

Não custam nada hoje: `Conversation Service`, `Free Utility Templates` (utility dentro da janela de atendimento aberta) e `Free entry points` (janela de 72h dos anúncios Click-to-WhatsApp).

## A mudança de 01/10/2026

A partir dessa data a Meta cobra por unidade as **mensagens de serviço** (respostas de texto livre dentro da janela de 24h) e os **templates de utility enviados com a janela já aberta**. A tarifa do Brasil foi confirmada em `US$ 0,0068` por mensagem — a mesma de Utility, sem desconto por volume. O campo é editável nas duas páginas.

O teto da Gupshup continua valendo, mas cobre só a camada Gupshup: a cobrança da Meta é uma camada separada, **sem teto**.

## Atualizar com um extrato novo

Sem tocar no repositório — arraste o CSV na página. Ela recalcula na hora, e nada sai da sua máquina.

Para atualizar a versão publicada:

```bash
python src/csv_para_json.py "caminho/analytics.csv"
python src/build.py
```

Confira o campo **Dias** no cabeçalho, que define o divisor da média mensal, e commite `dados.json`, `index.html` e `rateio.html`.

## Estrutura

```
index.html                 gerador de deck (gerado)
rateio.html                rateio geral (gerado)
dados.json                 extrato convertido, 19 campos por app
src/rateio.template.html   fonte do rateio, com o marcador __DATA__
src/deck.template.html     fonte do deck, com __DATA__ e __LOGO__
src/logo.txt              logo da Orpen em data URI
src/csv_para_json.py       CSV da Gupshup → dados.json
src/build.py               templates + dados → páginas publicadas
```

Edite sempre os arquivos em `src/` — `index.html` e `rateio.html` são gerados e qualquer alteração direta neles se perde no próximo build.

## Exportar um deck

**Exportar HTML** baixa a apresentação do cliente escolhido como um arquivo `.html` autônomo: leva o CSS, o logo em data URI e a navegação por teclado. Abre offline, em qualquer navegador, sem depender deste site.

**Exportar PDF** abre a impressão do navegador — escolha *Salvar como PDF* no destino. Sai em A4 paisagem, um slide por página, com o texto vetorial e selecionável. A tecla `P` faz o mesmo, aqui e no arquivo exportado.

> Não usamos biblioteca de PDF no navegador de propósito: `html2canvas` rasterizaria os seis slides, deixando o arquivo pesado e o texto sem seleção. A impressão nativa preserva fonte, cor e vetor.
