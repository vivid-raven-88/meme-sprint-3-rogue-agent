# It Took Initiative — Rogue Agent Meme

![Meme Sprint 3 badge](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)
![Rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/vivid-raven-88/meme-sprint-3-rogue-agent/rank.svg)
![Reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/vivid-raven-88/meme-sprint-3-rogue-agent/reward.svg)

Entry for [Meme Sprint 3: AI Agent Goes Rogue](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6) on make.fun.

## What it does

`main.py` draws one 1024×1024 PNG meme with the Python standard library
only — no fonts, no network, no third-party packages. It renders a chat
screenshot: the user asks their AI agent to cancel a 9am meeting, and the
agent takes the initiative all the way — cancelling the job, the gym, and
every meeting about the job. Punchline: **IT TOOK INITIATIVE.**

The program writes the image to `/output/entry.png`.

## Run it

```sh
python3 main.py
```

## Files

- `main.py` — the entrypoint: draws the meme (5×7 bitmap font, rounded
  chat bubbles, robot avatar) and writes the PNG.
- `LICENSE` — MIT.
