# Uniprez Design Process

## Description
The idea behind this microlibrary is to handle plugins and report back to the main script which plugins handle what. Some examples of this are:
- Which plugin would handle which mimetype
- Which plugin would handle which URL

## Design Goals
- Implamentability
	- Minimal amount of code in program to implament
	- Minimal amount of code in plugin to implament

## General Idea

Ideally, it would be best to have two different functions. One that would return the handlable items, one that would handle said items. That being said, it may not be possible from a technical standpoint.

## Plugin Information Given
This is a table of respective values of `entry_point`, given a `for entry_point in iter_entry_points(group=group, name=None):` loop.

|     name     |   module_name  |          dist          |     attrs      |
|   --------   |    --------    |         --------       |    --------    |
| lenovoHandle | plugins.lenovo | DriverDownloader 0.0.1 | ('handleExt',) |
| lenovoExt    | plugins.lenovo | DriverDownloader 0.0.1 | ('getExt',)    |

As you can tell, they were packaged in the same `dist`, and are in the same module (file). This is the way that these plugins would be handled to match with my design goals. My initial idea was to use the `lenovoExt` plugin to check for what extenstions the `lenovoHandle` plugin can handle. After it did this, it would tag the `lenovoHandle` in a dict of extensions by seaching for all plugins within the same `module_name` (as the module name is the file that the plugin resides), looking for one with the `attrs`: `handleExt`, and tag said plugin to load later with `load_entry_point(dist, group, name)`. I soon realized I don't need `load_entry_point` at all. The code that is currently implamented is what I went with, but before I realized that it was possible, here are other routes I decided to go down.

### Plugin Without Function Definition

You could try to be tricky by changing the plugin definition to not include the function so instead of `pluginname=plugins.pluginfile:function`, you simply use `pluginname=plugins.pluginfile`, but it turns out to be a little trickier than that.

For example, if you run:
```python
for entry_point in iter_entry_points(group='plugingroup.plugin', name=None):
    print(entry_point.load())
```
It will output exactly as expected:
```python
<module 'plugins.plugingroup' from 'c:\\users\\path\\to\\plugins\\pluginfile.py'>
```

However, when you try to append this to a list, it will only be added as a string.
```python
available_methods = []
for entry_point in iter_entry_points(group='plugingroup.plugin', name=None):
    available_methods.append(entry_point.name)
type(available_methods[0])
```
It will output:
```python
<class 'str'>
```

This is likely due to `inter_entry_points` being a generator, but that theory needs confirmation.
```python
>>> type(iter_entry_points(group="lenovo.plugin", name=None))
<class 'generator'>
```

### Path Import
However, a keen eye will notice that if you check for the value `__file__` of a given module object, it will output the file the module resides in: `c:\\users\\path\\to\\plugins\\pluginfile.py`
`"So, simple!"` I can hear you thinking. `"We'll import the module from the pathname."`. Well, no.

For Python 3.5+, you'd use:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.MyClass()
```

For Python 3.3 and 3.4, it's possible - but you have to use a deprecated method (as of Python 3.4):
```python
from importlib.machinery import SourceFileLoader
foo = SourceFileLoader("module.name", "/path/to/file.py").load_module()
foo.MyClass()
```
_[This section was lifted from a stackoverflow question](http://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path)_

As you can see, this is less than optimal. Not to mention the further issues that arise from trying to import from a path. Some that I can think of (without testing), include: permissions, windows derping on path [common], versions of Python being outdated with any given distribution method of Python, etc etc.

### Check Against Filename Approach
Possibly, one could: 
- Check all plugins for path name
- Check for function name (IE: `handler()` and `informant()`)
- If both are found for any given plugin, run `informant()` and return what `handler()` can handle
	- Add some kind of error handling if both functions are not found for any given plugin
- Load `handler()` from `load_entry_point(dist, group, name)`

However, that won't work, as (when packaged without function reference [which is needed for the trick of getting filenames]) you cannot link a function to a function. `function = entry_point.load().function()` will not work and will break things. However, it MIGHT be possible to check against `entry_point.module_name` (refer above) and mark THAT as the working plugin. This, though, arises many issues with possible duplicates and path issues caused by a difference of packaging.

- - -

## Class Workaround (untested)

To combat this, Alexis suggested to wrap everything around a class:
```python
for cls in plugins:
    for mime in cls.implements:
        plugin_dict[mime] = cls.handle

class EXIFPlugin(furl.Plugin):
    implements = ["image/png", …]
    def handle(self, file_):
        # stuff
```