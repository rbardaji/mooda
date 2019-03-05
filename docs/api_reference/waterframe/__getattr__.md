# WaterFrame.\_\_getattr\_\_(*self*, *key*)

From mooda >= 0.3.

It returns the value of *self.metadata[key]*

## Parameters

    key: str
        key of self.metadata

## Returns

    value:
        Value of self.metadata

## Example

```python
"""Example code"""
from mooda import WaterFrame


def example():
    # Creation of an empty WaterFrame
    wf = WaterFrame()

    # Add some metadata
    wf.metadata['title'] = "Example of WaterFrame"

    print(wf.title)

example()

```

Output:

    Example of WaterFrame

Return to the [WaterFrame Index](index_waterframe.md).