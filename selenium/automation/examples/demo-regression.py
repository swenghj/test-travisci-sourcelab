#!/usr/bin/env python2.7

#--------------------------------------------------------------------
# 
# Title: demo-regression.py - wrapper file for running all scripts
#
#--------------------------------------------------------------------

from subprocess import call

# list of the running scripts
scripts = [
    "demo-travisci-heroku-1.py",
    "demo-travisci-heroku-2.py"
]

if __name__ == '__main__':
    try:
        testfile = None
        for script in scripts:
            testfile = script
            call("python %s  -i travisci -d sauce" % script, shell=True)
       
    except Exception as e:
        print e
        raise Exception("Cannot run %s: " % testfile, e)

