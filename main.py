from pkg_resources import iter_entry_points

def getExtensions(group):
    extensions = {}
    handleExtPlugin = {}
    entry_points = []
    for entry_point in iter_entry_points(group=group, name=None):
        entry_points.append(entry_point)

    orderOfOps = [ 'handleExt', 'getExt'] # This will need to be read from a settings file and have defaults after #1 is implamented

    # Actually sorts the entry_points
    order = {key: i for i, key in enumerate(orderOfOps)}
    entry_points.sort(key=lambda x: order[x.attrs[0]])

    ## Sublists list by value
    # IE: newlist[0] will return all entry_point items that match `handleExt`
    entry_points = [[y for y in entry_points if y.attrs[0]==x] for x in order]

    ### Now comes the exciting part of figuring out how I want to handle these types of things
    ### The current code that resides is not good code and is not expandable in any way. This is just to get things working until I have more time.
    ### Considering the following duct-tape that's falling apart. It's gotta be replaced ASAP
    for epGroup in entry_points:
        for entry_point in epGroup:
            if entry_point.attrs[0] == "handleExt":
                handleExtPlugin[entry_point.module_name] = entry_point.load() # handleExtPlugin["plugins.lenovo"] (this MUST be first)
            elif entry_point.attrs[0] == "getExt":
                if handleExtPlugin.get(entry_point.module_name, None): # handleExtPlugin["plugins.lenovo"] (this MUST be second)
                    moduleLoad = handleExtPlugin[entry_point.module_name]
                for extension in entry_point.load()(): # entry_point() would return list of extentions handleExt could handle
                    extensions[extension] = moduleLoad # extensions["mp3"]
    

    return extensions