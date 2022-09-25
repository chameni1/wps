

# YAF version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(source):
    regex = re.findall(r'Powered by YAF.NET (\d.*?)</a>', source)
    if regex != []:
        if regex[0] != '' and regex[0] != ' ':
            version = regex[0].replace(' ', '')
            basic.success('YAF version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
            return version

    basic.error('Version detection failed!')
    return '0'
