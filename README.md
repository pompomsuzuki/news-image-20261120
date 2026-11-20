[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/pompomsuzuki/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/pompomsuzuki/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

# The World in One Day — 20 November 2026

Entry for make.fun's bounty [“Sum up 20 November's world news in one image”](https://make.fun/bounty/news-image-20261120).

`main.py` is a dependency-free Python program (standard library only, no
network) that draws a newspaper front page of Friday 20 November 2026 and
writes it to `/output/entry.png` (1024×1024 PNG). It renders its own PNG
encoder, raster canvas and 5×7 pixel font, so the two grading runs produce
byte-identical output.

The front page carries five stories of the day:

- **Lead — Brussels:** the UK and the EU seal a “reset” deal — food trade
  eased, carbon markets linked from 2028, and a youth-mobility scheme for
  100,000 young people a year each way.
- **Kyiv:** overnight Russian missile strikes hit bridges in Kyiv, killing 8
  and injuring 28 across Ukraine; two missiles and a drone crossed into
  Polish airspace.
- **Markets:** AI fears hit world markets — Tokyo's Nikkei fell 4.8% and
  Anthropic slid on its second day of trading after its record IPO debut.
- **Climate:** the COP31 draft deal in Antalya drops fossil fuels, keeping a
  35% electrification goal.
- **Kenya:** the last Ebola patient is discharged and the 42-day countdown
  to an Ebola-free declaration begins.

Footer ticker: a Van Gogh sells for a record $190.4M, and the Saudi-led
coalition strikes Yemen's port of Hodeidah.

## Run it

```sh
mkdir -p out
MAKEFUN_OUTPUT_DIR=out python3 main.py
# writes out/entry.png
```

## License

MIT — see `LICENSE`.
