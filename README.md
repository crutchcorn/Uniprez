# Uniprez

## Usage

### Within Script

You may `import uniprez`. When used, `uniprez.getExtensions` will returns a dictionary of extensions that said plugin can handle. An example of this would be: `extensions["mp3"] = <function object>`

### Packaging
In order to package the plugin, you must package them as two seperate plugins within the same file. There must be a minimum of two plugins, one to get the extensions, and one to handle them. There is an enforced naming convention: A plugin with a function begining with `get` is reserved for the ability to get the extensions. If there are only two plugins in your file, the standard is to name these plugins `<plugin>Handle` and `<plugin>Ext`, but this is not enforced.
```
[plugin.plugin]
pluginHandle=plugins.plugin:handleExt
pluginExt=plugins.plugin:getExt
```

### Building Plugins

To define what extensions said plugin can handle, you must have a function that begins with `get`. It must have the following qualities: One argument with a default of None, an if statement returning the string name of the function (within the plugin file) if anything other than None, and an else statement returning a list of the extensions the function mentioned prior can handle. An example of this might be as such:

```python
def getExt(handler = None):
    if handler:
        return "handleExt"
    else:
        return ["extension"]
```
