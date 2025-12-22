# Tutorial 1: First Steps

## Installing phytrace

```bash
pip install phytrace
```

## Running Your First Traced Simulation

```python
from phytrace import trace_run
from phytrace.invariants import finite
import numpy as np

def simple_decay(t, y, k):
    return -k * y

result = trace_run(
    simulate=simple_decay,
    params={'k': 0.5},
    t_span=(0, 10),
    y0=[1.0],
    invariants=[finite()],
    evidence_dir='./evidence/first_run'
)

print(f"Success: {result.success}")
```

## Exploring the Evidence Pack

Check the `./evidence/first_run/` directory for:
- `manifest.json`: Complete metadata
- `plots/`: Generated visualizations
- `data/`: Trajectory data

