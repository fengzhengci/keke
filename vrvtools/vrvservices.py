#!/usr/bin/env python3
# coding:utf-8
# author:kk

services = {
    "base" : [
        {
            "name"    : "mysqld",
            "port"    : "11306",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/data/mysql/data/",
            "logindex": "*.err",
            "logs"    : [],
            "comment" : "数据库DB服务"
        },
        {
            "name"    : "turnserver",
            "port"    : "10660",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/turnserver/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "打洞服务"
        },
        {
            "name"    : "nginx",
            "port"    : "10669",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/nginx/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "WEB服务"
        },
        {
            "name"    : "prelogin",
            "port"    : "5000",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/prelogin/",
            "logindex": "info.log*",
            "logs"    : [],
            "comment" : "预登录服务"
        },
        {
            "name"    : "upload",
            "port"    : "9089",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/upload/",
            "logindex": "upload.log*",
            "logs"    : [],
            "comment" : "文件服务"
        },
        {
            "name"    : "mediadood",
            "port"    : "10670",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/im/vrv/mediadood/server/log/",
            "logindex": "vrvmeeting.log",
            "logs"    : [],
            "comment" : "mediadood"
        },
        {
            "name"    : "cloud",
            "port"    : "6026",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/cloud/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "cloud"
        },
        {
            "name"    : "ddio",
            "port"    : "6025",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/ddio/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "ddio"
        },
        {
            "name"    : "apnsagent",
            "port"    : "9090",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/apnsagent/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "apnsagent"
        },
        {
            "name"    : "sharecomment",
            "port"    : "6023",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/sharecomment/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "sharecomment"
        },
        {
            "name"    : "miniweb",
            "port"    : "9001",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/im/minic/miniweb/src/miniweb/log/",
            "logindex": "miniweb.log",
            "logs"    : [],
            "comment" : "miniweb"
        },
        {
            "name"    : "oauth",
            "port"    : "8123",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/oauth/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "oauth"
        },
        {
            "name"    : "minidood",
            "port"    : "10670",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/minidood/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "minidood"
        },
        {
            "name"    : "organization",
            "port"    : "6024",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/organization/",
            "logindex": "*.log",
            "logs"    : [],
            "comment" : "organization"
        },
        {
            "name"    : "favorite",
            "port"    : "",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/favorite/",
            "logindex": "favorite.log",
            "logs"    : [],
            "comment" : "favorite"
        },
        {
            "name"    : "mail",
            "port"    : "11050",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "/data/linkdood/logs/mail/",
            "logindex": "mail.log",
            "logs"    : [],
            "comment" : "mail"
        },
    ],
    "merge": [
        {
            "name"    : "all",
            "port"    : "",
            "status"  : "",
            "pid"     : "",
            "logdir"  : "",
            "logindex": "",
            "logs"    : [],
            "comment" : "全部服务"
        },
    ]
}
