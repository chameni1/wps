import cmsdb.basic as basic

def start(url,ua):
    reg_url = url + '/wp-login.php?action=register'
    basic.info('Checking user registration status')
    reg_source = basic.getsource(reg_url, ua)
    reg_status = '0'
    if reg_source[0] == '1' and '<form' in reg_source[1]:
        if 'Registration confirmation will be emailed to you' in reg_source[1] or 'value="Register"' in reg_source[1] or 'id="user_email"' in reg_source[1]:
            basic.success('User registration open: ' + basic.bold + basic.fgreen + reg_url + basic.cln)
            reg_status = '1'
    return [reg_status, reg_url]
