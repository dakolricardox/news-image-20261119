# The NIMBLE GLOBE — 19 November 2026 front page

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/dakolricardox/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/dakolricardox/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A deterministic 1024x1024 PNG newspaper front page, rendered with Python + Pillow
only, summarizing the world news of Thursday 19 November 2026 on one cream
editorial page. Built for the make.fun "Sum up 19 November's world news in one
image" competition (https://make.fun/bounty/news-image-20261119).

## What the page shows

- **Top story:** First-ever trilateral summit — Trump, Xi and Putin at one table
  in Shenzhen (APEC 2026, day 2); 11 US-China deals signed.
- **The Watch rail:** NSA comms network outage fall-out; market taps (S&P 500 +1.0%
  at 6,770.06, NVDA +5.0%, gold 13-month low, Brent +2.0% at $64.22); Friday preview.
- **Four feature cards:** ground raid on Gaza City; US records / gold slide; Iran
  hits Kuwait (day 6); world briefs (Starmer resigns, Camp David 50th, US back in
  the WHO).
- **Also today band:** APEC closing, WHO re-entry, UK leadership revolt, UN AI
  race, Egypt Camp David anniversary.

## Run

```
python3 main.py
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` if set, otherwise
`<script dir>/output/entry.png`. Requires Pillow; stdlib otherwise.

## Files

- `main.py` — the entrypoint (single file, Pillow + stdlib)
- `vendor/pillow.whl` — vendored Pillow 12.3.0 wheel (sha256
  `0847a763...8b6d3`, verified against PyPI). The competition sandbox image
  ships Python 3.13 without Pillow or fonts, so `main.py` unpacks this wheel
  into a scratch dir at startup only when Pillow is missing, imports the full
  API (PNG encoder included), then removes the scratch tree.
- `vendor/fonts/` — the four DejaVu TTFs the page uses. They are tried
  before the system font paths, so rendering is independent of the host font
  stack (and of host vs. sandbox freetype version skew — the committed PNG
  was rendered with exactly these).
- `output/entry.png` — rendered 1024x1024 front page (rendered inside the
  competition sandbox image, so the committed file matches the graded run
  byte-for-byte)
- `.makefun/owner.json` — owner wallet
- `LICENSE` — MIT

## Determinism

No network access, no clock reads, no randomness: two runs are byte-identical
(verified with `cmp` inside the competition sandbox image). All fonts are
DejaVu (with a deterministic fallback chain); all geometry is fixed integer
math. The committed PNG was rendered in the exact grader environment
(Python 3.13.17 + vendored Pillow 12.3.0), so host font-stack differences
cannot change the graded bytes.
