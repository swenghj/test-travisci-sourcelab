# 
# this is testing purpose for webdriver
#
# Ref: 
# http://selenium-python.readthedocs.io/getting-started.html
# 

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from optparse import OptionParser

# option in command line
chromedriver = "../chromedriver"
parser = OptionParser()
parser.add_option("-d", "--driver", action="store", dest="drivername")
(options, args) = parser.parse_args()
if options.drivername == "chrome": WebDriver = webdriver.Chrome(chromedriver)
else: WebDriver = webdriver.Firefox()

WebDriver.get("http://www.python.org")

assert "Python" in WebDriver.title
elem = WebDriver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in WebDriver.page_source
WebDriver.close()
WebDriver.quit()