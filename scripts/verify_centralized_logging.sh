#!/usr/bin/env bash
set -e

echo "Starting Centralized Logging Validation..."

STAGED_FILES=$(git diff --cached --name-only | grep -E "\.ex$|\.exs$" || true)

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

FAILED=0

for FILE in $STAGED_FILES; do
  if grep -qiE "LoggerFileBackend|.log\"" "$FILE"; then
    echo "❌ ERROR: File logging destination detected in $FILE!"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Centralized Logging rule violated."
  echo "Applications MUST NEVER store their own log files on disk. You must use 'stdout' only for centralized log streams."
  exit 1
fi

echo "✅ Centralized Logging validation passed."
exit 0
