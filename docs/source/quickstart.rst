Quick Start Guide
==================

Installation
------------

.. code-block:: bash

   pip install phytrace

Basic Usage
-----------

Here's a simple example:

.. code-block:: python

   from phytrace import trace_run
   from phytrace.invariants import finite, bounded
   import numpy as np

   def damped_oscillator(t, y, k, c, m):
       x, v = y
       return [v, -(k/m)*x - (c/m)*v]

   result = trace_run(
       simulate=damped_oscillator,
       params={'k': 1.0, 'c': 0.1, 'm': 1.0},
       t_span=(0, 10),
       y0=[1.0, 0.0],
       invariants=[finite(), bounded(-10, 10)],
       evidence_dir='./evidence/run_001'
   )

   print(f"Success: {result.success}")

Next Steps
----------

- See :doc:`examples/index` for more examples
- Read :doc:`guides/reproducibility` for best practices
- Check :doc:`api/index` for full API reference

