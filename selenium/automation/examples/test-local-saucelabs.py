#!/usr/bin/env python
# this is selenium test using sauce lab environments

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

# travisci environment variables
username = os.environ.get('SAUCE_USERNAME')
access_key = os.environ.get('SAUCE_ACCESS_KEY')

test_environment_details = {
	'platform': "OS X 10.11",
	'browserName': "firefox",
	'version': "44.0",
	'name': "Test: Go to python website"
}

# setup webdriver characteristics 
# (e.g) driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX)
browser = webdriver.Remote(
	command_executor='http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (username, access_key),
	desired_capabilities=test_environment_details
	)

#! saucelabs -u username -k access_key - execute this command to turn on tunnel
browser.get("http://localhost:8000")
time.sleep(5)
browser.close()
browser.quit()