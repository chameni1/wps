

# Danneo CMS version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(url, ua):
    kurama = basic.getsource(url, ua)
    header = kurama[2].split('\n')
    regex = []
    for tail in header:
        if 'X-Powered-By: CMS Danneo' in tail:
            regex = re.findall(r'X-Powered-By: CMS Danneo (.*)', tail)
    if regex != []:
        basic.success('Danneo CMS version ' + basic.bold + basic.fgreen + regex[0] + basic.cln + ' detected')
        return regex[0]
    else:
        basic.error('Version detection failed!')
        return '0'
