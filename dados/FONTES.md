# Fontes dos dados

Cada CSV nesta pasta tem uma coluna `fonte` por linha. Este arquivo documenta o contexto completo: o que cada dataset contém, de onde vieram os números, e quando foram coletados.

---

## paul_setlist_full.csv

Setlist completo de Paul McCartney ao vivo: 373 músicas, 30.369 performances.

- **Origem:** [setlist.fm](https://www.setlist.fm) (dados logados por fãs; tratados como piso, não contagem exata)
- **Coleta:** jun/2026, via `curl` com user-agent de navegador (WebFetch retorna 403)
- **Usado em:** post 04 (concentração de setlist, Gini 0,77)

## paul_setlist_top52.csv

Top 52 músicas mais tocadas ao vivo pelo Paul, com contagem de performances e era (Beatles/Wings/solo).

- **Origem:** derivado de `paul_setlist_full.csv`
- **Coleta:** jun/2026
- **Usado em:** post 04

## beatles_autoria.csv

Créditos de composição das músicas dos Beatles, por compositor.

- **Origem:** Wikipedia (discografia dos Beatles), com contagens cruzadas em Far Out Magazine e UNCUT
- **Coleta:** jun/2026
- **Usado em:** post 05 (concentração de autoria, 88% Lennon-McCartney)

## northern_songs_transacoes.csv

Timeline de transações de propriedade do catálogo Beatles/Northern Songs (1963-2016), com valores originais, ajustados por inflação, e preço por música.

- **Origem:**
  - Beatles Bible: cronologia da perda de controle (1969), valores das transações ATV
  - HISTORY.com, Billboard, PMA Magazine: compra por Michael Jackson (1985), US$47,5M, ~4.000 músicas, 251 Lennon-McCartney
  - NPR, Rolling Stone: venda do estate de Jackson para Sony (2016), US$750M
  - Wikipedia: Northern Songs (fundação, IPO, dissolução), Sony Music Publishing
  - BLS CPI Inflation Calculator: ajuste inflacionário 1985→2016 (fator 2,27)
- **Coleta:** 27/jun/2026
- **Cálculos próprios:** CAGR nominal (11,8%), real (8,9%), preço por música (US$11.875 → US$375.000, 32x)
- **Usado em:** post 07 (quem é dono dos Beatles)

## beatles_spotify_comparativo.csv

Comparação de artistas em vendas totais, streams Spotify, monthly listeners, tamanho do catálogo, e métricas derivadas (vendas/ano, streams/música, streams/ano).

- **Origem:**
  - Wikipedia: List of best-selling music artists (vendas totais)
  - mystreamcount.com: Beatles total streams (~25,8B)
  - TooXclusive: Beatles 10M monthly listeners (21/mai/2026); Queen 50M (21/mai/2026)
  - ChartMasters: Queen total streams (~29,2B), ranking de artistas
  - Variety / Spotify Newsroom (abr/2026): Taylor Swift 100B+, Drake 100B+, monthly listeners
  - RIAA: Taylor Swift certified units
- **Coleta:** 27/jun/2026
- **Cálculos próprios:** vendas/ano de carreira, streams/música original, streams/ano no Spotify, ratio Taylor Swift / Beatles
- **Nota:** streams do Spotify são dinâmicos; os valores aqui são um snapshot de jun/2026
- **Usado em:** post 11 (it never gets old)

## nowandthen_trends_raw.csv

Google Trends semanal (`interest_over_time`) para "The Beatles", "The Rolling
Stones", "Led Zeppelin", "Pink Floyd", mundial, 2023-05-28 a 2024-02-25.

- **Origem:** pytrends (Google Trends), consulta conjunta (mesma normalização
  0-100 dos 4 termos).
- **Coleta:** 17/jul/2026.
- **Usado em:** post C4 (Now and Then, efeito halo). Ver
  `posts/c4-nowandthen-halo/referencias.md` para o desenho (DiD, mesmo
  estimador do C3) e as ressalvas (contaminação da semana do teaser).

## paul_geolift_trends_raw.csv

Google Trends semanal (`interest_over_time`) para "Paul McCartney", por
estado/região (Brasil + México), 2023-08-01 a 2025-02-01, formato longo.

- **Origem:** pytrends (Google Trends), uma chamada por região (termo único,
  sem combinar). Datas de show vêm da Wikipedia ("Got Back", turnê de Paul
  McCartney) — ver `posts/c5-geolift-shows/referencias.md`.
- **Coleta:** 17/jul/2026. Escopo reduzido de Brasil+México+Argentina para
  Brasil+México nesta sessão: códigos de região da Argentina bateram em
  rate-limit persistente do Google Trends.
- **Usado em:** post C5 (geo-lift). O post não confirma o efeito geográfico
  esperado — o achado foi que o grupo de controle não estava isolado do
  tratamento (cobertura de imprensa nacional). Ver referencias.md do post
  para a tentativa original de DiD por evento e por que foi abandonada.

---

## Comparações de asset classes (usadas no post 07, não em CSV separado)

- **S&P 500 CAGR 1985-2016:** ~11,1% nominal, ~8,4% real (moneychimp.com, slickcharts.com)
- **Ouro:** US$317/oz (1985) → US$1.251/oz (2016) = CAGR 4,5% (sdbullion.com, macrotrends.net)
- **Imóveis EUA:** ~3,5% real anual (Case-Shiller, FRED/St. Louis Fed, série CSUSHPINSA)
