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

    extensions = {}
    for getEx in funcDict['getExt']:
        for handle in funcDict[getEx.load()(True)]:
            if handle.module_name == getEx.module_name:
                for extension in getEx.load()():
                    extensions[extension] = handle.load()

    return extensions