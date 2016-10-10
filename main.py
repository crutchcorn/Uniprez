from pkg_resources import iter_entry_points

def getExtensions(group):
    entry_points = []
    for entry_point in iter_entry_points(group=group, name=None):
        entry_points.append(entry_point)

    # This will need to be read from a settings file and have defaults after #1 is implamented
    orderOfOps = ['getExt', 'handleExt']

    # Actually sorts the entry_points based on `orderOfOps`
    # attrs[0] refers to their function name within the plugin
    order = {key: i for i, key in enumerate(orderOfOps)}
    entry_points.sort(key=lambda x: order[x.attrs[0]])

    ## Subdicts list by value
    # IE: newlist['handleExt'] will return all entry_point items that match `handleExt`
    # for each item in order in each plugin
    # IE: getExt (x) for plugin1 (y) => handleExt for plugin1 (y) ==> getExt for plugin2 (x) => handleExt for plugin2 (y)
    # When orderOfOps == pluginFunction name, initialize empty list (if empty, that is) inside of funcDict dictionary
    # Then, append the plugin to the list within funcDict
    funcDict = {}
    for x,y in [(x,y) for x in order for y in entry_points]:
        if y.attrs[0] == x:
            funcDict.setdefault(y.attrs[0], []).append(y)

    ## Gathering exensions
    extensions = {}
    # for each item in order, assuming that the item begins with "get"
    for funcName in (oName for oName in order if oName.startswith("get")):
        # For each dict of function __name__ value that matches funcName (in this case, getExt). Can be dynamic when #1 done
        for getEx in funcDict[funcName]:
            # run getEx with `True` argument to load name of function __name__ value that matches return (often refered to as the handler)
            for handle in funcDict[getEx.load()(True)]:
                # If the file which the functions within handle and getEx match
                if handle.module_name == getEx.module_name:
                    # For each extension returned from default getExt constructor
                    for extension in getEx.load()():
                        # Make the dictionary extensions have a list of extensions that could load the handler of said extensions
                        extensions[extension] = handle.load()

    return extensions