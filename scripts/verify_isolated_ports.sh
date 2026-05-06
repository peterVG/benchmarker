#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Starting Port Isolation Validation..."

APPS_DIR="./apps"
ALL_PORTS_STRING=""
FAILED=0

# Loop through each module in the umbrella apps directory
for APP_PATH in "$APPS_DIR"/*; do
  if [ -d "$APP_PATH" ]; then
    APP_NAME=$(basename "$APP_PATH")
    
    DEV_EXS="$APP_PATH/config/dev.exs"
    RUNTIME_EXS="$APP_PATH/config/runtime.exs"
    
    # 1. Ensure config files exist
    if [ ! -f "$DEV_EXS" ] || [ ! -f "$RUNTIME_EXS" ]; then
      echo "⚠️  [SKIPPING] $APP_NAME: Missing dev.exs or runtime.exs"
      continue
    fi

    echo "🔍 Validating $APP_NAME..."

    # Extract target dev port using regex search
    # Matches: port: 4000
    DEV_PORT=$(grep -oE 'port:\s*[0-9]+' "$DEV_EXS" | grep -oE '[0-9]+' | head -n 1)

    # Extract target fallback runtime port using regex search
    # Matches: System.get_env("PORT", "4000")
    RUNTIME_PORT=$(grep -oE 'System\.get_env\("PORT",\s*"[0-9]+"\)' "$RUNTIME_EXS" | grep -oE '[0-9]+' | head -n 1)

    if [ -z "$DEV_PORT" ]; then
      echo "❌ ERROR ($APP_NAME): Could not find 'port: XXXX' in dev.exs"
      FAILED=1
    fi

    if [ -z "$RUNTIME_PORT" ]; then
      echo "❌ ERROR ($APP_NAME): Could not find fallback 'PORT', 'XXXX' in runtime.exs"
      FAILED=1
    fi

    # 2. Assert Match
    if [ "$DEV_PORT" != "$RUNTIME_PORT" ]; then
      echo "❌ ERROR ($APP_NAME): Port mismatch! dev.exs ($DEV_PORT) != runtime.exs ($RUNTIME_PORT)"
      FAILED=1
    fi

    # 3. Assert Uniqueness
    if [[ "$ALL_PORTS_STRING" == *"$DEV_PORT"* ]]; then
      echo "❌ ERROR ($APP_NAME): Port $DEV_PORT is already in use by another app!"
      FAILED=1
    else
      ALL_PORTS_STRING="$ALL_PORTS_STRING $DEV_PORT:$APP_NAME"
      echo "✅ $APP_NAME uniquely bound to $DEV_PORT"
    fi
  fi
done

if [ "$FAILED" -ne 0 ]; then
  echo ""
  echo "🚨 VALIDATION FAILED: Port isolation constraints violated. See errors above."
  exit 1
else
  echo ""
  echo "🚀 VALIDATION PASSED: All modules maintain strict port isolation."
  exit 0
fi
