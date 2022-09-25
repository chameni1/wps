

# Ophal version detection
# Rev 1

import cmsdb.basic as basic
import re

def start(ga_content, url, ua):
    ga_content = ga_content.lower()
    regex = re.findall(r'ophal (.*?) \(ophal.org\)', ga_content)
    if regex != []:
        version = regex[0]
        basic.success('Ophal version ' + basic.bold + basic.fgreen + version + basic.cln + ' detected')
        return version
    else:
        kurama = basic.getsource(url, ua) # copypasta
        header = kurama[2].split('\n')
        regex = []
        for tail in header:
            if 'x-powered-by' in tail:
                regex = re.findall(r'x-powered-by: Ophal (.*?) \(ophal.org\)', tail)
        if regex != []:
            basic.success('Ophal version ' + basic.bold + basic.fgreen + regex[0] + basic.cln + ' detected')
            return regex[0]
        else:
            basic.error('Version detection failed!')
            return '0'
