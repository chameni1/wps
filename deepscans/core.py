def start(id, url, ua, ga, source, ga_content, detection_method='', headers=''):
    if id == "wp":
       
        import deepscans.wp.init as wpscan
        wpscan.start(id, url, ua, ga, source, detection_method)
   