#!/usr/bin/env python2.7

#--------------------------------------------------------------------
# 
# Title: ap-demo-automation-1.py
#
#--------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime, timedelta
from optparse import OptionParser
import time, unittest, os, json
from autotools import demo_api as api
from autotools import HTMLTestRunner
# saucelabs 
from sauceclient import SauceClient

with open("data/login.json") as data_file:
    server = json.load(data_file)

with open("data/input.json") as data_file:
    data = json.load(data_file)

# globals
testname = "ap-demo-automation-1"
chromedriver = "../chromedriver"
current_date = datetime.now()
profile = None

# saucelabs
USE_SAUCE = False
Sauce_Client = None
saucelab_environment_details = {
        'platform': "OS X 10.11",
        'browserName': "firefox",
        'version': "44.0",
        'name': testname
}

# option in command line
parser = OptionParser()
parser.add_option("-u", "--url", action="store", dest="urlname")
parser.add_option("-i", "--integration", action="store", dest="ciname")
parser.add_option("-d", "--driver", action="store", dest="drivername")
(options, args) = parser.parse_args()
# parsing the URL option
if options.urlname:
    urladdress = options.urlname

    # if another URL used, then set the Firefox preference
    profile = webdriver.FirefoxProfile()
    profile.set_preference("xpinstall.signatures.required", False)
else: urladdress = server["domain"]

# travisci-saucelab tunnel
if options.ciname == "travisci": 
    saucelab_environment_details['tunnel-identifier'] = os.environ.get('TRAVIS_JOB_NUMBER')
    saucelab_environment_details['build'] = os.environ.get('TRAVIS_BUILD_NUMBER')
    saucelab_environment_details['tags'] = [os.environ.get('TRAVIS_PYTHON_VERSION'), 'CI']

# parsing the web browser testing option and checking system os
if options.drivername == "chrome": WebDriver = webdriver.Chrome(chromedriver)
elif options.drivername == "sauce":
    # saucelabs
    # travisci environment variables
    USE_SAUCE = True
    username = os.environ.get('SAUCE_USERNAME')
    access_key = os.environ.get('SAUCE_ACCESS_KEY')
    Sauce_Client = SauceClient(username, access_key)
    saucelab_environment_details['username'] = username
    saucelab_environment_details['key'] = access_key

    WebDriver = webdriver.Remote(
        command_executor='http://%s:%s@ondemand.saucelabs.com:80/wd/hub' % (username, access_key),
        desired_capabilities=saucelab_environment_details
    )
else: WebDriver = webdriver.Firefox(firefox_profile=profile)
#else: WebDriver = webdriver.Firefox()

class TravisciHerokuWebAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global WebDriver        
        cls.driver = WebDriver
        global Sauce_Client
        cls.sauce_client = Sauce_Client

    def setUp(self):
        print "setUp"

    def test_001_login(self):
        try:
            self.driver.get(urladdress)
            self.driver.maximize_window()
            
            #login to AP account
            api.send_text_by_tag_name(self.driver, "username", server["ap-username"])
            api.send_text_by_tag_name(self.driver, "password", server["ap-password"], True)

            #reference#
            # elem = self.driver.find_element_by_id('summary')
            # res = 'FalseSentence!' in elem.get_attribute('innerHTML')

            # # saucelabs - update saucelab result first
            # if USE_SAUCE:
            #     print "annotating true/false in saucelabs dashboard"                
            #     self.sauce_client.jobs.update_job(self.driver.session_id, passed=res) 

            # # this is for the local report
            # self.assertTrue(res, "Text(It worked!) not in the headings")

            time.sleep(5)
        except Exception as e:
            print e
            raise Exception("Cannot open URL: ", e)

    def test_002_attempt_click_webaccessrequest(self):
        try:
            xpath = "//*[@class='list-group-item' and contains(text(), 'Web Access Requests')]"
            api.click_element_by_xpath(self.driver, xpath)

            #reference#
            # # saucelabs - update saucelab result first
            # if USE_SAUCE:
            #     print "annotating true/false in saucelabs dashboard"                
            #     self.sauce_client.jobs.update_job(self.driver.session_id, passed=res) 

            # # this is for the local report
            # self.assertTrue(res, "Text(Of course,) not in the instructions")

            time.sleep(5)
        except Exception as e:
            print e
            raise Exception("Cannot open URL: ", e)

    def tearDown(self):
        print "tearDown"

    @classmethod
    def tearDownClass(cls):
        print "test done"
        cls.driver.close()
        cls.driver.quit()


if __name__ == '__main__':
    # output to a file
    if not os.path.exists('reports'): os.mkdir('reports')
    suite = unittest.TestLoader().loadTestsFromTestCase(TravisciHerokuWebAutomation)

    test_report = 'reports/' + testname + '.html'
    fp = file(test_report, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title=testname,
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # run the test
    runner.run(suite)

    # output result on console for debugging
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    # close output file
    fp.close()
