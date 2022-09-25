
def start(id, url, ua, ga, source, ga_content, headers):
    if id == "wp":
        # trust me more will be added soon
        import VersionDetect.wp as wpverdetect
        wpver = wpverdetect.start(id, url, ua, ga, source)
        return wpver
    elif id == 'joom':
        import VersionDetect.joom as joomverdetect
        joomver = joomverdetect.start(id, url, ua, ga, source)
        return joomver
    elif id == 'dru':
        import VersionDetect.dru as druverdetect
        druver = druverdetect.start(id, url, ua, ga, source)
        return druver
    elif id == 'xe':
        import VersionDetect.xe as xeverdetect
        xever = xeverdetect.start(ga_content)
        return xever
    elif id == 'wgui':
        import VersionDetect.wgui as wguiverdetect
        wguiver = wguiverdetect.start(ga_content)
        return wguiver
    elif id == 'dncms':
        import VersionDetect.dncms as dncmsverdetect
        dncmsver = dncmsverdetect.start(url, ua)
        return dncmsver
    elif id == 'con5':
        import VersionDetect.con5 as con5verdetect
        con5ver = con5verdetect.start(ga_content)
        return con5ver
    elif id == 'yaf':
        import VersionDetect.yaf as yafverdetect
        yafver = yafverdetect.start(source)
        return yafver
    elif id == 'mg':
        import VersionDetect.mg as mgverdetect
        mgver = mgverdetect.start(url, ua)
        return mgver
    elif id == 'coms':
        import VersionDetect.coms as comsverdetect
        comsver = comsverdetect.start(url, ua)
        return comsver

