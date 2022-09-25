

# Drupal version detection

import cmsdb.basic as basic
import re
def start(id, url, ua, ga, source):
    if ga == '1':
        # well for now we only have one way of detecting the version 
        basic.statement('Detecting version using generator meta tag [Method 1 of 2]')
        regex = re.findall(r'<meta name="Generator" content="Drupal (.*?) \(http(s|):\/\/(www\.|)drupal.org\)"', source)
        if regex != []:
            basic.success('Drupal version ' + basic.bold + regex[0][0] + basic.cln + ' detected')
            return regex[0][0]
    else:
        # Detect version via CHANGELOG.txt (not very accurate)
        basic.statement('Detecting version using CHANGELOG.txt [Method 2 of 2]')
        changelog = url + '/CHANGELOG.txt'
        changelog_source = basic.getsource(changelog, ua)
        if changelog_source[0] == '1' and 'Drupal' in changelog_source[1]:
            cl_array = changelog_source[1].split('\n')
            for line in cl_array:
                match = re.findall(r'Drupal (.*?),', line)
                if match != []:
                    basic.success('Drupal version ' + basic.bold + match[0] + basic.cln + ' detected')
                    return match[0]
            basic.error('Drupal version detection failed!')
            return '0'
        else:
            basic.error('Drupal version detection failed!')
            return '0'
    return '0'
