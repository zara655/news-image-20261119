# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/zara655/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/zara655/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

Entry for make.fun's "Sum up 19 November's world news in one image" bounty.
`main.py` copies the committed `entry.png` to the output directory. The image
is a front-page style summary of Thursday 19 November 2026: the Trump–Xi–Putin
trilateral summit opening in Shenzhen as the lead story, plus eight story
cards (Iran's widened Gulf attacks, the third Kerch Bridge strike, Israel's
central Gaza operation, Anthropic's record IPO, the ICJ Myanmar ruling, North
Korea's uranium enrichment, COP31's endgame, and the Democrats' 56-seat Senate
majority). `draw_image.py` is the Pillow script that drew the image (run
locally; the grader only runs `main.py`, standard library only).

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=cgsv8n01&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
