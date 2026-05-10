#!/usr/bin/env bash
# List every open \fillme{...} stub in docs/scaling_attention as a checklist
# that any LLM (or human) can pick from. Each line shows ID, title, file, and
# line number so you can `\$EDITOR <file>:<line>` straight to the stub.
#
# Usage:
#   bash scripts/list_fill_stubs.sh                  # plain checklist
#   bash scripts/list_fill_stubs.sh --markdown       # markdown task list
#   bash scripts/list_fill_stubs.sh --count          # just the totals
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SECTIONS="$ROOT/docs/scaling_attention/sections"

if [[ ! -d "$SECTIONS" ]]; then
  echo "no sections directory at $SECTIONS" >&2
  exit 1
fi

MODE="plain"
case "${1:-}" in
  --markdown) MODE="markdown" ;;
  --count)    MODE="count" ;;
  --help|-h)
    grep '^#' "$0" | head -10
    exit 0
    ;;
esac

# Find every \fillme{ID}{TITLE}{...} occurrence and pull out ID + TITLE.
# We use ripgrep when available (much faster on a large repo) and fall back
# to grep otherwise.
if command -v rg >/dev/null 2>&1; then
  HITS=$(rg -n --no-heading '^\\fillme\{' "$SECTIONS" || true)
else
  HITS=$(grep -rnH '^\\fillme{' "$SECTIONS" || true)
fi

if [[ -z "$HITS" ]]; then
  echo "0 open stubs."
  exit 0
fi

# Each HIT line looks like: <file>:<line>:\fillme{ID}{TITLE}{...
parse() {
  local line="$1"
  local file="${line%%:*}"
  local rest="${line#*:}"
  local lineno="${rest%%:*}"
  local body="${rest#*:}"
  # Strip leading \fillme{
  body="${body#\\fillme\{}"
  # ID is up to the first }
  local id="${body%%\}*}"
  body="${body#*\}}"
  # next char should be { for TITLE; strip that one and read until matching }
  body="${body#\{}"
  local title="${body%%\}*}"
  printf "%s\t%s\t%s\t%s\n" "$id" "$title" "$file" "$lineno"
}

ROWS=""
while IFS= read -r line; do
  ROWS+="$(parse "$line")"$'\n'
done <<<"$HITS"
ROWS="${ROWS%$'\n'}"
SORTED="$(printf "%s\n" "$ROWS" | sort)"
TOTAL="$(printf "%s\n" "$SORTED" | wc -l | tr -d ' ')"

case "$MODE" in
  count)
    echo "$TOTAL open \\fillme{} stubs across $(echo "$SORTED" | awk -F'\t' '{print $3}' | sort -u | wc -l | tr -d ' ') files."
    ;;
  markdown)
    echo "# Open \`\\fillme\` stubs ($TOTAL)"
    echo
    while IFS=$'\t' read -r id title file lineno; do
      rel="${file#"$ROOT/"}"
      printf -- "- [ ] **%s** %s — \`%s:%s\`\n" "$id" "$title" "$rel" "$lineno"
    done <<<"$SORTED"
    ;;
  plain|*)
    echo "Open \\fillme stubs: $TOTAL"
    echo "---"
    printf "%-14s  %-60s  %s\n" "ID" "TITLE" "FILE:LINE"
    printf "%-14s  %-60s  %s\n" "--------------" "------------------------------------------------------------" "---------"
    while IFS=$'\t' read -r id title file lineno; do
      rel="${file#"$ROOT/"}"
      printf "%-14s  %-60s  %s:%s\n" "$id" "${title:0:60}" "$rel" "$lineno"
    done <<<"$SORTED"
    ;;
esac
