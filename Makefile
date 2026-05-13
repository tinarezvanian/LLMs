# SubQ video pipeline.
# All commands assume micromamba env `subq` exists. See README.md for setup.

SHELL := /bin/bash
ROOT := $(shell pwd)
MM := $(ROOT)/bin/micromamba
ENV := $(ROOT)/.micromamba/envs/subq
ACTIVATE := export MAMBA_ROOT_PREFIX="$(ROOT)/.micromamba" && eval "$$($(MM) shell hook --shell bash)" && micromamba activate subq && export PATH="$(ROOT)/bin:$$PATH" && export PYTHONPATH="$(ROOT):$$PYTHONPATH"

QUALITY ?= -qm
OUT_DIR := $(ROOT)/edit/renders

TEASER_SCENES := \
  vid/scenes/teaser/scene_01_open.py:Scene01Open \
  vid/scenes/teaser/scene_02_curve.py:Scene02Curve \
  vid/scenes/teaser/scene_03_wall.py:Scene03Wall \
  vid/scenes/teaser/scene_03b_tokens.py:Scene03BTokens \
  vid/scenes/teaser/scene_03c_attention_tile.py:Scene03CAttentionTile \
  vid/scenes/teaser/scene_03d_scaling_loglog.py:Scene03DScalingLogLog \
  vid/scenes/teaser/scene_03e_chinchilla_bite.py:Scene03EChinchillaBite \
  vid/scenes/teaser/scene_03f_kv_band_aids.py:Scene03FKVBandAids \
  vid/scenes/teaser/scene_03g_landscape_quadrant.py:Scene03GLandscapeQuadrant \
  vid/scenes/teaser/scene_03h_wall_twice.py:Scene03HWallTwice \
  vid/scenes/teaser/scene_04_break.py:Scene04Break \
  vid/scenes/teaser/scene_05_payoff.py:Scene05Payoff \
  vid/scenes/teaser/scene_06_cta.py:Scene06CTA

DEEPDIVE_SCENES := \
  vid/scenes/deepdive/scene_01_cold_open.py:Scene01ColdOpenTitle \
  vid/scenes/deepdive/scene_03_scaling_laws.py:Scene03ScalingLaws \
  vid/scenes/deepdive/scene_04_pivot.py:Scene04Pivot \
  vid/scenes/deepdive/scene_05_attention.py:Scene05Attention \
  vid/scenes/deepdive/scene_06_kv_wall.py:Scene06KVWall \
  vid/scenes/deepdive/scene_07_flashattention.py:Scene07FlashAttention \
  vid/scenes/deepdive/scene_08_landscape.py:Scene08Landscape \
  vid/scenes/deepdive/scene_09_mamba.py:Scene09Mamba \
  vid/scenes/deepdive/scene_10_subq_position.py:Scene10SubQPosition \
  vid/scenes/deepdive/scene_11_benchmarks.py:Scene11Benchmarks \
  vid/scenes/deepdive/scene_12_demo_intro.py:Scene12DemoIntro \
  vid/scenes/deepdive/scene_14_close.py:Scene14EndCard

STILLS_DIR := $(OUT_DIR)/stills

RES ?= 1080p60

.PHONY: all teaser deepdive stills concat socials setup setup-latex check clean help

help:
	@echo "Targets:"
	@echo "  setup       - install micromamba env (run once)"
	@echo "  setup-latex - print platform-specific commands for LaTeX 'preview' package"
	@echo "  check       - smoke-test that manim + ffmpeg work"
	@echo "  teaser      - render all teaser scenes (override QUALITY=-qh for HD)"
	@echo "  deepdive    - render all deep-dive scenes"
	@echo "  stills      - export final PNG frame of every scene (override QUALITY=-qh for HD)"
	@echo "  concat      - glue scene MP4s into single previews (RES=1080p60 by default)"
	@echo "  socials     - 1:1 + 9:16 cuts of the teaser concat (for X / Shorts / Reels / TikTok)"
	@echo "  all         - render teaser + deepdive"
	@echo "  clean       - remove edit/renders and __pycache__"

# Lean install: conda-forge `manim` + `ffmpeg` only. Installing `manim-voiceover`
# from conda in the same solve pulls a huge TTS dep tree and can hang for 20+ min.
# After `make setup`, optional: `micromamba activate subq && pip install manim-voiceover`
setup:
	@if [ ! -x "$(MM)" ]; then echo "micromamba missing at $(MM); see README"; exit 1; fi
	@if [ ! -d "$(ENV)" ]; then \
	  export MAMBA_ROOT_PREFIX="$(ROOT)/.micromamba" && \
	  $(MM) create -y -n subq -c conda-forge python=3.12 manim ffmpeg; \
	fi
	@$(ACTIVATE) && python -c "import manim; print('manim', manim.__version__)"

check:
	@$(ACTIVATE) && which python && python -c "import manim; print('manim', manim.__version__)"
	@$(ROOT)/bin/ffmpeg -version | head -1

teaser:
	@mkdir -p $(OUT_DIR)/teaser
	@set -e; for entry in $(TEASER_SCENES); do \
	  file=$${entry%%:*}; klass=$${entry##*:}; \
	  echo "==> rendering $$file::$$klass"; \
	  $(ACTIVATE) && manim $(QUALITY) --media_dir $(OUT_DIR)/teaser $$file $$klass; \
	done

deepdive:
	@mkdir -p $(OUT_DIR)/deepdive
	@set -e; for entry in $(DEEPDIVE_SCENES); do \
	  file=$${entry%%:*}; klass=$${entry##*:}; \
	  echo "==> rendering $$file::$$klass"; \
	  $(ACTIVATE) && manim $(QUALITY) --media_dir $(OUT_DIR)/deepdive $$file $$klass; \
	done

stills:
	@mkdir -p $(STILLS_DIR)
	@set -e; for entry in $(TEASER_SCENES) $(DEEPDIVE_SCENES); do \
	  file=$${entry%%:*}; klass=$${entry##*:}; \
	  echo "==> still $$file::$$klass ($(QUALITY))"; \
	  $(ACTIVATE) && manim $(QUALITY) -s --format png --media_dir $(STILLS_DIR) $$file $$klass; \
	done
	@echo "==> stills written under $(STILLS_DIR)/images/"

concat:
	@bash $(ROOT)/scripts/concat_scenes.sh teaser   $(RES)
	@bash $(ROOT)/scripts/concat_scenes.sh deepdive $(RES)

socials:
	@bash $(ROOT)/scripts/social_cuts.sh

setup-latex:
	@echo "Manim's MathTex needs the LaTeX 'preview' package."
	@echo "Install per platform, then re-run 'make deepdive':"
	@echo ""
	@echo "  macOS / Linux (TeX Live):  sudo tlmgr install preview"
	@echo "  Windows (MiKTeX):          MiKTeX Console -> Packages -> install 'preview'"
	@echo ""
	@echo "Alternative: in any deep-dive scene, swap equation(...) for text_equation(...)"
	@echo "from vid.theme — renders plain Text, no LaTeX needed."

all: teaser deepdive

clean:
	rm -rf $(OUT_DIR)
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
