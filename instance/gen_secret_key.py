#coding:utf-8
import os
with open("secret_key",'w') as f:
    s = os.urandom(24)
    f.write(s)