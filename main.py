from pkg_resources import iter_entry_points

def getExtensions(group):
    extensions = {}
    handleExtPlugin = {}
    for entry_point in iter_entry_points(group=group, name=None):
        if entry_point.attrs[0] == "handleExt":
            if extensions:
                for extension in extensions:
                    if extensions[extension] == entry_point.module_name: # if extensions["mp3"] == "plugins.lenovo "(this assumes this is second)
                        extensions[extension] = entry_point.load()
            handleExtPlugin[entry_point.module_name] = entry_point.load() # handleExtPlugin["plugins.lenovo"] (this assumes this is first)
        elif entry_point.attrs[0] == "getExt":
            if handleExtPlugin.get(entry_point.module_name, None): # handleExtPlugin["plugins.lenovo"] (this assumes this is second)
                moduleLoad = handleExtPlugin[entry_point.module_name]
            else:
                moduleLoad = entry_point.module_name # This assumed this is first. It allows the extensions to become module_name to be handled by handleExt code
            for extension in entry_point.load()(): # entry_point() would return list of extentions handleExt could handle
                extensions[extension] = moduleLoad # extensions["mp3"]
    return extensions