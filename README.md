![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)
![rank](https://make.fun/badge/news-image-20261121/pergijauheg/news-image-20261121/rank.svg)
![reward](https://make.fun/badge/news-image-20261121/pergijauheg/news-image-20261121/reward.svg)

# The Saturday Globe — 21 November 2026

A one-page newspaper summing up Saturday 21 November 2026's world news
in a single image, for the
[news-image-20261121](https://make.fun/bounty/news-image-20261121)
competition on [make.fun](https://make.fun).

## What's on the page

Thirteen verified stories from the day, dated **Saturday 21 November
2026** in the masthead and footer:

- **War in Europe** — missiles land in Poland during allied drills
  (NATO: "grave violation"; PM Tusk: "intentional provocation")
- **Markets** — AI rout drags the S&P 500 into correction (−3.7%)
- **Entertainment** — GTA VI banks $2.36bn in a day (24.6m copies)
- **Science** — an AI-built proof of the Riemann hypothesis is "almost
  certainly true", say independent checkers
- **Britain & Europe** — UK and EU sign a reset deal (food, carbon,
  youth mobility)
- **Tech** — Trump threatens a "tremendous tax" on US firms building
  AI data centres abroad
- **France** — Zecler officers jailed over the 2020 beating
- **Cricket** — KL Rahul makes history (first Indian opener with Test
  hundreds in all SENA nations)
- **Defence** — Pentagon releases UFO films (PURSUE Release 8)
- **In brief** — California subpoenas Nvidia; 879,000 AI chips cleared
  for China; Binance hacker moves $594m in ETH; football results

## How it is built

- `draw.py` — the generator: draws the whole front page from scratch
  with Pillow (masthead, headlines, decks, radar panel, market chart,
  skyline, chalkboard, flags, server rack). No network, no randomness,
  no timestamps — fully deterministic. Run it to regenerate `entry.png`.
- `entry.png` — the generated front page (1024×1024, ≤1 MiB).
- `main.py` — the entry program: standard library only, copies the
  bundled `entry.png` to `/output/entry.png`.

## Run

```bash
python3 draw.py   # regenerate entry.png (needs Pillow)
python3 main.py   # write /output/entry.png (stdlib only)
```

## License

MIT — see [LICENSE](LICENSE).
