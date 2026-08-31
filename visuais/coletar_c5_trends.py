"""Coleta bruta pra C5 (geo-lift): 'Paul McCartney' no Google Trends, por
regiao (estado/provincia), Brasil + Mexico. Escopo reduzido de Brasil+Mexico+
Argentina para Brasil+Mexico nesta sessao: os codigos de regiao da Argentina
(AR-C, AR-X, AR-S, AR-M) bateram em rate-limit (429/bloqueio "sorry") de forma
persistente mesmo com backoff longo; documentado em referencias.md.

Uma unica janela larga por regiao (2023-08-01 a 2025-02-01) cobre as duas
levas da turne Got Back (nov-dez/2023 e out-nov/2024). Normalizacao do Trends
e por query (max da janela = 100), entao razoes pre/pos dentro de uma mesma
serie sao comparaveis entre regioes mesmo com essa janela larga compartilhada.

Saida: dados/paul_geolift_trends_raw.csv, formato longo
  geo, label, country, is_treated, event_date, date, interest
"""
import time
import pandas as pd
from pytrends.request import TrendReq

TIMEFRAME = "2023-08-01 2025-02-01"
TERM = "Paul McCartney"

# geo, label, pais, tratado?, data do show (None p/ controle)
REGIONS = [
    ("BR-DF", "Brasilia", "BR", True, "2023-11-30"),
    ("BR-MG", "Belo Horizonte", "BR", True, "2023-12-03"),
    ("BR-SP", "Sao Paulo", "BR", True, "2023-12-07"),
    ("BR-PR", "Curitiba", "BR", True, "2023-12-13"),
    ("BR-RJ", "Rio de Janeiro", "BR", True, "2023-12-16"),
    ("BR-SC", "Florianopolis", "BR", True, "2024-10-19"),
    ("MX-DIF", "Cidade do Mexico", "MX", True, "2023-11-14"),
    ("MX-NLE", "Monterrey (Guadalupe)", "MX", True, "2024-11-08"),
    ("BR-BA", "Salvador (controle)", "BR", False, None),
    ("BR-PE", "Recife (controle)", "BR", False, None),
    ("BR-CE", "Fortaleza (controle)", "BR", False, None),
    ("BR-RS", "Porto Alegre (controle)", "BR", False, None),
    ("BR-AM", "Manaus (controle)", "BR", False, None),
    ("MX-JAL", "Guadalajara (controle)", "MX", False, None),
]

pt = TrendReq(hl="en-US", tz=0, retries=3, backoff_factor=1.0)
rows = []
for geo, label, country, is_treated, event_date in REGIONS:
    ok = False
    for attempt in range(3):
        try:
            pt.build_payload([TERM], timeframe=TIMEFRAME, geo=geo)
            df = pt.interest_over_time()
            ok = True
            break
        except Exception as e:
            print(f"{geo} tentativa {attempt+1} falhou: {e}")
            time.sleep(30 * (attempt + 1))
    if not ok or df.empty:
        print(f"{geo} SEM DADO (pulado)")
        continue
    for date, val in df[TERM].items():
        rows.append(dict(geo=geo, label=label, country=country,
                          is_treated=is_treated, event_date=event_date,
                          date=date.date(), interest=val))
    print(f"{geo} OK: {len(df)} semanas, media {df[TERM].mean():.1f}")
    time.sleep(15)

out = pd.DataFrame(rows)
out.to_csv("dados/paul_geolift_trends_raw.csv", index=False)
print("salvo dados/paul_geolift_trends_raw.csv:", out.shape, out['geo'].nunique(), "regioes")
