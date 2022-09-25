import cmsdb.basic as basic
import VersionDetect.wp as wordpress_version_detect
import deepscans.wp.userenum as wp_user_enum
import deepscans.wp.vuln as wp_vuln_scan
import deepscans.wp.pluginsdetect as wp_plugins_enum
import deepscans.wp.themedetect as wp_theme_enum
import deepscans.wp.pathdisc as path_disclosure
import deepscans.wp.check_reg as check_reg
import cmsdb.result as sresult
import time
import re
import os

def start(id, url, ua, ga, source, detection_method):
    '''
    id = ID of the cms
    url = URL of target
    ua = User Agent
    ga = [0/1] is GENERATOR meta tag available
    source = source code
    '''

   
    if id == "wp":
        # referenced before assignment fix
        vulnss = version = wpvdbres = result = plugins_found = usernames = usernamesgen = '0'

        basic.statement('Starting WordPress DeepScan')


        # Check if site really is WordPress
        if detection_method == 'source':
            # well most of the wordpress false positives are from source detections.
            basic.statement('Checking if the detection is false positive')
            temp_domain = re.findall('^(?:https?:\/\/)?(?:[^@\n]+@)?(?:www\.)?([^:\/\n\?\=]+)', url)[0]
            wp_match_pattern = temp_domain + '\/wp-(content|include|admin)\/'
            if not re.search(wp_match_pattern, source):
                basic.error('Detection was false positive! basic is quitting!')
                basic.success('Run basic with {0}{1}{2} argument next time'.format(basic.fgreen, '--ignore-cms wp', basic.cln))
                #basic.handle_quit()
                return

        # Version detection
        version = wordpress_version_detect.start(id, url, ua, ga, source)

        ## Check for minor stuffs like licesnse readme and some open directory checks
        basic.statement("Initiating open directory and files check")

        ## Readme.html
        readmesrc = basic.getsource(url + '/readme.html', ua)
        if readmesrc[0] != '1': ## something went wrong while getting the source codes
            basic.statement("Couldn't get readme file's source code most likely it's not present")
            readmefile = '0' # Error Getting Readme file
        elif 'Welcome. WordPress is a very special project to me.' in readmesrc[1]:
            readmefile = '1' # Readme file present
        else:
            readmefile = '2'

        ## license.txt
        licsrc = basic.getsource(url + '/license.txt', ua)
        if licsrc[0] != '1':
            basic.statement('license file not found')
            licfile = '0'
        elif 'WordPress - Web publishing software' in licsrc[1]:
            licfile = '1'
        else:
            licfile = '2'

        ## wp-content/uploads/ folder
        wpupsrc = basic.getsource(url + '/wp-content/uploads/', ua)
        if wpupsrc[0] != '1':
            wpupdir = '0'
        elif 'Index of /wp-content/uploads' in wpupsrc[1]:
            wpupdir = '1'
        else:
            wpupdir = '2'

        ## xmlrpc
        xmlrpcsrc = basic.getsource(url + '/xmlrpc.php', ua)
        if xmlrpcsrc[0] != '1':
            basic.statement('XML-RPC interface not available')
            xmlrpc = '0'
        elif 'XML-RPC server accepts POST requests only.' in xmlrpcsrc[1]:
            xmlrpc = '1'
        else:
            xmlrpc = '2'

        ## Path disclosure
        basic.statement('Looking for potential path disclosure')
        path = path_disclosure.start(url, ua)
        if path != "":
            basic.success('Path disclosure detected, path: ' + basic.bold + path + basic.cln)

        ## Check for user registration
        usereg = check_reg.start(url,ua)
        reg_found = usereg[0]
        reg_url = usereg[1]

        ## Plugins Enumeration
        plug_enum = wp_plugins_enum.start(source)
        plugins_found = plug_enum[0]
        plugins = plug_enum[1]

        ## Themes Enumeration
        theme_enum = wp_theme_enum.start(source,url,ua)
        themes_found = theme_enum[0]
        themes = theme_enum[1]

        ## User enumeration
        uenum = wp_user_enum.start(id, url, ua, ga, source)
        usernamesgen = uenum[0]
        usernames = uenum[1]

        ## Version Vulnerability Detection
        if version != '0':
            version_vuln = wp_vuln_scan.start(version, ua)
            wpvdbres = version_vuln[0]
            result = version_vuln[1]
            if wpvdbres != '0' and version != '0':
                vulnss = len(result['vulnerabilities'])
            vfc = version_vuln[2]

        ### Deep Scan Results comes here
        comptime = round(time.time() - basic.cstart, 2)
        log_file = os.path.join(basic.log_dir, 'cms.json')
        basic.clearscreen()
        basic.banner("Deep Scan Results")
        sresult.target(url)
        sresult.cms('WordPress', version, 'https://wordpress.org')
        #basic.result("Detected CMS: ", 'WordPress')
        basic.update_log('cms_name','WordPress') # update log
        #basic.result("CMS URL: ", "https://wordpress.org")
        basic.update_log('cms_url', "https://wordpress.org") # update log

        sresult.menu('[WordPress Deepscan]')
        item_initiated = False
        item_ended = False


        if readmefile == '1':
            sresult.init_item("Readme file found: " + basic.fgreen + url + '/readme.html' + basic.cln)
            basic.update_log('wp_readme_file',url + '/readme.html')
            item_initiated = True


        if licfile == '1':
            basic.update_log('wp_license', url + '/license.txt')
            if item_initiated == False:
                sresult.init_item("License file: " + basic.fgreen + url + '/license.txt' + basic.cln)
            else:
                sresult.item("License file: " + basic.fgreen + url + '/license.txt' + basic.cln)

        if wpvdbres == '1':
            if item_initiated == False:
                sresult.init_item('Changelog: ' + basic.fgreen + str(result['changelog_url']) + basic.cln)
            else:
                sresult.item('Changelog: ' + basic.fgreen + str(result['changelog_url']) + basic.cln)
            basic.update_log('wp_changelog_file',str(result['changelog_url']))

        if wpupdir == '1':
            basic.update_log('wp_uploads_directory',url + '/wp-content/uploads')
            if item_initiated == False:
                sresult.init_item("Uploads directory has listing enabled: " + basic.fgreen + url + '/wp-content/uploads' + basic.cln)
            else:
                sresult.item("Uploads directory has listing enabled: " + basic.fgreen + url + '/wp-content/uploads' + basic.cln)


        if xmlrpc == '1':
            basic.update_log('xmlrpc', url + '/xmlrpc.php')
            if item_initiated == False:
                sresult.init_item("XML-RPC interface: "+ basic.fgreen + url + '/xmlrpc.php' + basic.cln)
            else:
                sresult.item("XML-RPC interface: " + basic.fgreen + url + '/xmlrpc.php' + basic.cln)


        if reg_found == '1':
            sresult.item('User registration enabled: ' + basic.bold + basic.fgreen + reg_url + basic.cln)
            basic.update_log('user_registration', reg_url)


        if path != "":
            sresult.item('Path disclosure: ' + basic.bold + basic.orange + path + basic.cln)
            basic.update_log('path', path)


        if plugins_found != 0:
            plugs_count = len(plugins)
            sresult.init_item("Plugins Enumerated: " + basic.bold + basic.fgreen + str(plugs_count) + basic.cln)
            wpplugs = ""
            for i, plugin in enumerate(plugins):
                plug = plugin.split(':')
                wpplugs = wpplugs + plug[0] + ' Version ' + plug[1] + ','
                if i == 0 and i != plugs_count - 1:
                    sresult.init_sub('Plugin: ' + basic.bold + basic.fgreen + plug[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + plug[1] + basic.cln)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/plugins/' + plug[0] + basic.cln)
                elif i == plugs_count - 1:
                    sresult.empty_sub()
                    sresult.end_sub('Plugin: ' + basic.bold + basic.fgreen + plug[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + plug[1] + basic.cln, True, False)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/plugins/' + plug[0] + basic.cln, True, False)
                else:
                    sresult.empty_sub()
                    sresult.sub_item('Plugin: ' + basic.bold + basic.fgreen + plug[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + plug[1] + basic.cln)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/plugins/' + plug[0] + basic.cln)
            basic.update_log('wp_plugins', wpplugs)
            sresult.empty_item()

        if themes_found != 0:
            thms_count = len(themes)
            sresult.init_item("Themes Enumerated: " + basic.bold + basic.fgreen + str(thms_count) + basic.cln)
            wpthms = ""
            for i,theme in enumerate(themes):
                thm = theme.split(':')
                thmz = thm[1].split('|')
                wpthms = wpthms + thm[0] + ' Version ' + thmz[0] + ','
                if i == 0 and i != thms_count - 1:
                    sresult.init_sub('Theme: ' + basic.bold + basic.fgreen + thm[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + thmz[0] + basic.cln)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + basic.bold + basic.fgreen + url + thmz[1] + basic.cln)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/themes/' + thm[0] + basic.cln)
                elif i == thms_count - 1:
                    sresult.empty_sub(True)
                    sresult.end_sub('Theme: ' + basic.bold + basic.fgreen + thm[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + thmz[0] + basic.cln, True, False)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + basic.bold + basic.fgreen + url + thmz[1] + basic.cln, True, False)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/themes/' + thm[0] + basic.cln, True, False)
                else:
                    sresult.sub_item('Theme: ' + basic.bold + basic.fgreen + thm[0] + basic.cln)
                    sresult.init_subsub('Version: ' + basic.bold + basic.fgreen + thmz[0] + basic.cln)
                    if thmz[1] != '':
                        sresult.subsub('Theme Zip: ' + basic.bold + basic.fgreen + url + thmz[1] + basic.cln)
                    sresult.end_subsub('URL: ' + basic.fgreen + url + '/wp-content/themes/' + thm[0] + basic.cln)
            basic.update_log('wp_themes', wpthms)
            sresult.empty_item()


        if usernamesgen == '1':
            user_count = len(usernames)
            sresult.init_item("Usernames harvested: " + basic.bold + basic.fgreen + str(user_count) + basic.cln)
            wpunames = ""
            for i,u in enumerate(usernames):
                wpunames = wpunames + u + ","
                if i == 0 and i != user_count - 1:
                    sresult.init_sub(basic.bold + basic.fgreen + u + basic.cln)
                elif i == user_count - 1:
                    sresult.end_sub(basic.bold + basic.fgreen + u + basic.cln)
                else:
                    sresult.sub_item(basic.bold + basic.fgreen + u + basic.cln)
            basic.update_log('wp_users', wpunames)
            sresult.empty_item()

        if version != '0':
            # basic.result("Version: ", version)
            basic.update_log('wp_version', version)
            if wpvdbres == '1':
                sresult.end_item('Version vulnerabilities: ' + basic.bold + basic.fgreen + str(vulnss) + basic.cln)
                basic.update_log('wp_vuln_count', str(vulnss))
                basic.update_log("wp_vulns", result, False)
                if vulnss > 0:
                    for i,vuln in enumerate(result['vulnerabilities']):
                        if i == 0 and i != vulnss - 1:
                            sresult.empty_sub(False)
                            sresult.init_sub(basic.bold + basic.fgreen + str(vuln['name']) + basic.cln, False)
                            # sresult.init_subsub("Type: " + basic.bold + basic.fgreen + str(vuln['vuln_type']) + basic.cln, False, True)
                            # sresult.subsub("Link: " + basic.bold + basic.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + basic.cln, False, True)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + basic.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + vuln["cve"] + basic.cln, False, True)

                            
                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + basic.fgreen + str(ref) + basic.cln, False, True)
                            sresult.end_subsub("Fixed In Version: " + basic.bold + basic.fgreen + str(vuln['fixed_in']) + basic.cln, False, True)

                        elif i == vulnss - 1:
                            sresult.empty_sub(False)
                            sresult.end_sub(basic.bold + basic.fgreen + str(vuln['name']) + basic.cln, False)
                            # sresult.init_subsub("Type: " + basic.bold + basic.fgreen + str(vuln['vuln_type']) + basic.cln, False, False)
                            # sresult.subsub("Link: " + basic.bold + basic.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + basic.cln, False, False)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + basic.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + vuln["cve"] + basic.cln, False, False)

                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + basic.fgreen + str(ref) + basic.cln, False, False)

                            sresult.end_subsub("Fixed In Version: " + basic.bold + basic.fgreen + str(vuln['fixed_in']) + basic.cln, False, False)
                        else:
                            sresult.empty_sub(False)
                            sresult.sub_item(basic.bold + basic.fgreen + str(vuln['name']) + basic.cln, False)
                            #sresult.init_subsub("Type: " + basic.bold + basic.fgreen + str(vuln['vuln_type']) + basic.cln, False, True)
                            #sresult.subsub("Link: " + basic.bold + basic.fgreen + "http://wpvulndb.com/vulnerabilities/" + str(vuln['id']) + basic.cln, False, True)
                            strvuln = str(vuln)
                            if vuln['cve'] != "":
                                sresult.subsub("CVE: " + basic.fgreen + "http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-" + str(ref) + basic.cln, False, True)
                                    

                            if vuln["references"] != []:
                                for ref in vuln["references"]:
                                    sresult.subsub("Reference: " + basic.fgreen + str(ref) + basic.cln, False, True)

                            sresult.end_subsub("Fixed In Version: " + basic.bold + basic.fgreen + str(vuln['fixed_in']) + basic.cln, False, True)
        sresult.end(str(basic.total_requests), str(comptime), log_file)
        return


    return
