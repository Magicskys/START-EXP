#!/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.console import Interface


def main():
    logo = """
    _______________________
    < START Exploit Framework >
    -----------------------
    
        ..||||||||∞ |||||
        ╭||||━━　　━━ ||||╮
        ╰|||　　 ~　　　|||╯
        　||╰╭--╮ˋ╭--╮╯||
        　||　╰/ /　 || ОО
        
        节操粉碎中 请稍后
         ━━━━━━━━━━━
         ▉▉▉▉▉▉▉▉ 99.9%
         ━━━━━━━━━━━

+ -- --=[ START Exploit Framework ]
    """
    interface = Interface()
    print logo
    while True:
        try:
            interface.cmdloop()
        except KeyboardInterrupt:
            print "Interrupt: use the 'exit' command to quit"

if __name__ == "__main__":
    main()