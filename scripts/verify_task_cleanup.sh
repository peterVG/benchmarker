#!/usr/bin/env bash

# Task Cleanup Validation
#
# This script ensures that whenever a Walkthrough document exists for a task,
# the corresponding Plan and ToDos documents are removed to prevent clutter.

FAILED=0

# Find all Walkthrough documents across all apps
WALKTHROUGHS=$(find apps -name "*-Walkthrough.md" 2>/dev/null)

for WT in $WALKTHROUGHS; do
  # Extract the base path and the task identifier (e.g., "apps/app_abc/docs/tasks/Task-1.1")
  BASE_NAME="${WT%-Walkthrough.md}"
  
  PLAN_FILE="${BASE_NAME}-Plan.md"
  TODOS_FILE="${BASE_NAME}-ToDos.md"

  if [ -f "$PLAN_FILE" ]; then
    echo "❌ ERROR: Task cleanup failure. Found Walkthrough but Plan document still exists: $PLAN_FILE"
    FAILED=1
  fi

  if [ -f "$TODOS_FILE" ]; then
    echo "❌ ERROR: Task cleanup failure. Found Walkthrough but ToDos document still exists: $TODOS_FILE"
    FAILED=1
  fi
done

if [ $FAILED -ne 0 ]; then
  echo "You must remove the '-Plan.md' and '-ToDos.md' files once the '-Walkthrough.md' is generated."
  exit 1
fi

exit 0
