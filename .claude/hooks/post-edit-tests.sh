#!/usr/bin/env bash
# PostToolUse hook: run the test suite after every Edit/Write.
# On failure, exit 2 so Claude Code shows the failing tests to the agent right away.

cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}"

TEST_CMD=""
# shellcheck disable=SC1091
[ -f .claude/harness.env ] && . .claude/harness.env
[ -z "$TEST_CMD" ] && exit 0

out=$(bash -c "$TEST_CMD" 2>&1)
if [ $? -eq 0 ]; then
  exit 0
fi

echo "[harness] Tests fail after this edit:" >&2
echo "$out" | tail -15 >&2
exit 2
