import cmsdb.basic as basic
import re

def start(url,ua):

    rss_file = url + '/wp-includes/rss.php'
    rss_source = basic.getsource(rss_file, ua)
    if rss_source[0] == '1' and 'on line' in rss_source[1]:
        path = re.findall(r'<b>/(.*?)wp-includes/rss.php</b>', rss_source[1])
        if path != []:
            return path[0]

    tw_theme = url + '/wp-content/themes/twentyfifteen/index.php'
    theme_source = basic.getsource(tw_theme, ua)
    if theme_source[0] == '1' and 'Uncaught Error:' in theme_source[1]:
        path = re.findall(r'<b>(.*?)wp-content/themes/twentyfifteen/index.php</b>', theme_source[1])
        if path != []:
            return path[0]

    tw_theme = url + '/wp-content/themes/twentysixteen/index.php'
    theme_source = basic.getsource(tw_theme, ua)
    if theme_source[0] == '1' and 'Uncaught Error:' in theme_source[1]:
        path = re.findall(r'<b>(.*?)wp-content/themes/twentyfifteen/index.php</b>', theme_source[1])
        if path != []:
            return path[0]

    tw_theme = url + '/wp-content/themes/twentyseventeen/index.php'
    theme_source = basic.getsource(tw_theme, ua)
    if theme_source[0] == '1' and 'Uncaught Error:' in theme_source[1]:
        path = re.findall(r'<b>(.*?)wp-content/themes/twentyfifteen/index.php</b>', theme_source[1])
        if path != []:
            return path[0]

    return ""
