#!/usr/bin/env bash
set -e

echo "Starting Portable Documentation Validation..."

STAGED_FILES=$(git diff --cached --name-only | grep "\.md$" || true)

if [ -z "$STAGED_FILES" ]; then
  exit 0
fi

FAILED=0

for FILE in $STAGED_FILES; do
  if grep -qiE "file:///" "$FILE"; then
    echo "❌ ERROR: Absolute path 'file:///' detected in $FILE!"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Portable Documentation rule violated."
  echo "You MUST use relative paths (e.g. [PRD](../prd.md)) instead of absolute file:/// strings."
  exit 1
fi

echo "✅ Portable Documentation validation passed."
exit 0
