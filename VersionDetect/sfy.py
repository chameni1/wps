

# Sitefinity version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(ga_content):
    ga_content = ga_content.lower()
    regex = re.findall(r'sitefinity (.*)', ga_content)
    if regex != []:
        version = regex[0]
        basic.success('Sitefinity version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
        return version
    else:
        basic.error('Version detection failed!')
        return '0'
