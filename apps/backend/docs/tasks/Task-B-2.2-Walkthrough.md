# Task B-2.2 Walkthrough

## SRS-BENCH-003: Metric Collection Engine
## SRS-BENCH-002: Pluggable Model Execution Harness

### Implementation Overview
1. **Pluggable Architecture**: Replaced the static OllamaHarness with a dynamic `AIRunner` interface (`apps/backend/app/modules/execution/runners/base.py`). Implemented the concrete `OllamaRunner` which handles auto-installation, OS detection, and binary execution.
2. **Auto-Installer**: Downloads platform-specific binaries for macOS and Linux automatically, applying execution permissions and logging status with `rich` console styling.
3. **Metric Collection Engine**: Created `MetricsCollector` (`apps/backend/app/modules/execution/metrics.py`) to accurately capture inference telemetry (Tokens/sec, Latency). Added string-based accuracy metrics.
4. **BDD Integration**: Validated telemetry formatting and exact/substring matching against ground truth using Behave step definitions (`apps/backend/tests/features/steps/metric_collection_steps.py`).

### Test Execution Output

```
1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
14 steps passed, 0 failed, 0 skipped
Took 0min 0.000s
```

```
1 feature passed, 0 failed, 0 skipped
3 scenarios passed, 0 failed, 0 skipped
20 steps passed, 0 failed, 0 skipped
Took 0min 0.013s
```
