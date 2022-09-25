import sys
import os
import http.client
import urllib.request
import json
import importlib
from datetime import datetime
import time

import VersionDetect.detect as version_detect # Version detection
import deepscans.core as advanced # Deep scan and Version Detection functions
import cmsdb.basic as basic # All the basic functions
import cmsdb.sc as source # Contains function to detect cms from source code
import cmsdb.header as header # Contains function to detect CMS from gathered http headers
import cmsdb.cmss as cmsdb # Contains basic info about the CMSs
import cmsdb.robots as robots
import cmsdb.generator as generator
import cmsdb.result as result

def main_proc(site,cua):

    # Check for skip_scanned
    if basic.skip_scanned:
        for csite in basic.report_index['results'][0]:
            if site == csite and basic.report_index['results'][0][site]['cms_id'] != '':
                basic.warning('Skipping {0} as it was previously scanned!'.format(basic.red + site + basic.cln))
                return

    basic.clearscreen()
    basic.banner("CMS Detection And Deep Scan")
    basic.info("Scanning Site: " + site)
    basic.statement("User Agent: " + cua)
    basic.statement("Collecting Headers and Page Source for Analysis")
    init_source = basic.getsource(site, cua)
    if init_source[0] != '1':
        basic.error("Couldn't connect to site \n    Error: %s" % init_source[1])
        return
    else:
        scode = init_source[1]
        headers = init_source[2]
        if site != init_source[3] and site + '/' != init_source[3]:
            if basic.redirect_conf == '0':
                basic.info('Target redirected to: ' + basic.bold + basic.fgreen + init_source[3] + basic.cln)
                if not basic.batch_mode:
                    follow_redir = input('[#] Set ' + basic.bold + basic.fgreen + init_source[3] + basic.cln + ' as target? (y/n): ')
                else:
                    follow_redir = 'y'
                if follow_redir.lower() == 'y':
                    site = init_source[3]
                    basic.statement("Reinitiating Headers and Page Source for Analysis")
                    tmp_req = basic.getsource(site, cua)
                    scode = tmp_req[1]
                    headers = tmp_req[2]
            elif basic.redirect_conf == '1':
                site = init_source[3]
                basic.info("Followed redirect, New target: " + basic.bold + basic.fgreen + init_source[3] + basic.cln)
                basic.statement("Reinitiating Headers and Page Source for Analysis")
                tmp_req = basic.getsource(site, cua)
                scode = tmp_req[1]
                headers = tmp_req[2]
            else:
                basic.statement("Skipping redirect to " + basic.bold + basic.red + init_source[3] + basic.cln)
    if scode == '':
        # silly little check thought it'd come handy
        basic.error('Aborting detection, source code empty')
        return

    basic.statement("Detection Started")

    ## init variables
    cms = '' # the cms id if detected
    cms_detected = '0' # self explanotory
    detection_method = '' # ^
    ga = '0' # is generator available
    ga_content = '' # Generator content

    ## Parse generator meta tag
    parse_generator = generator.parse(scode)
    ga = parse_generator[0]
    ga_content = parse_generator[1]

    basic.statement("Using headers to detect CMS (Stage 1 of 4)")
    header_detection = header.check(headers)

    if header_detection[0] == '1':
        detection_method = 'header'
        cms = header_detection[1]
        cms_detected = '1'

    if cms_detected == '0':
        if ga == '1':
            # cms detection via generator
            basic.statement("Using Generator meta tag to detect CMS (Stage 2 of 4)")
            gen_detection = generator.scan(ga_content)
            if gen_detection[0] == '1':
                detection_method = 'generator'
                cms = gen_detection[1]
                cms_detected = '1'
        else:
            basic.statement('Skipping stage 2 of 4: No Generator meta tag found')

    if cms_detected == '0':
        # Check cms using source code
        basic.statement("Using source code to detect CMS (Stage 3 of 4)")
        source_check = source.check(scode, site)
        if source_check[0] == '1':
            detection_method = 'source'
            cms = source_check[1]
            cms_detected = '1'

    if cms_detected == '0':
        # Check cms using robots.txt
        basic.statement("Using robots.txt to detect CMS (Stage 4 of 4)")
        robots_check = robots.check(site, cua)
        if robots_check[0] == '1':
            detection_method = 'robots'
            cms = robots_check[1]
            cms_detected = '1'

    if cms_detected == '1':
        basic.success('CMS Detected, CMS ID: ' + basic.bold + basic.fgreen + cms + basic.cln + ', Detection method: ' + basic.bold + basic.lblue + detection_method + basic.cln)
        basic.update_log('detection_param', detection_method)
        basic.update_log('cms_id', cms) # update log
        basic.statement('Getting CMS info from database') # freaking typo
        cms_info = getattr(cmsdb, cms)
        
        if cms_info['deeps'] == '1' and not basic.light_scan and not basic.only_cms:
            # basic.success('Starting ' + basic.bold + cms_info['name'] + ' deep scan' + basic.cln)
            advanced.start(cms, site, cua, ga, scode, ga_content, detection_method, headers)
            return
        
        elif cms_info['vd'] == '1' and not basic.only_cms:
            basic.success('Starting version detection')
            cms_version = '0' # Failsafe measure
            cms_version = version_detect.start(cms, site, cua, ga, scode, ga_content, headers)
            basic.clearscreen()
            basic.banner("CMS Scan Results")
            result.target(site)
            result.cms(cms_info['name'],cms_version,cms_info['url'])
            basic.update_log('cms_name', cms_info['name']) # update log
            if cms_version != '0' and cms_version != None:
                basic.update_log('cms_version', cms_version) # update log
            basic.update_log('cms_url', cms_info['url']) # update log
            comptime = round(time.time() - basic.cstart, 2)
            log_file = os.path.join(basic.log_dir, 'cms.json')
            result.end(str(basic.total_requests), str(comptime), log_file)
            '''
            basic.result('Target: ', site)
            basic.result("Detected CMS: ", cms_info['name'])
            basic.update_log('cms_name', cms_info['name']) # update log
            if cms_version != '0' and cms_version != None:
                basic.result("CMS Version: ", cms_version)
                basic.update_log('cms_version', cms_version) # update log
            basic.result("CMS URL: ", cms_info['url'])
            basic.update_log('cms_url', cms_info['url']) # update log
            '''
            return
        else:
            # nor version detect neither DeepScan available
            basic.clearscreen()
            basic.banner("CMS Scan Results")
            result.target(site)
            result.cms(cms_info['name'],'0',cms_info['url'])
            basic.update_log('cms_name', cms_info['name']) # update log
            basic.update_log('cms_url', cms_info['url']) # update log
            comptime = round(time.time() - basic.cstart, 2)
            log_file = os.path.join(basic.log_dir, 'cms.json')
            result.end(str(basic.total_requests), str(comptime), log_file)
            '''
            basic.result('Target: ', site)
            basic.result("Detected CMS: ", cms_info['name'])
            basic.update_log('cms_name', cms_info['name']) # update log
            basic.result("CMS URL: ", cms_info['url'])
            basic.update_log('cms_url', cms_info['url']) # update log
            '''
            return
    else:
        print('\n')
        basic.error('CMS Detection failed, if you know the cms please help me improve basic by reporting the cms along with the target by creating an issue')
        print('''

{4}Title:{5} [SUGGESTION] CMS detction failed!
{6}Content:{7}
    - basic Version: {0}
    - Target: {1}
    - Probable CMS: <name and/or cms url>

N.B: Create issue only if you are sure, please avoid spamming!
        '''.format(basic.basic_version, site, basic.bold, basic.cln, basic.bold, basic.cln, basic.bold, basic.cln))
        return
    return 
