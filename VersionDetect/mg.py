

# Magento version detection
# Rev 1
import cmsdb.basic as basic
import re
def start(url, ua):
    # Detect version via magento_version (not very accurate)
    basic.statement('Detecting version using magento_version [Method 1 of 1]')
    magento_version = url + '/magento_version'
    changelog_source = basic.getsource(magento_version, ua)
    if changelog_source[0] == '1' and 'Magento' in changelog_source[1]:
        cl_array = changelog_source[1].split('/')
        if cl_array != []:
            basic.success('Magento version ' + basic.bold + cl_array[1] + basic.cln + ' detected')
            return cl_array[1]
        basic.error('Magento version detection failed!')
        return '0'
    else:
        basic.error('Magento version detection failed!')
        return '0'