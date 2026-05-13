#!/usr/bin/env bash
# Scan main.log for LaTeX "Overfull \hbox" warnings (width problems that often
# produce visible overlap or run-in with margin floats in tufte-book).
#
# Usage:
#   ./check_overfull.sh              # print all overfull lines, exit 0
#   FAIL_MAX_PT=30 ./check_overfull.sh   # exit 1 if any overflow exceeds 30pt
#
# This does not catch every visual glitch (e.g. some PDF-only overlaps without
# an overfull box), but it catches the Chapter 9 table class of bug reliably.

set -euo pipefail
cd "$(dirname "$0")"
LOG="${1:-main.log}"
if [[ ! -f "$LOG" ]]; then
  echo "check_overfull: missing $LOG (run xelatex first)" >&2
  exit 2
fi

tmp=$(mktemp)
grep -F 'Overfull \hbox' "$LOG" >"$tmp" || true
count=$(wc -l <"$tmp" | tr -d ' ')
if [[ "$count" -eq 0 ]]; then
  rm -f "$tmp"
  echo "No Overfull \\hbox warnings in $LOG"
  exit 0
fi

echo "Overfull \\hbox warnings ($count):"
cat "$tmp"

max_pt="0"
while IFS= read -r line; do
  pt=$(printf '%s' "$line" | sed -n 's/.*Overfull \\hbox (\([0-9.]*\)pt too wide).*/\1/p')
  [[ -z "$pt" ]] && continue
  awk -v a="$max_pt" -v b="$pt" 'BEGIN{exit !(b>a)}' && max_pt="$pt"
done <"$tmp"
rm -f "$tmp"

echo "==> largest overflow: ${max_pt}pt"

fail_at="${FAIL_MAX_PT:-}"
if [[ -n "$fail_at" ]]; then
  awk -v m="$max_pt" -v lim="$fail_at" 'BEGIN{exit !(m>lim)}' && {
    echo "check_overfull: FAIL (max ${max_pt}pt > ${fail_at}pt)" >&2
    exit 1
  }
  echo "check_overfull: OK (max ${max_pt}pt <= ${fail_at}pt)"
fi
