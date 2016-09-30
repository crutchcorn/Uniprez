# Uniprez

## Usage

### Within Script

You may `import getExtensions from uniprez`. When used, `getExtensions` will returns a dictionary of extensions that said plugin can handle. An example of this would be: `extensions["mp3"] = <function object>`

### Packaging
In order to package the plugin, you must package them as two seperate plugins within the same file. The standard is to name these plugins `<plugin>Handle` and `<plugin>Ext`, but this is not enforced.
```
[plugin.plugin]
pluginHandle=plugins.plugin:handleExt
pluginExt=plugins.plugin:getExt
```

However, the function names are enforced.
Use the function `getExt` to define what extensions said plugin can handle. You must return the data in a list. An example of this would be: `return ["extension"]`

Then, define a function `handleExt` for the script to call when it comes time to handle the extension.


