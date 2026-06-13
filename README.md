# 🎸 beatlenomics

A side project where I point the tools of economics and data analysis at The Beatles and Paul McCartney.

Each entry takes one question (how often does Paul play each song, how concentrated is his setlist, how much of his stage time still belongs to The Beatles) and answers it with real data, a clear chart, and one economic idea. The series runs on my LinkedIn as **#beatlenomics**.

I am [Tanise Bussmann](https://www.linkedin.com/in/tanisebussmann), a data scientist and economist. By day I measure market concentration in antitrust cases. This is the same toolkit, applied to something I love.

## What's inside

| Post | Question | Key finding |
|------|----------|-------------|
| 04 | What does Paul McCartney play live, and how concentrated is it? | Gini of 0.77 across 373 songs. Half of them account for 1% of his stage time. |

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
