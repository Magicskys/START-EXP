#coding:utf-8
from termcolor import colored

def error(string):
    print colored("[!]"+string,"red")

def success(string):
    print colored("[+]"+string, "green")


def process(string):
    print colored("[*]"+string, "blue")