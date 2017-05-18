#coding:utf-8
import cmd
import os
import subprocess
from lib import logger
from lib.plugin_manager import PluginManager

class Interface(cmd.Cmd,PluginManager):
    def __init__(self):
        cmd.Cmd.__init__(self)
        PluginManager.__init__(self)
        self.prompt="START Exploit Framework > "

    def do_help(self, arg):
        commands={
            'help':"帮助菜单",
            'use':'使用插件',
            'version':'显示版本信息',
            'init_db':"初始化数据库",
            'rebuild_db':'重建数据库',
            'shell':"运行外部命令",
            'back':"返回到菜单",
            'info':"显示插件信息",
            'values':'漏洞',
            'exploit':'执行',
            'crawl':'批量自动化',
            'exit':'退出'
        }

        print "\n帮助\n=============\n"
        print "%-30s%s"%("命令","描述")
        print "%-30s%s"%("----","---")
        for command in commands:
            print "%-30s%s"%(command,commands[command])
        print

    def do_version(self,line):
        print "Version:% s\n"%self.version()

    def do_list(self,line):
        print "\nEXP列表\n=============\n"
        print "%-40s%-40s%s" % ("名字", "范围", "描述")
        print "%-40s%-40s%s" % ("----", "-------", "-----------")
        for name, scope, description in self.list_plugins():
            print "%-40s%-40s%s" % (name, scope, description)
            print
        print "共有EXP %s个"%self.plugins_num()

    def do_search(self,keyword):
        if keyword:
            print "\n查询EXP\n=============\n"
            print "%-40s%-40s%s" % ("名字", "范围", "描述")
            print "%-40s%-40s%s" % ("----", "-------", "-----------")
            for name, scope, description in self.search_plugin(keyword):
                print "%-40s%-40s%s" % (name, scope, description)
                print
        else:
            logger.error("search <keyword>")

    def do_back(self,line):
        self.current_plugin=""
        self.prompt="START Tools Framewark > "

    def do_shell(self,arg):
        logger.process("exec: %s"%arg)
        sub_cmd=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        print
        print sub_cmd.communicate()[0]

    def do_info(self,plugin):
        if not plugin:
            if self.current_plugin:
                plugin=self.current_plugin
            else:
                logger.error("info <plugin>")
                return
        if self.plugin_info(plugin):
            name, author, soft, scope, description =  self.plugin_info(plugin)
            print "\n%15s: %s" % ("名字", name)
            print "%15s: %s" % ("软件", soft)
            print "%15s: %s\n" % ("范围", scope)
            print "来源:\n\t%s\n" % author
            print "描述:\n\t%s\n" % description
        else:
            logger.error("Invalid plugin:%s"%plugin)
    def complete_info(self,text,line,begidx,endidx):
        plugins=[i[0] for i in self.list_plugins()]
        if not text:
            completions=plugins
        else:
            completions=[p for p in plugins if p.startswith(text)]
        return completions

    def do_use(self,plugin):
        if plugin:
            try:
                self.plugin_load(plugin)
            except Exception,e:
                print e
                logger.error("Failed to laod plugin:%s"%plugin)
            if self.current_plugin:
                self.prompt=" %s >"%self.current_plugin
        else:
            logger.error("use <plugin>")

    def complete_use(self,text,line,begidx,endidx):
        plugins=[i[0] for i in self.list_plugins()]
        if not text:
            completions=plugins
        else:
            completions=[p for p in plugins if p.startswith(text)]
        return completions

    def do_options(self,line):
        if self.current_plugin:
            rn=self.options_show()
            if isinstance(rn,str):
                logger.error(rn)
            else:
                print "\n%-20s%-28s%-10s%s" % ("名字", "目前配置",
                                                 "必须", "描述")
                print "%-20s%-20s%-10s%s" % ("----", "---------------",
                                               "--------", "-----------")
                for option in rn:
                    print "%-20s%-20s%-10s%s" % (option["Name"],
                                                   option["Current Setting"],
                                                   option["Required"],
                                                   option["Description"])
                print
        else:
            logger.error("获取一个插件")

    def do_set(self, arg):
        if self.current_plugin:
            if len(arg.split()) == 2:
                option = arg.split()[0]
                value = arg.split()[1]
                rn = self.option_set(option.upper(), value)
                if rn.startswith("错误选项:"):
                    logger.error(rn)
                else:
                    print rn
            else:
                logger.error("set <option> <value>")
        else:
            logger.error("获取一个插件")


    def do_init_db(self,line):
        logger.process("初始化数据库")
        self.db_init()
        logger.success("OK")
    def do_rebuild_db(self,line):
        logger.process("清空数据库")
        logger.process("重建数据库")
        self.db_rebuild()
        logger.success("OK")
    def do_values(self,arg):
        arg=arg.split()
        if not arg:
            vulns = self.show_vulns()
            print "\nVulns\n=====\n"
            print "%-42s%s" % ("标题", "漏洞")
            print "%-40s%s" % ("------", "----")
            for plugin, vuln in vulns:
                print "%-40s%s" % (plugin, vuln)
            print
        elif arg[0] == "-d":
            self.clear_vulns()
            logger.success("Clear database successfully.")
    def do_exploit(self,line):
        if self.current_plugin:
            rn=self.plugin_exec()
            if not rn[0]:
                logger.error(rn[1])
        else:
            logger.error("获取一个插件")

    def default(self,line):
        logger.error("找不到命令: %s"%line)

    def do_exit(self,line):
        self.exit()
        exit()

    def do_quit(self, line):
        self.exit()
        exit()

    def emptyline(self):
        pass

    def do_crawl(self,arg):
        if self.current_plugin:
            if len(arg.split()) == 2:
                url = arg.split()[0]
                page = arg.split()[1]
                rn = self.crawl(url, page)
                if rn.startswith("错误选项:"):
                    logger.error(rn)
                else:
                    print rn
            else:
                logger.error("crawl <url> <page>")
        else:
            logger.error("获取一个插件")
