from pkg_resources import iter_entry_points

def getExtensions(group):
    entry_points = []
    for entry_point in iter_entry_points(group=group, name=None):
        entry_points.append(entry_point)

    orderOfOps = ['getExt', 'handleExt'] # This will need to be read from a settings file and have defaults after #1 is implamented

    # Actually sorts the entry_points
    order = {key: i for i, key in enumerate(orderOfOps)}
    entry_points.sort(key=lambda x: order[x.attrs[0]])

    ## Subdicts list by value
    # IE: newlist['handleExt'] will return all entry_point items that match `handleExt`
    funcDict = {}
    for x,y in [(x,y) for x in order for y in entry_points]:
        if y.attrs[0] == x:
            funcDict.setdefault(y.attrs[0], []).append(y)


    ### Now comes the exciting part of figuring out how I want to handle these types of things
    ### The current code that resides is not good code and is not expandable in any way. This is just to get things working until I have more time.
    ### Considering the following duct-tape that's falling apart. It's gotta be replaced ASAP
    extensions = {}
    handleExtPlugin = {}
    for handleEx in funcDict['handleExt']:
        handleExtPlugin[handleEx.module_name] = handleEx.load() # handleExtPlugin["plugins.lenovo"] (this MUST be first)
    for getEx in funcDict['getExt']:
        moduleLoad = handleExtPlugin[getEx.module_name] # handleExtPlugin["plugins.lenovo"] (this MUST be second)
        for extension in getEx.load()(): # entry_point() would return list of extentions handleExt could handle
            extensions[extension] = moduleLoad # extensions["mp3"]

    return extensions