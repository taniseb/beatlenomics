# Notas — `paul_setlists_por_turne.csv`

Fonte usada para cada era de turnê (uma amostra representativa e completa por era, formato longo: uma linha por música por turnê). Todas as músicas foram conferidas diretamente no setlist.fm (via WebFetch da página do show) ou já estavam documentadas no próprio repositório — nenhuma música foi inventada ou estimada.

## Eras cobertas (12/12)

1. **Wings Over America (1976)** — Wings, Madison Square Garden, Nova York, 25/mai/1976 (perna americana do Wings Over America Tour; documentado no álbum ao vivo homônimo). 29 músicas.
   https://www.setlist.fm/setlist/wings/1976/madison-square-garden-new-york-ny-3bd7a02c.html

2. **The Paul McCartney World Tour (1989-1990)** — Madison Square Garden, Nova York, 14/dez/1989. 28 músicas.
   https://www.setlist.fm/setlist/paul-mccartney/1989/madison-square-garden-new-york-ny-63d7e687.html

3. **New World Tour (1993)** — Giants Stadium, East Rutherford (NJ), 11/jun/1993. 33 músicas (inclui trechos de banda/instrumentais que o setlist.fm lista como faixas próprias, ex. "Robbie's Bit (Thanks Chet)", "Good Rocking Tonight").
   https://www.setlist.fm/setlist/paul-mccartney/1993/giants-stadium-east-rutherford-nj-13dc0161.html

4. **Driving USA Tour (2002)** — Madison Square Garden, Nova York, 27/abr/2002. 36 músicas.
   https://www.setlist.fm/setlist/paul-mccartney/2002/madison-square-garden-new-york-ny-53ddb731.html

5. **Back in the World Tour (2003)** — Palais Omnisports de Paris-Bercy, Paris, 25/mar/2003. 37 músicas.
   **Substituição de escopo:** o pedido original agrupava "Back in the US / Back in the World, 2003". Na história real da turnê, "Back in the US" foi o nome da perna norte-americana de set/out de 2002 (documentada no álbum "Back in the U.S."), enquanto "Back in the World" foi a perna europeia de 2003 (documentada no álbum/DVD "Back in the World"). Como o pedido especificava o ano 2003, usei um show de 2003 (Paris-Bercy) sob o nome "Back in the World Tour" em vez de misturar as duas pernas — o repertório das duas é quase idêntico de qualquer forma.

6. **US Tour 2005** — Madison Square Garden, Nova York, 30/set/2005. 37 músicas.
   **Nota:** o pedido chamava essa era de "US summer tour, 2005"; a turnê de 2005 rodou de set a nov/2005 sob o nome oficial "US Tour" (sem uma perna de verão isolada e bem documentada à parte). Usei um show de setembro (início da turnê), a data mais próxima do "verão" com setlist completo e confiável.
   https://www.setlist.fm/setlist/paul-mccartney/2005/madison-square-garden-new-york-ny-5bddb700.html

7. **Summer Live '09 (2009)** — Citi Field, Nova York (Queens), 17/jul/2009 (show de abertura do Citi Field, também documentado no filme/álbum "Good Evening New York City"). 33 músicas.
   https://www.setlist.fm/setlist/paul-mccartney/2009/citi-field-queens-ny-43d657ab.html

8. **Up and Coming (2010-2012)** — reaproveitado do repositório: Porto Alegre, 07/nov/2010 (show_num 1 em `meus_13_shows_musicas.csv`). 38 músicas.
   https://www.setlist.fm/setlist/paul-mccartney/2010/estadio-beira-rio-porto-alegre-brazil-33d564c9.html

9. **Out There (2013-2015)** — **Desvio do pedido, documentado aqui:** o pedido original listava esta era para scraping novo, mas o próprio `meus_13_shows.csv` já tem um show da Tanise rotulado como turnê "Out There" (show_num 5, Montevidéu, 19/abr/2014), com setlist completo já salvo em `meus_13_shows_musicas.csv` e URL do setlist.fm já documentada em `referencias.md`. Para evitar duplicar trabalho e usar dados já verificados pela própria Tanise, reaproveitei esse show em vez de raspar um novo. 40 músicas.
   https://www.setlist.fm/setlist/paul-mccartney/2014/estadio-centenario-montevideo-uruguay-33c3eccd.html

10. **One on One (2016-2019)** — reaproveitado: Porto Alegre, 13/out/2017 (show_num 6). 39 músicas.
    https://www.setlist.fm/setlist/paul-mccartney/2017/estadio-beira-rio-porto-alegre-brazil-43e3ef13.html

11. **Freshen Up (2018-2019)** — reaproveitado: Buenos Aires, 23/mar/2019 (show_num 12). 39 músicas.
    https://www.setlist.fm/setlist/paul-mccartney/2019/campo-argentino-de-polo-buenos-aires-argentina-4b9253b6.html

12. **Got Back (2022-2025)** — união das 6 músicas dos shows Got Back da Tanise já no repositório (show_num 7, 8, 9, 10, 11, 13: Curitiba 13/dez/2023, Brasília 30/nov/2023, São Paulo 15/out/2024, São Paulo 16/out/2024, Florianópolis 19/out/2024, Cidade do México 14/nov/2023), para capturar um retrato mais completo do repertório rotativo dessa era mais recente (a turnê Got Back tem bastante variação de show pra show). 49 músicas únicas na união. `ano` foi registrado como 2023 (início da turnê); `data_show_fonte` mostra o intervalo real das 6 datas usadas.
    URLs (uma por show, na mesma ordem): setlist.fm/.../estadio-couto-pereira-curitiba-brazil-13ae05a1.html | .../arena-brb-mane-garrincha-brasilia-brazil-5bae9774.html | .../allianz-parque-sao-paulo-brazil-2b57f08a.html | .../allianz-parque-sao-paulo-brazil-357650b.html | .../estadio-da-ressacada-florianopolis-brazil-43573363.html | .../foro-sol-mexico-city-mexico-4ba1cf56.html

## Eras não encontradas / puladas

Nenhuma. Todas as 12 eras pedidas têm setlist completo e fonte citável.

## Confiança geral

Alta para as 12 eras. Todos os shows escolhidos são apresentações "clássicas"/bem documentadas (muitas delas viraram álbuns ou filmes ao vivo — Wings Over America, Back in the U.S., Good Evening New York City), com setlists completos e sem lacunas conhecidas no setlist.fm. As duas ressalvas registradas acima (era 5 e era 6) são sobre o nome exato da turnê/mês do show, não sobre a precisão do setlist em si. O desvio na era 9 (reaproveitar show_num 5 em vez de raspar de novo) foi uma decisão de eficiência, não uma limitação de fonte — os dados já eram de qualidade equivalente às raspagens novas.

## Números finais do dataset

- 12 eras de turnê cobertas.
- 143 músicas únicas em todo o dataset.
- 438 linhas música-turnê no formato longo (`paul_setlists_por_turne.csv`).
