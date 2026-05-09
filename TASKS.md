# TASKS.md

> Live actionable backlog. The plan in `.cursor/plans/` is strategy; this file is the next physical step.

Conventions:
- `[x]` complete  ·  `[~]` in progress / needs human  ·  `[ ]` pending  ·  `[!]` blocked on external access

---

## Phase 1 — Research

- [x] **Research notes drafted** → [research/notes.md](research/notes.md)
- [~] **Read primary papers** — checklist with arXiv IDs → [research/PAPER_CHECKLIST.md](research/PAPER_CHECKLIST.md)
  - Acceptance: Tina can sketch Kaplan loss, attention QKV→n², and one post-transformer family on a whiteboard without notes.

## Phase 2 — Scripts

- [x] **Teaser script** → [scripts/teaser.md](scripts/teaser.md)
- [x] **Deep-dive script** → [scripts/deepdive.md](scripts/deepdive.md)
- [~] **Scratch VO recording** — see [audio/scratch/README.md](audio/scratch/README.md)
  - Acceptance: scratch tracks in `audio/scratch/` (gitignored); scripts edited for pacing.

## Phase 3 — Production tooling

- [x] **Repo scaffold**, **theme**, **mobjects**, **Makefile**, **environment.yml**
- [x] **Lean micromamba env** — `make setup` / `make check`
- [x] **Teaser + deep-dive smoke renders** at `QUALITY=-ql` (all Makefile-listed scenes)
- [x] **LaTeX-free deep-dive** — formulas use `text_equation()` / `Text` in scenes 3, 5, 6, 9 so CI machines without TeX can run `make deepdive`.

## Phase 4 — Animation

### Teaser (6 scenes)

Polish pass applied in code (easing, KV bar count-up, crack shards, payoff icons, CTA sheen). Production renders: `QUALITY=-qh make teaser`.

- [x] **scene_01–06** — smoke OK at `-ql`; polish in source
- [~] **Final `-qh` / `-qk` masters** — run when locking picture

### Deep-dive (11 Manim scenes + 2 `SKIP_RENDER` placeholders)

Scene 2 (on-cam) and 13 (screen demo) are placeholders — real footage on shoot day.

- [x] **All numbered Manim scenes** — `QUALITY=-ql make deepdive` passes (2026-05-09)
- [~] **Production `-qh` pass** — optional before final upload

## Phase 5 — Shoot day

Runbook: [scripts/runbook_shoot_day.md](scripts/runbook_shoot_day.md)

- [ ] SubQ beta / API key
- [ ] Camera + audio setup
- [ ] On-camera takes → `video/`
- [ ] VO → `audio/final/`
- [ ] SubQ Code capture → `demo/`

## Phase 6 — Edit + ship

Runbook: [scripts/runbook_edit_and_ship.md](scripts/runbook_edit_and_ship.md)

- [ ] DaVinci assembly, color, mix, captions
- [ ] Delivery masters (16:9, 1:1, 9:16 per [DESIGN.md](DESIGN.md))

## Phase 7 — Companion deliverables

- [x] Starter repo, blog draft, X thread draft, cover letter
- [ ] **Live benchmarks** — fill [companion/subq-quickstart/BENCHMARKS.md](companion/subq-quickstart/BENCHMARKS.md) after API access  
  - Smoke without SDK: `python benchmarks/needle_in_haystack.py --dry-run --tokens 500000`
- [ ] **Publish `subq-quickstart`** — [companion/subq-quickstart/PUBLISH.md](companion/subq-quickstart/PUBLISH.md)
- [x] **X-thread stills** — `make stills` → `bash scripts/export_x_thread_stills.sh` → `assets/x_thread_stills/*.png` (default render frame; square-crop to 1080×1080 in Resolve or ffmpeg if needed for X)
- [ ] **Schedule X thread** (~9am PT)

## Phase 8 — Submit

- [ ] Confirm handles / links in [companion/cover_letter.md](companion/cover_letter.md)
- [ ] Submit application

---

## Reconcile duplicate scene files — DONE 2026-05-09

See git history: alternates for scenes 04/05/07 merged into canonical files and deleted.

## Done definition (whole sprint)

- [ ] Teaser on YouTube + embedded in X tweet 1
- [ ] Deep-dive on YouTube
- [ ] Blog live
- [ ] X thread posted
- [ ] `subq-quickstart` public with ≥1 real benchmark row
- [ ] Application submitted
