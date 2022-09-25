

import os
import json
import datetime
import cmsdb.basic as basic
import logging, traceback

def init(basic_dir, report_dir=""):
    '''
    Creates/Updates result index
    Needed Parameters:
    basic_dir = basic directory / access_directory
    report_dir = path to report directory leave empty if default
    '''
    # Create a json list of all the sites scanned and save it to <basic_dir>/reports.json
    basic.info('Updating basic result index...')
    if os.path.isdir(basic_dir):
        index_file = os.path.join(basic_dir, 'reports.json')
        if report_dir == "":
            report_dir = os.path.join(basic_dir, 'Result')
        if os.path.isdir(report_dir):
            result_index = {}
            result_dirs = os.listdir(report_dir)
            for result_dir in result_dirs:
                scan_file = os.path.join(report_dir, result_dir, 'cms.json')
                if os.path.isfile(scan_file):
                    try:
                        with open(scan_file, 'r', encoding='utf8') as sf:
                            scan_content = json.loads(sf.read())
                        scan_url = scan_content['url']
                        result_index[scan_url] = {"cms_id": scan_content['cms_id'],"date": scan_content['last_scanned'],"report":scan_file}
                    except Exception as e:
                        logging.error(traceback.format_exc())
                        basic.statement('Skipping invalid basic result: ' + scan_file)
            # Write index
            result_index = {"last_updated":str(datetime.datetime.now()), "results":[result_index]}
            inf = open(index_file, 'w+')
            inf.write(json.dumps(result_index, sort_keys=False, indent=4))
            inf.close()
            basic.success('Report index updated successfully!')
            basic.report_index = result_index
            return ['1', 'Report index updated successfully!']

        else:
            basic.error('Result directory does not exist!')
            return [0, 'Result directory does not exist']

    else:
        basic.error('Invalid basic directory passed!')
        return [0, 'basic directory does not exist']
