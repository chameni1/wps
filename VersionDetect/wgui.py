

# WebGUI version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(ga_content):
    regex = re.findall(r'WebGUI (.*)', ga_content)
    if regex != []:

        if ')' in regex[0]:
            # This could be done by regex right? if you know how to do so proudly create an issue and show me the way ;)
            version = regex[0].replace(')','')
        else:
            version = regex[0]

        basic.success('WebGUI version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
        return version
    else:
        basic.error('Version detection failed!')
        return '0'
