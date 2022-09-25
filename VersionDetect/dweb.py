

# Dynamicweb version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(ga_content):
    basic.statement('Detecting Dynamicweb version using generator meta tag [Method 1 of 1]')
    regex = re.findall(r'Dynamicweb (.*)', ga_content)
    if regex != []:
        version = regex[0]
        basic.success('Dynamicweb version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
        return version
    else:
        basic.error('Version detection failed!')
        return '0'
