#!/usr/bin/env bash
set -e

echo "Starting Format Validation..."

APPS_DIR="./apps"
FAILED=0

for APP_PATH in "$APPS_DIR"/*; do
  if [ -d "$APP_PATH" ] && [ -f "$APP_PATH/mix.exs" ]; then
    APP_NAME=$(basename "$APP_PATH")
    echo "🔍 Validating formatting for $APP_NAME..."
    
    cd "$APP_PATH"
    
    # Run the Elixir formatter in check mode
    if ! mix format --check-formatted >/dev/null 2>&1; then
      echo "❌ ERROR ($APP_NAME): Code format violation detected!"
      FAILED=1
    else
      echo "✅ $APP_NAME is properly formatted."
    fi
    
    cd - >/dev/null
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Test-Driven Development formatting rule violated."
  echo "You MUST run 'mix format' inside each modified app directory before committing."
  exit 1
fi

echo "✅ Format validation passed."
exit 0
