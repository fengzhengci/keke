# !/usr/bin/env python3
# coding:utf-8
# author:feng
import sqlite3, threading, os, psutil
from vrvtools import vrvservices
from subprocess import getstatusoutput as getcmd
import json, time


class Sql(object):
    def __init__(self):
        self.db_name = "to_django.db"
        self.db_conn = sqlite3.connect(self.db_name)
        self.db_curs = self.db_conn.cursor()

    def create(self):
        table_sql = "create table if not exists vrvservices(" \
                    "name VARCHAR, " \
                    "port VARCHAR (50), " \
                    "status VARCHAR (50), " \
                    "pid VARCHAR (50), " \
                    "logdir VARCHAR (200), " \
                    "logindex VARCHAR (50)," \
                    "logs VARCHAR (50), " \
                    "comment VARCHAR (200))"
        self.db_curs.execute(table_sql)
        system_info = "create table if not exists system_info(" \
                      "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                      "root_used VARCHAR (50)," \
                      "root_free VARCHAR (50)," \
                      "data_used VARCHAR (50)," \
                      "data_free VARCHAR (50)," \
                      "cpu_used VARCHAR (50)," \
                      "memory_used VARCHAR (50)," \
                      "netin VARCHAR (50)," \
                      "netout VARCHAR (50)," \
                      "insert_time TIMESTAMP DEFAULT (datetime('now', 'localtime')))"
        self.db_curs.execute(system_info)
        self.db_conn.commit()

    def execure_sql(self, sql):
        self.db_curs.execute(sql)
        self.db_conn.commit()
        return self.db_curs

    def __del__(self):
        self.db_conn.close()


class Check_services(object):
    def update_data(self):
        """
        update services data
        :return:
        """
        self.check()
        for data in services:
            data['logs'] = str(data.get('logs'))
            count = \
                (sqlite.execure_sql("select count(*) from vrvservices WHERE name='%s'" % data.get('name'))).fetchall()[
                    0][0]

            if count > 0:
                sql = "update vrvservices set name='%s'," \
                      "port='%s',status='%s',pid='%s'," \
                      "logdir='%s',logindex='%s',logs='%s'," \
                      "comment='%s' WHERE name='{0}'".format(data.get('name')) % tuple(data.values())
            else:
                sql = "insert into vrvservices({0}) VALUES {1}".format(','.join(data.keys()), tuple(data.values()))

            sqlite.execure_sql(sql)

    # 通过pidof命令判断进程是否纯在
    def ckpid(self, s):
        result, output = getcmd('/sbin/pidof %s' % s.get('name'))
        if result:
            s['status'] = "FAILED"
        else:
            s['status'] = "SUCCESS"

    # 通过端口判断进程是否存在
    def ckport(self, s):
        result, output = getcmd("/usr/sbin/ss -tnl | /bin/awk '$4~/.*:%s/{print $4}'" % s.get('port'))
        if output:
            s['status'] = "SUCCESS"
        else:
            s['status'] = "FAILED"

    # 检查服务状态
    def check(self):
        th_list = []  # 存储所有服务查询进程
        for s in services:
            if s.get('name') in (
                    'mysqld', 'turnserver', 'nginx', 'prelogin', 'upload', 'cloud', 'ddio', 'apnsagent', 'sharecomment',
                    'miniweb',
                    'oauth', 'minidood', 'organization', 'favorite', 'mail'):
                th = threading.Thread(target=self.ckpid, args=(s,))  # 启动线程
                th.start()
                th_list.append(th)
            elif s.get('name') in ('mediadood',):
                th = threading.Thread(target=self.ckport, args=(s,))
                th.start()
                th_list.append(th)
            else:
                pass

        for t in th_list:
            t.join()
        return services

    # 服务运行状态接口
    def api_vrvstatus(self):
        fetchall = (sqlite.execure_sql("select count(*) from vrvservices WHERE status='FAILED'")).fetchall()[0][0]
        return 'SUCCESS' if fetchall == '0' else 'FAILED'

    # 获取正常服务列表
    def api_normal(self):
        normal_list = []
        fetchall = sqlite.execure_sql("select * from vrvservices WHERE status='SUCCESS'")
        for i in fetchall.fetchall():
            normal_json = {}
            normal_json['name'] = i[0]
            normal_json['port'] = i[1]
            normal_json['status'] = i[2]
            normal_json['pid'] = i[3]
            normal_json['logdir'] = i[4]
            normal_json['logindex'] = i[5]
            normal_json['logs'] = i[6]
            normal_json['comment'] = i[7]
            normal_list.append(normal_json)
        return normal_list

    # 获取异常服务列表
    def api_abnormal(self):
        abnormal_list = []
        fetchall = sqlite.execure_sql("select * from vrvservices WHERE status='FAILED'")
        for i in fetchall.fetchall():
            abnormal_json = {}
            abnormal_json['name'] = i[0]
            abnormal_json['port'] = i[1]
            abnormal_json['status'] = i[2]
            abnormal_json['pid'] = i[3]
            abnormal_json['logdir'] = i[4]
            abnormal_json['logindex'] = i[5]
            abnormal_json['logs'] = i[6]
            abnormal_json['comment'] = i[7]
            abnormal_list.append(abnormal_json)
        return abnormal_list

    def run(self):
        while 1:
            self.update_data()
            time.sleep(5)


class Check_os(object):
    def get_os_info(self):
        info = {}
        get_cmd = lambda cmd: '0' if (os.popen(cmd).readline().strip()) == "" else (os.popen(cmd).readline().strip())
        info['root_used'] = get_cmd('df -Ph|grep \"/$\"|awk \'{print $3}\'')
        info['root_free'] = get_cmd('df -Ph|grep \"/$\"|awk \'{print $4}\'')
        info['data_used'] = get_cmd('df -Ph|grep \"/data$\"|awk \'{print $4}\'')
        info['data_free'] = get_cmd('df -Ph|grep \"/data$\"|awk \'{print $3}\'')
        info['cpu_used'] = psutil.cpu_percent()
        info['memory_used'] = psutil.virtual_memory().percent
        info['netin'] = psutil.net_io_counters().bytes_recv
        info['netout'] = psutil.net_io_counters().bytes_sent
        return info

    def insert_data(self):
        # 删除大于10分钟的数据
        sqlite.execure_sql("delete from system_info "
                           "WHERE (julianday(datetime('now', 'localtime')) - julianday(insert_time))*24*60 > 10")
        sys_info = self.get_os_info()
        sql = "insert into system_info({0}) VALUES {1}".format(','.join(sys_info.keys()), tuple(sys_info.values()))
        sqlite.execure_sql(sql)

    def run(self):
        while 1:
            self.insert_data()
            time.sleep(5)


class Backups(object):
    def back_up(self):
        info = {
            'execute_time': '2019-04-09 02:00:00',
            'path'        : '/data/linkdood/im/conf/',
            'save_time'   : '2019-04-09 09:00:00'
        }

        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        file_name = 'back' + date
        with open('back.conf', 'w+') as f:
            f.write(json.dumps(info, indent=4))


if __name__ == '__main__':
    sqlite = Sql()
    sqlite.create()

    services = vrvservices.services['base']

    # check_vrv = Check_services()
    # check_os = Check_os()
    # th1 = threading.Thread(target=check_vrv.run)
    # th2 = threading.Thread(target=check_os.run)
    # th1.start()
    # th2.start()
    # th1.join()
    # th2.join()
    backups = Backups()
    backups.back_up()
