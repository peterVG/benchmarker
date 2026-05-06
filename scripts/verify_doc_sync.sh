#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Document Sync Validation..."

# Get all staged files
STAGED_FILES=$(git diff --cached --name-only)

if [ -z "$STAGED_FILES" ]; then
  # Nothing staged
  exit 0
fi

# Check if any source code was modified
CODE_MODIFIED=0
for FILE in $STAGED_FILES; do
  if [[ "$FILE" == *.ex ]] || [[ "$FILE" == *.exs ]]; then
    CODE_MODIFIED=1
    break
  fi
done

# Check if any documentation was modified
DOCS_MODIFIED=0
for FILE in $STAGED_FILES; do
  if [[ "$FILE" == *.md ]]; then
    DOCS_MODIFIED=1
    break
  fi
done

if [ "$CODE_MODIFIED" -eq 1 ] && [ "$DOCS_MODIFIED" -eq 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Code was modified but no documentation (.md files) were updated!"
  echo "Per the Pull Request Documentation Updates rule, permanent documentation (PRD, SRS, ADRs) must remain synchronized."
  echo "If this code change truly requires zero documentation updates, you can bypass this hook with 'git commit --no-verify'."
  echo ""
  exit 1
fi

echo "✅ Document Sync Validation passed."
exit 0
