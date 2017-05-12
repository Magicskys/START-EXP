#coding:utf-8
from os import walk
import sqlite3
from imp import load_module,find_module

class PluginManager(object):

    def __init__(self):
        self.plugins={}
        self.conn=sqlite3.connect("database/data.db")
        self.conn.text_factory = str
        self.cu=self.conn.cursor()
        self.current_plugin = ""

    def version(self):
        self.cu.execute("select * from version")
        return self.cu.fetchone()[0]

    def exit(self):
        self.conn.close()
    def db_init(self):
        self.cu.execute("DROP TABLE plugins;")
        self.cu.execute("DROP TABLE vulns;")
        self.cu.execute("CREATE TABLE plugins (name, author, soft, scope, description);")
        self.cu.execute("CREATE TABLE vulns (title,vuln);")
    def db_rebuild(self):
        self.cu.execute("delete from plugins")
        self.conn.commit()
        for dirpath,dirnames,filenames in walk("plugins/"):
            if dirpath=="plugins/":
                continue
            db={
                'soft':dirpath.split("/")[1]+"_"+dirpath.split("/")[-1],
                "plugins":[]
            }
            for fn in filenames:
                if fn.endswith("py"):
                    db["plugins"].append(fn.split(".")[0])
            for plugin in db["plugins"]:
                p=load_module(plugin,*find_module(plugin,[dirpath]))
                name=db['soft']+"_"+plugin
                author=p.author
                scope=p.scope
                description=p.description
                self.cu.execute("insert into plugins values(?,?,?,?,?)",
                                (name,author,db["soft"],scope,description))
                self.conn.commit()

    def search_plugin(self,keyword):
        keyword="%"+keyword+"%"
        self.cu.execute("select name,scope,description from plugins where name link ? or description link ?",(keyword,keyword))

    def plugin_info(self,plugin):
        self.cu.execute("select name,author,soft,scope,description from plugins where name=?",(plugin,))
        return self.cu.fetchone()

    def plugins_num(self):
        self.cu.execute("select count(*) from plugins")
        return self.cu.fetchone()[0]

    def list_plugins(self):
        self.cu.execute("select name,scope,description from plugins")
        return self.cu.fetchall()

    def plugin_load(self,plugin):
        if plugin not in self.plugins:
            self.plugins[plugin] = {}
            plugin_name = plugin[plugin.rindex("_")+1:]
            plugin_dir = "plugins/" + plugin[:plugin.rindex("_")].replace("_","/")
            module = load_module(plugin_dir+plugin_name,
                                 *find_module(plugin_name, [plugin_dir]))
            self.plugins[plugin]["options"] = module.options
            self.plugins[plugin]["exploit"] = module.exploit
        self.current_plugin = plugin

    def options(self):
        return self.plugins[self.current_plugin]["options"]

    def options_show(self,option,value):
        for op in self.plugins[self.current_plugin]['options']:
            if op["Name"]==option:
                op["Current_Setting"]=value
                return "%s => %s"%(op["Name"],value)
            else:
                return "无效的配置: %s"%option

    def plugin_exec(self):
        options={}
        for option in self.plugins[self.current_plugin]["options"]:
            name=option["Name"]
            current_setting=option["Current_Setting"]
            required=option['Required']
            if required and not current_setting:
                return "%s is required!"%name
            else:
                if name=="URL":
                    if current_setting.endswith("/"):
                        options["URL"]=current_setting[:-1]
                    else:
                        options['URL']=current_setting
                elif name=="Cokkie":
                    options["Cookie"] = dict(
                        i.split("=", 1)
                        for i in current_setting.split("; ")
                    )
                elif name=="Thread":
                    options["Thread"]=int(current_setting)
                else:
                    options[name]=current_setting
        try:
            vuln=self.plugins[self.current_plugin]["exploit"](**options)
            if vuln:
                self.cu.execute("insert into vulns values (?, ?)",(self.current_plugin, vuln))
                self.conn.commit()
                return True,vuln
            else:
                return False,"利用失败"
        except sqlite3.ProgrammingError:
            return True, vuln
        except Exception, e:
            return False, "%s: %s" % (self.current_plugin, e.message)

    def show_vulns(self):
        self.cu.execute("select title, vuln from vulns")
        return self.cu.fetchall()

    def clear_vulns(self):
        self.cu.execute("delete from vulns")
        self.conn.commit()

    def crwal(self):
        pass