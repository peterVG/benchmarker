#!/usr/bin/env bash

# Master Pre-Commit Hook

echo "========================================"
echo "Running Pre-Commit Hooks..."
echo "========================================"

# 0. Validate Branch-per-Task Workflow
./scripts/verify_branch.sh
if [ $? -ne 0 ]; then
  exit 1
fi

# 1. Validate isolated ports
./scripts/verify_isolated_ports.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Port Validation"
  exit 1
fi

# 2. Validate document sync
./scripts/verify_doc_sync.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Document Sync Validation"
  exit 1
fi

# 3. Validate Bi-directional PRD/SRS Traceability
./scripts/verify_srs_traceability.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Traceability Validation"
  exit 1
fi

# 4. Validate relative links
./scripts/verify_relative_links.sh
if [ $? -ne 0 ]; then

  echo "❌ pre-commit failed: Portable Documentation Validation"
  exit 1
fi

# 4. Validate workspace boundaries
./scripts/verify_workspace_boundaries.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Workspace Boundary Validation"
  exit 1
fi

# 5. Validate centralized logging
./scripts/verify_centralized_logging.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Centralized Logging Validation"
  exit 1
fi

# 6. Validate Elixir formatting
./scripts/verify_formatting.sh
if [ $? -ne 0 ]; then
  echo "❌ pre-commit failed: Formatting Validation"
  exit 1
fi

echo "========================================"
echo "✅ All Pre-Commit Hooks Passed!"
echo "========================================"
exit 0
