# rbardaji/mooda/docs

In this folder are the MarkDown files that make up the Project documentation.

The 'docs' folder and each subfolder contain an index that helps the user move between documentation.

Subfolders bring together MarkDown files with the documentation for a specific topic. For example, the 'examples' subfolder contains all the documentation for mooda examples and tutorials, and the 'api_reference' subfolder contains an explanation of mooda's capabilities.

The MarkDown files that are located inside 'api_reference' and explain a specific function are made with the following template:

```
# <name of the function, arguments with italic style, delete 'self' in class methods>

## Reference

<Short text explaining the function>

### Parameters

* <argument 1>: <Definition of the argument 1>, (<type of argument 1>)
* ...
* <argument n>: <Definition of the argument n>, (<type of argument n>)

### Returns

* <return variable name>: <Explanation of the return>, (<type of return variable>)

## Example

<A short example code to show the basic use of the function. If necessary, you can accompany the code of a small introductory text.>

```pythom
<Write here the Python code. Finish the code adding ```>

Output:

<Write here the output of the Python code>

Return to [<index name>](<index location>).
```

Return to the documentation of the [rbardaji/mooda](rbardaji_mooda.md) folder.
