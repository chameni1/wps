

import cmsdb.basic as basic
import re
import json

def start(source):
    basic.info('Starting passive plugin enumeration')
    plug_regex = re.compile('wp-content/plugins/([^/]+)/.+ver=([0-9\.]+)')
    results = plug_regex.findall(source)
    plugins = []
    found = 0
    for result in results:
        # found += 1
        name = result[0].replace('-master','').replace('.min','')
        nc = name + ":"
        if nc not in str(plugins):
            version = result[1]
            each_plugin = name + ":" + version
            plugins.append(each_plugin)
    plugins = set(plugins)
    found = len(plugins)
    if found > 0:
        if found == 1:
            basic.success(basic.bold + basic.fgreen + str(found) + " Plugin enumerated!")
        else:
            basic.success(basic.bold + basic.fgreen + str(found) + " Plugins enumerated!")
    else:
        basic.error('No plugins enumerated!')
    return [found, plugins]
