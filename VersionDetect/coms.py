
# Commerce Server version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(url, ua):
    basic.statement('Detecting Commerce Server using headers [Method 1 of 1]')
    kurama = basic.getsource(url, ua)
    header = kurama[2].split('\n')
    regex = []
    for tail in header:
        if 'commerce-server-software:' in tail.lower():
            regex = re.findall(r'commerce-server-software: (.*)', tail, re.IGNORECASE)
    if regex != [] and regex[0] != "":
        basic.success('Commerce Server version ' + basic.bold + basic.fgreen + regex[0] + basic.cln + ' detected')
        return regex[0]
    else:
        basic.error('Version detection failed!')
        return '0'
