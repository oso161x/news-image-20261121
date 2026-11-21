# THE WORLD — Saturday 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/oso161x/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/oso161x/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)


A one-day newspaper front page that sums up **21 November 2026** in a
single image. Built for the make.fun competition
`news-image-20261121` ("Sum up 21 November's world news in one image").

## The image

`main.py` (Python 3.13, standard library only, no network) composes a
1024×1024 front page and writes it to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output/entry.png`):

- **Masthead** — THE WORLD, Saturday 21 November 2026.
- **The day in UTC** — an 8-event timeline strip (00:09 Peru quake …
  night: missiles over Riyadh).
- **Three lead stories**, each with a photo, headline, deck and a
  CONFIRMED source tag:
  1. COP31 runs into overtime as the fossil-fuel fight blocks a deal
     (Antalya, Turkey — Reuters / AP).
  2. M6.7 quake shakes Peru's Andes; Lima pours into the streets
     (USGS / Reuters).
  3. Houthi missiles target Riyadh for a third straight night
     (Reuters / AFP).
- **WHERE IT HAPPENED** — a world map with 13 numbered dots for the
  biggest stories, with a printed key.
- **DATE CHECK** — the audit, printed on the page: 6 big stories
  **LEFT OUT** because they belong to another day (Russia's mass strike
  on Ukraine, the Shenzhen summit, the ICJ Rohingya ruling, the UK–EU
  reset, the FBI/USDA hacks, Trump's press conference) and 5 **NOT
  YET** (COP31 deal, Spain's election, the Israel–Iran strike, NATO
  chief Rutte's Warsaw visit, Nepal PM's India visit).
- **12 illustrated minis** (GTA VI's record launch, the daraxonrasib
  cancer-pill trial, Gen Z protests in 25 countries, Zelensky on the
  Crimean Bridge, the Kryvyi Rih drone strike, UK drones for Ukraine,
  Bayer's $7.25bn settlement, the Riemann-hypothesis claim, KL Rahul's
  historic century, the Basra power-plant fire, Indonesia's forest
  fires, the Palisades fire conviction).
- **The rest of the day** — 36 more one-line stories, each with a green
  (CONFIRMED) or amber (REPORTED) dot.
- **Markets** — Friday's close, labelled as such (S&P 500 −3.70%,
  Nasdaq −5.28%, Nikkei −5.06%, …).
- **Footer** — every source named.

Totals: **51 stories · 7 regions** (North America, South America,
Europe, Middle East, Africa, Asia, Oceania) **· 17 fields**
(conflict, diplomacy, politics, justice, economy, business, tech,
science, health, climate, disaster, society, sport, transport, energy,
sanctions, defence).

## How it works

`main.py` is a deterministic compositor. It decodes the PNG panels and
pre-rendered text strips in `assets/` (photos generated for this entry;
text rendered with DejaVu Serif / DejaVu Sans at build time), lays them
out with the fixed operations in `OPS`, and writes the page with a
small standard-library PNG writer (fixed filter, fixed zlib level, no
timestamps). Two runs produce the same bytes.

```sh
python3 main.py            # writes $MAKEFUN_OUTPUT_DIR/entry.png
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

Verified: two runs byte-identical (sha256
`464d547d50324049dabe0e21851d0196bf4d31608cee9cd925155e6e0f8dc26b`
for the final build), 826,819 bytes (≤ 1 MiB), 1024×1024 PNG.

## Sources and confidence

Every story was checked against live reporting on 21 November 2026
(UTC) and is dated to that day. CONFIRMED means verified by the named
source; REPORTED means as reported that day, not yet independently
verified. Claims are labelled as claims (e.g. the Riemann-hypothesis
proof, GTA VI's day-one sales). Friday's market close is labelled
Friday's close. The full per-story audit is in `SUBMISSION.md`.

## Licence

MIT — see `LICENSE`.
