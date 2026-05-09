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

.PHONY: all teaser deepdive setup check clean help

help:
	@echo "Targets:"
	@echo "  setup     - install micromamba env (run once)"
	@echo "  check     - smoke-test that manim + ffmpeg work"
	@echo "  teaser    - render all teaser scenes (override QUALITY=-qh for HD)"
	@echo "  deepdive  - render all deep-dive scenes"
	@echo "  all       - render everything"
	@echo "  clean     - remove rendered media (keeps source)"

setup:
	@if [ ! -x "$(MM)" ]; then echo "micromamba missing at $(MM); see README"; exit 1; fi
	@$(ACTIVATE) && python -c "import manim; print('manim', manim.__version__)" \
	  || ($(MM) create -y -n subq -c conda-forge python=3.12 manim manim-voiceover ffmpeg)

check:
	@$(ACTIVATE) && which python && python -c "import manim; print('manim', manim.__version__)"
	@$(ROOT)/bin/ffmpeg -version | head -1

teaser:
	@mkdir -p $(OUT_DIR)/teaser
	@for entry in $(TEASER_SCENES); do \
	  file=$${entry%%:*}; klass=$${entry##*:}; \
	  echo "==> rendering $$file::$$klass"; \
	  $(ACTIVATE) && manim $(QUALITY) --media_dir $(OUT_DIR)/teaser $$file $$klass; \
	done

deepdive:
	@mkdir -p $(OUT_DIR)/deepdive
	@for entry in $(DEEPDIVE_SCENES); do \
	  file=$${entry%%:*}; klass=$${entry##*:}; \
	  echo "==> rendering $$file::$$klass"; \
	  $(ACTIVATE) && manim $(QUALITY) --media_dir $(OUT_DIR)/deepdive $$file $$klass; \
	done

all: teaser deepdive

clean:
	rm -rf $(OUT_DIR)
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
