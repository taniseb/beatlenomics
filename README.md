# 🎸 beatlenomics

A side project where I point the tools of economics and data analysis at The Beatles and Paul McCartney.

Each entry takes one question (how often does Paul play each song, how concentrated is his setlist, how much of his stage time still belongs to The Beatles) and answers it with real data, a clear chart, and one economic idea. The series runs on my LinkedIn as **#beatlenomics**.

I am [Tanise Bussmann](https://www.linkedin.com/in/tanisebussmann), a data scientist and economist. By day I measure market concentration in antitrust cases. This is the same toolkit, applied to something I love.

## The series

| Date | Question | Key number | LinkedIn | Code & chart |
|------|----------|------------|----------|--------------|
| 22/06/2026 | What does Paul McCartney play live, and how concentrated is it? | Gini coefficient of 0.77 across 373 songs | [LinkedIn](https://www.linkedin.com/in/tanisebussmann/recent-activity/all/) | [code](visuais/gerar_04c_lorenz_v2.py) · [chart](visuais/04c_lorenz_v2.png) |
| 25/06/2026 | How concentrated was Beatles songwriting? | Lennon-McCartney wrote 88% of the catalogue | [LinkedIn](https://www.linkedin.com/in/tanisebussmann/recent-activity/all/) | [code](visuais/gerar_05_autoria.py) · [chart](visuais/05_autoria.png) |
| 28/06/2026 | Who owns the Beatles? | The catalogue returned 11.8% CAGR over 31 years, beating gold and matching the S&P 500 | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_%F0%9D%97%AA%F0%9D%97%B5%F0%9D%97%BC-%F0%9D%97%BC%F0%9D%98%84%F0%9D%97%BB%F0%9D%98%80-%F0%9D%98%81%F0%9D%97%B5%F0%9D%97%B2-%F0%9D%97%95%F0%9D%97%B2%F0%9D%97%AE%F0%9D%98%81%F0%9D%97%B9%F0%9D%97%B2%F0%9D%98%80-in-share-7477329455712157697-X8RZ) | [code](visuais/gerar_07_catalogo.py) · [chart](visuais/07_catalogo.png) |
| 01/07/2026 | It never gets old. But does it never get old? | 600M records sold, but not in Spotify's top 50. Here Comes the Sun still gets 472k plays per day. | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_beatlenomics-share-7477331722964066304-nJjF) | [code](visuais/gerar_11_stock_flow.py) · [chart](visuais/11_stock_flow.png) |
| 06/07/2026 | Did Get Back move the catalogue? | Diff-in-diff: +23.5 index points, a 63% lift in Beatles searches over the 8 weeks after the documentary dropped | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_beatlenomics-causalinference-datascience-share-7479561930920288257-Q2Dy) | [code](visuais/gerar_c3_getback.py) · [chart](visuais/c3_getback.png) |
| 09/07/2026 | Was the Get Back effect real, or a fluke of the method? | Placebo test: 63 fake treatment dates came back near zero; the real effect sat 9.3 standard deviations out | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_beatlenomics-causalinference-datascience-ugcPost-7479561731455938562-uumP) | [code](visuais/gerar_c6_lines.py) · [chart](visuais/c6_lines.png) |
| 16/07/2026 | Did the Bohemian Rhapsody movie actually move Queen's streams? | Synthetic control: real Queen ran ~1.4x above its synthetic counterfactual for 16 weeks after release | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_bohemian-rhapsody-synthetic-control-in-share-7482410755561222145-8tZl) | [code](visuais/gerar_c1_queen.py) · [chart](visuais/c1_queen.png) |
| 20/07/2026 | I saw Paul McCartney live 13 times. Which songs never left the setlist? | Across 85 songs played over 13 shows, only 12 showed up every single time | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_beatlenomics-thebeatles-paulmccartney-ugcPost-7482411385252048896-Kyl7) | [code](visuais/gerar_13shows.py) · [chart](visuais/13shows_top.png) |
| 23/07/2026 | Did "Now and Then" lift searches for the whole Beatles catalogue? | Diff-in-diff: searches lifted ~30% pre-release on the teaser alone, still above baseline 3 months out | [LinkedIn](https://www.linkedin.com/posts/tanisebussmann_beatlenomics-causalinference-datascience-share-7484001998221176832-uH7y/) | [code](visuais/gerar_c4_nowandthen.py) · [chart](visuais/c4_nowandthen.png) |

More posts are on the way.

## How it works

- `dados/` — datasets compiled from public sources, one CSV per topic
- `visuais/` — the chart scripts (`gerar_*.py`) and the final PNGs
- `visuais/beatlenomics_style.py` — the shared visual identity for the series

Every figure is reproducible. Run a script from the project root:

```bash
PYTHONPATH=visuais python3 visuais/gerar_04c_lorenz_v2.py
```

## Data

Numbers come from publicly documented setlists on [setlist.fm](https://www.setlist.fm). The counts are fan logged, so they are best read as floors rather than exact totals. Each post folder records its sources.

## License

Code under MIT. The data belongs to its original sources.
