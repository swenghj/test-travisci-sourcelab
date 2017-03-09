#!/usr/bin/env python2.7

#--------------------------------------------------------------------
# 
# Title: ap-demo-regression.py - wrapper file for running all scripts
#
#--------------------------------------------------------------------

from subprocess import call

# list of the running scripts
scripts = [
    "ap-demo-automation-1.py"
    #ap-demo-automation-2.py
]

#scripts = []

if __name__ == '__main__':
    try:
        testfile = None
        for script in scripts:
            testfile = script
            call("python %s  -i travisci -d sauce" % script, shell=True)
       
    except Exception as e:
        print e
        raise Exception("Cannot run %s: " % testfile, e)

