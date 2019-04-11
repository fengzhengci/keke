#_*_coding:utf-8_*_
__author__ = 'keke'

import os,sys,time,re,json,subprocess,random,datetime
import psutil
import logging
import subprocess
from  keke.settings import *



def set_log(level, filename=LOG_FILE):
    log_file = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(log_file):
        os.mknod(log_file)
    log_level_total = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARN, 'error': logging.ERROR,
                       'critical': logging.CRITICAL}

    logger_f = logging.getLogger()
    logger_f.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_file)
    fh.setLevel(log_level_total.get(level, logging.DEBUG))
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger_f.addHandler(fh)
    return logger_f

# 日志记录器
logger = set_log(LOG_LEVEL)



