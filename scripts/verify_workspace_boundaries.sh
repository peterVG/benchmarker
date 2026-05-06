#!/usr/bin/env bash
set -e

echo "Starting Workspace Boundary Validation..."

FORBIDDEN_FILES=(
  "mix.exs"
  "package.json"
  "requirements.txt"
  "Gemfile"
)

FAILED=0

for FILE in "${FORBIDDEN_FILES[@]}"; do
  if [ -f "$FILE" ]; then
    echo "❌ ERROR: Forbidden language tooling '$FILE' found at global repository root!"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Workspace Boundaries rule violated."
  echo "All language and dependency manifests MUST be placed inside individual modules in the 'apps/' directory, not at the root!"
  exit 1
fi

echo "✅ Workspace Boundary validation passed."
exit 0
