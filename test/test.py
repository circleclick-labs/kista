#!/usr/bin/env python3
import os, sys, json, time, datetime as dt, kista

kista.w3_connect(None, 1.1)
#kista.set_gasfactor(1.1)
#kista.set_public( os.getenv('PUBLIC'))
#kista.set_private(os.getenv('PRIVATE'))

from kista import *

print("run tests", public, private)

a = deploy_contractAddress("Test1", "hello")
print(a)

c =  load_wrapped_contract("Test1")
print(c.s())

print(c.msgSender())

c.setMsgSender()

print(c.msgSender())

print(c.getMsgSender())

