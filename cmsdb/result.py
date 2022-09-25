

import cmsdb.basic as basic

def target(target):
    ## initiate the result
    target = target.replace('https://','').replace('http://', '').split('/')
    target = target[0]
    print(' ┏━Target: ' + basic.bold + basic.red + target + basic.cln)

def end(requests, time, log_file):
    ## end the result
    print(' ┃\n ┠── Result: ' + basic.bold + basic.fgreen + log_file + basic.cln)
    print(' ┃\n ┗━Scan Completed in ' + basic.bold +basic.lblue + time + basic.cln +' Seconds, using ' + basic.bold + basic.lblue + requests + basic.cln +' Requests')

def cms(cms,version,url):
    ## CMS section
    print(' ┃\n ┠── CMS: ' + basic.bold + basic.fgreen + cms + basic.cln +'\n ┃    │')
    if version != '0' and version != None:
        print(' ┃    ├── Version: '+ basic.bold + basic.fgreen + version + basic.cln)
    print(' ┃    ╰── URL: ' + basic.fgreen + url + basic.cln)

def menu(content):
    # Use it as a header to start off any new list of item
    print(' ┃\n ┠──' + content)

def init_item(content):
    # The first item of the menu
    print(' ┃    │\n ┃    ├── ' + content)

def item(content):
    # a normal item just not the first or the last one
    print(' ┃    ├── ' + content)

def empty_item():
    print(' ┃    │')

def end_item(content):
    # The ending item
    print(' ┃    ╰── ' + content)

def init_sub(content, slave=True):
    # initiating a list of menu under a item
    print(' ┃    │    │\n ┃    │    ├── ' + content if slave else ' ┃         │\n ┃         ├── ' + content)

def sub_item(content, slave=True):
    # a sub item
    print(' ┃    │    ├── ' + content if slave else ' ┃         ├── ' + content)

def end_sub(content, slave=True):
    # ending a sub item
    print(' ┃    │    ╰── ' + content if slave else ' ┃         ╰── ' + content)

def empty_sub(slave=True):
    print(' ┃    │    │' if slave else ' ┃         │')


def init_subsub(content, slave2=True, slave1=True):
    # Sub item of a sub item.. this is getting too much at this point
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   │' if slave1 else '    │'
    part3 = '\n ┃    │    ' if slave2 else '\n ┃         '
    part4 = '│   ├── ' if slave1 else '    ├── '
    content = part1 + part2 + part3 + part4 + content
    print(content)

def subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ├── ' if slave1 else '    ├── '
    content = part1 + part2 + content
    print(content)

def end_subsub(content, slave2=True, slave1=True):
    part1 = ' ┃    │    ' if slave2 else ' ┃         '
    part2 = '│   ╰── ' if slave1 else '    ╰── '
    content = part1 + part2 + content
    print(content)
