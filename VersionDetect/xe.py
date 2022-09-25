

# XpressEngine version detection
# Rev 1
import cmsdb.basic as basic
import re

def start(ga_content):
    regex = re.findall(r'XpressEngine (.*)', ga_content)
    if regex != []:
        basic.success('XpressEngine version ' + basic.bold + basic.fgreen + regex[0] + basic.cln + ' detected')
        return regex[0]
    else:
        basic.error('Version detection failed!')
        return '0'
