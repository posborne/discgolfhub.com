from fabric.api import *
import os
from collections import deque

def _cmdjoin(*cmds):
    return ' '.join(cmds)

#===============================================================================
# A simple password encryption algorithm to keep out the innocent
#===============================================================================
def _simple_encrypt(password, passfile):
    d = deque([ord(x) for x in password])
    d.rotate(3)
    chars = list(d)
    for i, char in enumerate(chars):
        chars[i] = char - 5
    open(passfile, 'w').write(''.join([chr(x) for x in chars]))

def _simple_decrypt(passfile):
    d = deque([ord(x) for x in open(passfile).read()])
    d.rotate(-3)
    chars = list(d)
    for i, char in enumerate(chars):
        chars[i] = char + 5
    return ''.join([chr(x) for x in chars])

python = 'python2.5'
appengine_base = os.path.abspath('./google_appengine')
appcfg = os.path.join(appengine_base, 'appcfg.py')
appserver = os.path.join(appengine_base, 'dev_appserver.py')
bulkloader = os.path.join(appengine_base, 'bulkloader.py')

def deploy():
    """Deploy the current state of the applicaiton to google"""
    local(_cmdjoin('echo "%s" | ' % _simple_decrypt('pw.txt'), 
                   python, appcfg, 'update . --email=osbpau@gmail.com'), capture=False)

def writepw():
    pw = prompt('password to encrypt: ')
    _simple_encrypt(pw, 'pw.txt')
    
    

