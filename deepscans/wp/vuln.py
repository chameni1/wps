

import cmsdb.basic as basic
import json

def start(version,ua):
    if version == "0":
        basic.warning("Skipping version vulnerability scan as WordPress Version wasn't detected")
        wpvdbres = '0' # fix for issue #3
        result = ""
        vfc = ""
    else: ## So we have a version let's scan for vulnerabilities
        basic.info("Checking version vulnerabilities using wpvulns.com")
        vfc = version.replace('.','') # NOT IMPORTANT: vfc = version for check well we have to kill all the .s in the version for looking it up on wpvulndb.. kinda weird if you ask me
        #ws = basic.getsource("https://wpvulndb.com/api/v2/wordpresses/" + vfc, ua)
        # print(ws[0])
        ws = basic.getsource("https://wpvulns.com/version/{0}.json".format(version), ua)
        if ws[0] == "1":
            # wjson = json.loads(ws[1]) + vfd + "['release_date']"
            wpvdbres = '1' ## We have the wpvulndb results
            result = json.loads(ws[1]) #[version]
        else:
            wpvdbres = '0'
            result = ""
            basic.error('Error Retriving data from wpvulndb')
    return [wpvdbres, result, vfc]
