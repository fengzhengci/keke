#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:FengZhengCi, ZhangLiQing

import os, sys, json
import logging
import socket
import time
import datetime
from subprocess import getstatusoutput as getcmd

local_json = '/data/linkdood/im/conf/local_version.json'
server_json = '/data/update/server_version.json'


def set_log(level, filename='linkdood_update_interface.log', filedir='/tmp'):
    log_file = os.path.join(filedir, filename)
    if not os.path.isdir(filedir):
        os.makedirs(filedir)
    if not os.path.isfile(log_file):
        os.mknod(log_file)

    log_level_status = {'debug'   : logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN,
                        'error'   : logging.ERROR,
                        'critical': logging.CRITICAL}

    logger_f = logging.getLogger()
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_status.get(level, logging.DEBUG))
    formatter = logging.Formatter(
            '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f


logger = set_log('debug')


def cron_ctrl(task, mode):
    'mode:a append d delete'
    with open('/var/spool/cron/root', 'r') as f:
        lines = f.readlines()

    if mode == 'a':
        logger.info('append crontab task %s' % task)

        cmd = task.split("*")[1]
        newlines = [i for i in lines if cmd not in i]
        with open('/var/spool/cron/root', 'w+') as f:
            f.write(''.join(newlines))

        if task in lines:
            return True
        with open('/var/spool/cron/root', 'a+') as f:
            f.write(task)
        return True
    elif mode == 'd':
        logger.info('delete crontab task %s' % task)
        if task not in lines:
            return True
        lines.remove(task)
        with open('/var/spool/cron/root', 'w+') as f:
            f.write(''.join(lines))
        return True
    else:
        return False


def get_newest_tag():
    with open(server_json, 'r') as f:
        data = json.load(f)
        tagdict = {}
        taglist = list(data.keys())
        for tag in taglist:
            tagnum = tag.strip('V').split('.')
            tagdict[tag] = 1000000 * \
                           int(tagnum[0]) + 1000 * int(tagnum[1]) + int(tagnum[2])
        newest_tag = max(tagdict, key=tagdict.get)
        return newest_tag


def excmd(cmd, record=True):
    if record:
        logger.info('execute commands %s' % cmd)
    status, output = getcmd(cmd)
    if record:
        logger.info('execute result %s' % output)
    return (status, output)


def get_json_value(conf, *args):
    result = []
    if not os.path.isfile(conf):
        return False
    with open(conf) as f:
        data = json.load(f)
    for key in args:
        result.append(data.get(key))
    if len(result) == 1:
        return result[0]
    else:
        return result


def change_json_value(conf, value, key1, key2=''):
    if not os.path.isfile(conf):
        return False
    with open(conf) as f:
        data = json.load(f)
        a = data.get(key1)
    if type(a).__name__ == 'dict':
        a[key2] = value
    else:
        data[key1] = value
    with open(conf, 'w+') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)
    return True


def version_to_int(version):
    version = version.split('_')[0].lstrip('Vv').split('.')
    version_int = int(version[0]) * 1000000 \
                  + int(version[1]) * 1000 + int(version[2])
    return version_int


def get_inip():
    ip = excmd("/sbin/ifconfig | awk '/.*inet addr/{print $2}'")[1]
    iplist = [i.strip('addr:') for i in ip.split('\n') if
              i not in ("addr:127.0.0.1", "addr:192.168.42.1", "addr:172.17.42.1")]
    return iplist[0]


def confirm_server_version():
    for file in os.listdir('/data/update'):
        if file == get_newest_tag():
            return True
        else:
            pass


def version_compare():
    if not os.path.isfile(server_json):
        return False

    if confirm_server_version:
        server_version = get_newest_tag()
    else:
        return False

    local_version = get_json_value(local_json, 'version')
    server_version = version_to_int(server_version)
    local_version = version_to_int(local_version)

    if server_version > local_version:

        download_md5 = excmd('md5sum %s' %
                             '/data/update/' + get_newest_tag() + '/linkdood-minic.tar.gz')[1]
        download_md5 = download_md5.split(" ")[0]
        server_md5 = get_json_value(server_json,
                                    get_newest_tag())['server']['md5']

        if download_md5 == server_md5:
            return True
        else:
            print('New version exists but md5 check failed.')
            return False
    else:
        return False


def info_extract():
    version = get_json_value(local_json, 'version')
    bugfix_version = get_json_value(local_json, 'bugfix_version')
    tool_version = get_json_value(local_json, 'tools_version')

    info = {'version'       : version,
            'bugfix_version': bugfix_version,
            'tool_version'  : tool_version}

    return info


def is_valid_date(str):
    try:
        time.strptime(str, "%Y-%m-%d %H:%M:%S")
        return True
    except BaseException:
        return False


def is_valid_time(str):
    try:
        time.strptime(str, "%H:%M:%S")
        return True
    except BaseException:
        return False


def get_innerip(iplist):
    for ip in iplist:
        socketTest = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTest.settimeout(1)
        DXADDR = (str(ip), int(80))
        dxstatus = socketTest.connect_ex(DXADDR)
        if dxstatus == 0:
            downloadServer = ip
            return downloadServer


def download_server_json():
    iplist = get_json_value(local_json, 'cdn')
    download_link = 'http://' + \
        get_innerip(iplist) + '/download/minic/release/server_version.json'
    excmd('wget -O %s -P %s %s' % (server_json, '/data/update', download_link))


def application(update, allow):
    try:
        update = int(update)
    except:
        return False

    if update not in (0, 1):
        logger.error('Illegel request value.')
        return 'Illegel request value.'

    if update == 0:
        if is_valid_time(allow) or is_valid_date(allow):
            change_json_value(local_json, allow)

            if get_json_value(local_json, 'server'):
                logger.info('allow_time renovated, please check.')
                return 'allow_time renovated, please check.'
        else:
            logger.error('Illegel request value.')
            return 'Illegel request value.'
    elif update == 1:
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).split(" ")[0].split('-')
        daytime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())).split(" ")[1].split(':')

        minute = daytime[1].lstrip("0")
        hour = daytime[0].lstrip("0")
        day = date[2].lstrip("0")
        month = date[1].lstrip("0")

        if os.path.isdir('/data/update/%s' % get_newest_tag()):
            isupdate = get_json_value(local_json, 'server')['isupdate']
            if isupdate == '1':
                cron_ctrl('%s %s %s %s * /usr/bin/python /data/update/%s/data/server_upgrade.py stage2\n' %
                          (str(int(minute) + 2), hour, day, month, get_newest_tag()), 'a')
                return 'Updating...Please check after may be 5 minutes. :)'
            else:
                return 'Uncessary to update Server.it\'s newest version right now'
        else:
            cron_ctrl('%s %s %s %s * /usr/bin/python /data/linkdood/im/bin/get_update.py --imm\n' %
                      (str(int(minute) + 2), hour, day, month), 'a')
            return 'Updating...Please check after may be 5 minutes. :)'

    else:
        logger.error('Illegel request body.')
        return 'Illegel request body.'


def get_version():
    dic = info_extract()
    dic['new_version_existence'] = version_compare()
    return json.dumps(dic)


# 定时升级
def time_upgrade(allow):
    if is_valid_time(allow) or is_valid_date(allow):
        change_json_value(local_json, allow)

        if get_json_value(local_json, 'server'):
            logger.info('allow_time renovated, please check.')
            return 'allow_time renovated, please check.'
    else:
        logger.error('Illegel request value.')
        return 'Illegel request value.'


# 立即升级
def now_upgrade():
    if os.path.isdir('/data/update/%s' % get_newest_tag()):
        isupdate = get_json_value(local_json, 'server')['isupdate']
        if isupdate == '1':
            # cron_ctrl('%s %s %s %s * /usr/bin/python /data/update/%s/data/server_upgrade.py stage2\n' %
            #           (str(int(minute) + 2), hour, day, month, get_newest_tag()), 'a')
            excmd("nohup python /data/update/%s/data/server_upgrade.py stage2 &" %(get_newest_tag()))
            return 'Updating...Please check after may be 5 minutes. :)'
        else:
            return 'Uncessary to update Server.it\'s newest version right now'
    else:
        #cron_ctrl('%s %s %s %s * /usr/bin/python /data/linkdood/im/bin/get_update.py --imm\n')
        excmd("nohup python /data/linkdood/im/bin/get_update.py --imm &")
        return 'Updating...Please check after may be 5 minutes. :)'



if __name__ == '__main__':
    excmd('md5sum test.txt')
