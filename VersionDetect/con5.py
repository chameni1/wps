

# Concrete5 CMS version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(ga_content):
    regex = re.findall(r'concrete5 - (.*)', ga_content)
    if regex != []:
        version = regex[0]
        basic.success('Concrete5 CMS version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
        return version
    else:
        basic.error('Version detection failed!')
        return '0'
