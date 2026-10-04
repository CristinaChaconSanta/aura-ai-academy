#!/usr/bin/env bash
# init.sh — Start/close gate for AI agents working in this repo.
#
# Run it before starting work and before declaring any task done.
# Exit 0: the environment is ready. Non-zero: stop and fix it first.
# Per-project settings (TEST_CMD, AUDIT_CMD, ...) live in .claude/harness.env.

set -u
cd "$(dirname "$0")"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[0;33m'; NC='\033[0m'
ok()   { printf "${GREEN}[OK]${NC}    %s\n" "$1"; }
warn() { printf "${YELLOW}[WARN]${NC}  %s\n" "$1"; }
fail() { printf "${RED}[FAIL]${NC}  %s\n" "$1"; EXIT_CODE=1; }

EXIT_CODE=0
ENV_CHECK_CMD=""
TEST_CMD=""
AUDIT_CMD=""
HARNESS_FILES="CLAUDE.md AGENTS.md CHECKPOINTS.md progress/current.md odd/tasks"
# shellcheck disable=SC1091
[ -f .claude/harness.env ] && . .claude/harness.env

echo "── 1. Environment ─────────────────────────────────────"
if [ -z "$ENV_CHECK_CMD" ]; then
  warn "ENV_CHECK_CMD not set in .claude/harness.env"
elif out=$(bash -c "$ENV_CHECK_CMD" 2>&1); then
  ok "$ENV_CHECK_CMD -> $(echo "$out" | head -1)"
else
  fail "Environment check failed: $ENV_CHECK_CMD"
fi

echo ""
echo "── 2. Harness files ───────────────────────────────────"
for f in $HARNESS_FILES; do
  if [ -e "$f" ]; then ok "Exists $f"; else fail "Missing $f"; fi
done
if [ -f CLAUDE.md ]; then
  CLAUDE_LINES=$(wc -l < CLAUDE.md | tr -d ' ')
  if [ "$CLAUDE_LINES" -lt 200 ]; then
    ok "CLAUDE.md has $CLAUDE_LINES lines (< 200)"
  else
    fail "CLAUDE.md has $CLAUDE_LINES lines (must be < 200; move detail to docs/)"
  fi
fi

echo ""
echo "── 3. Tests ───────────────────────────────────────────"
if [ -z "$TEST_CMD" ]; then
  warn "Tests skipped (TEST_CMD not set in .claude/harness.env)"
else
  out=$(bash -c "$TEST_CMD" 2>&1); rc=$?
  echo "$out" | tail -3
  if [ $rc -eq 0 ]; then ok "All tests pass"; else fail "There are failing tests"; fi
fi

echo ""
echo "── 4. Security (optional tools) ───────────────────────"
if command -v gitleaks >/dev/null 2>&1; then
  if gitleaks git --no-banner --redact -l error . >/dev/null 2>&1; then
    ok "gitleaks: no secrets in git history"
  else
    fail "gitleaks found secrets (run: gitleaks git --redact .)"
  fi
else
  warn "gitleaks not installed (brew install gitleaks)"
fi
if [ -z "$AUDIT_CMD" ]; then
  warn "Dependency audit skipped (AUDIT_CMD not set)"
else
  audit_bin=${AUDIT_CMD%% *}
  if [ -x "$audit_bin" ] || command -v "$audit_bin" >/dev/null 2>&1; then
    if bash -c "$AUDIT_CMD" >/dev/null 2>&1; then
      ok "audit: no known vulnerable dependencies"
    else
      fail "audit found vulnerable dependencies (run: $AUDIT_CMD)"
    fi
  else
    warn "audit tool not installed ($audit_bin)"
  fi
fi

echo ""
echo "── 5. Summary ─────────────────────────────────────────"
if [ $EXIT_CODE -eq 0 ]; then
  ok "Environment ready. You can start working."
else
  printf "${RED}[FAIL]${NC}  Environment NOT ready. Fix the errors above before continuing.\n"
fi
exit $EXIT_CODE
