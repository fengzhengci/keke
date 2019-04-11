#!/bin/bash
#
username=$1
password=$2
email=$3

[[ -n $email ]] || email=' '
if [[ -z $username && -z $password ]] ; then 
    echo '初始化失败'
    exit 1
fi

#初始化数据库
/usr/bin/python3 manage.py migrate
#初始化管理员

/usr/bin/python3 manage.py createsuperuser  --username $username  << EOF
$email
$password
$password
EOF
