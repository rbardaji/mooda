# WaterFrame.empty(*self*)

It return True if the dataframe is empty.

## Returns

    empty: bool

## Example

```python
from mooda import WaterFrame

def example():
    """
    Example of code.
    It creates a WaterFrame and prints a message if the WaterFrame doesn't have data.
    """
    wf = WaterFrame()

    if wf.empty():
        print("The WaterFrame is empty.")

example()
```

Return to the [WaterFrame Index](index_waterframe.md).
