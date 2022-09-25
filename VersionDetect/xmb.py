

# XMB version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(source):
    regex = re.findall(r'<!-- Powered by XMB (\d.*?) ', source)
    if regex != []:
        if regex[0] != '' and regex[0] != ' ':
            version = regex[0]
            basic.success('XMB version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
            return version
    else:
        regex = re.findall(r'Powered by XMB (\d.*?) ', source)
        if regex != []:
            if regex[0] != '' and regex[0] != ' ':
                version = regex[0]
                basic.success('XMB version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
                return version

    basic.error('Version detection failed!')
    return '0'
