# Scripts Directory

This directory contains **executable scripts** that the AI agent can run using the `code_interpreter` tool to validate logic, simulate load, or perform automated checks.

## Purpose

Scripts enable the agent to:
- ✅ **Validate** business logic without deploying code
- ✅ **Simulate** load testing or edge cases
- ✅ **Verify** calculations (e.g., fee estimation, chunking logic)
- ✅ **Automate** repetitive verification tasks

## What Goes Here

### Validation Scripts
Scripts that verify business logic or calculations:
- `validate_chunking_logic.py` - Verify file chunking algorithm
- `calculate_storage_fees.py` - Estimate Arweave storage costs
- `verify_encryption.py` - Test encryption/decryption logic

### Simulation Scripts
Scripts that simulate system behavior:
- `simulate_concurrent_uploads.py` - Test load handling
- `simulate_network_failure.py` - Test retry logic
- `generate_test_data.py` - Create test datasets

### Analysis Scripts
Scripts that analyze or report on data:
- `analyze_retention_policy.py` - Verify records retention logic
- `audit_dependencies.py` - Check for "high gravity" dependencies
- `generate_coverage_report.py` - Test coverage analysis

## Example Structure

```
scripts/
├── validation/
│   ├── validate_chunking_logic.py
│   └── calculate_storage_fees.py
├── simulation/
│   ├── simulate_concurrent_uploads.py
│   └── generate_test_data.py
└── analysis/
    └── analyze_retention_policy.py
```

## How Skills Use Scripts

Skills can execute scripts using the `code_interpreter` tool:

```yaml
---
name: Architecture Validator
description: Validates system architecture decisions
allowed-tools:
  - code_interpreter
scripts:
  - scripts/validation/calculate_storage_fees.py
---

# Architecture Validator Skill

When validating the file upload architecture:
1. Read the architecture.md
2. Execute scripts/validation/calculate_storage_fees.py
3. Verify that estimated costs align with PRD budget constraints
4. Report any issues
```

## Example Script: Chunking Validation

**`scripts/validation/validate_chunking_logic.py`:**

```python
#!/usr/bin/env python3
"""
Validates file chunking logic for Arweave uploads.

Usage:
    python validate_chunking_logic.py --file-size 450 --chunk-size 100
"""

import argparse

def calculate_chunks(file_size_mb, chunk_size_mb):
    """Calculate number of chunks needed."""
    import math
    return math.ceil(file_size_mb / chunk_size_mb)

def validate_chunking(file_size_mb, chunk_size_mb, max_file_size=500):
    """Validate chunking logic against requirements."""
    results = {
        "file_size_mb": file_size_mb,
        "chunk_size_mb": chunk_size_mb,
        "num_chunks": calculate_chunks(file_size_mb, chunk_size_mb),
        "valid": True,
        "errors": []
    }
    
    # SRS-UPLOAD-001: Maximum file size is 500MB
    if file_size_mb > max_file_size:
        results["valid"] = False
        results["errors"].append(f"File size {file_size_mb}MB exceeds maximum {max_file_size}MB")
    
    # SRS-UPLOAD-002: Chunk size must be at least 1MB
    if chunk_size_mb < 1:
        results["valid"] = False
        results["errors"].append(f"Chunk size {chunk_size_mb}MB is below minimum 1MB")
    
    # SRS-PERF-001: Files under 10MB should not be chunked
    if file_size_mb < 10 and results["num_chunks"] > 1:
        results["valid"] = False
        results["errors"].append(f"File {file_size_mb}MB should not be chunked (< 10MB)")
    
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate file chunking logic")
    parser.add_argument("--file-size", type=float, required=True, help="File size in MB")
    parser.add_argument("--chunk-size", type=float, default=100, help="Chunk size in MB")
    
    args = parser.parse_args()
    
    results = validate_chunking(args.file_size, args.chunk_size)
    
    print(f"File Size: {results['file_size_mb']}MB")
    print(f"Chunk Size: {results['chunk_size_mb']}MB")
    print(f"Number of Chunks: {results['num_chunks']}")
    print(f"Valid: {results['valid']}")
    
    if not results["valid"]:
        print("\nErrors:")
        for error in results["errors"]:
            print(f"  - {error}")
        exit(1)
    else:
        print("\n✅ Chunking logic is valid!")
        exit(0)
```

## Agent Workflow with Scripts

```
USER: Verify that our chunking logic meets the SRS requirements

AGENT: [Activates Architecture Validator skill]
AGENT: [Skill specifies scripts/validation/validate_chunking_logic.py]
AGENT: [Executes script with test cases]
AGENT: [Reports results]

OUTPUT:
✅ Test 1: 5MB file → 1 chunk (valid)
✅ Test 2: 450MB file → 5 chunks (valid)
✅ Test 3: 500MB file → 5 chunks (valid)
❌ Test 4: 501MB file → Error: exceeds maximum (valid error handling)
```

## Best Practices

### 1. Make Scripts Executable
```bash
chmod +x scripts/validation/validate_chunking_logic.py
```

### 2. Include Documentation
Every script should have:
- Docstring explaining purpose
- Usage examples
- SRS requirement references

### 3. Use Standard Libraries
Minimize dependencies to keep scripts portable:
- ✅ Use Python standard library when possible
- ⚠️ If external deps needed, document in `requirements.txt`

### 4. Return Exit Codes
```python
if validation_passed:
    exit(0)  # Success
else:
    exit(1)  # Failure
```

### 5. Map to SRS Requirements
```python
# SRS-UPLOAD-001: Maximum file size is 500MB
if file_size_mb > 500:
    results["errors"].append("Exceeds SRS-UPLOAD-001 limit")
```

## Progressive Disclosure Benefits

Scripts are only loaded and executed when:
- A skill explicitly requires them
- The agent needs to validate logic
- The user requests simulation or analysis

This saves tokens and execution time when scripts aren't needed.

## Example: Local-First Records Retention

**`scripts/analysis/analyze_retention_policy.py`:**

```python
#!/usr/bin/env python3
"""
Analyzes records retention policy for compliance.

Validates that retention periods meet legal requirements
and calculates storage costs for permanent archival.
"""

import json
from datetime import datetime, timedelta

def analyze_retention(records_file, retention_years=7):
    """Analyze records retention policy."""
    with open(records_file) as f:
        records = json.load(f)
    
    results = {
        "total_records": len(records),
        "compliant": 0,
        "non_compliant": 0,
        "permanent": 0,
        "estimated_cost_usd": 0
    }
    
    for record in records:
        created = datetime.fromisoformat(record["created_at"])
        retention_end = created + timedelta(days=retention_years * 365)
        
        if record["retention_type"] == "permanent":
            results["permanent"] += 1
            results["compliant"] += 1
            # Arweave permanent storage cost estimation
            size_mb = record["size_mb"]
            cost_per_mb = 0.005  # Example rate
            results["estimated_cost_usd"] += size_mb * cost_per_mb
        elif datetime.now() < retention_end:
            results["compliant"] += 1
        else:
            results["non_compliant"] += 1
    
    return results

if __name__ == "__main__":
    import sys
    results = analyze_retention(sys.argv[1])
    print(json.dumps(results, indent=2))
```

**Agent uses this to:**
1. Validate retention logic before deployment
2. Estimate storage costs for budget planning
3. Verify compliance with legal requirements

## Integration with Antigravity Workflow

```
1. Write SRS requirement: "Records must be retained for 7 years"
2. Create validation script: scripts/analysis/analyze_retention_policy.py
3. Agent executes script during architecture validation
4. Script verifies logic meets SRS-RET-001
5. Agent reports compliance status
```

Scripts become **executable documentation** that proves your system meets requirements!
