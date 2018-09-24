#!/usr/bin/env python2.7

#-----------------------------------------------------------------------------
# 
# Title: demo-api.py
#
# Purpose: collects of the commonly used functions for testing Django server
#
#-----------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def click_element_by_text(driver, text, pose=2):
	elem = driver.find_element_by_xpath('//*[contains(text(), "'+ text + '")]')
	elem.click()
	time.sleep(pose)

def click_element_by_xpath(driver, xpath, pose=2):
	elem = driver.find_element_by_xpath(xpath)
	elem.click()
	time.sleep(pose)

def click_element_by_tag_value(driver, value, pose=2):
	elem = driver.find_element_by_xpath('//*[@value="' + value + '"]')
	elem.click()
	time.sleep(pose)

def click_element_by_id(driver, id, pose=2):
	elem = driver.find_element_by_id(id)
	elem.click()
	time.sleep(pose)

def click_element_by_clsname(driver, clsname, pose=2):
	elem = driver.find_element_by_class_name(clsname)
	elem.click()
	time.sleep(pose)

def send_text_by_tag_name(driver, tag_name, value, enter=False):
	elem = driver.find_element_by_name(tag_name)
	elem.clear()
	elem.send_keys(value)
	time.sleep(1)
	if enter:
		elem.send_keys(Keys.RETURN)
		time.sleep(3)

def get_element_attribute_by_xpath(driver, xpath, attr, pose=0):
	elem = driver.find_element_by_xpath(xpath)
	res = elem.get_attribute(attr)
	time.sleep(pose)
	return res	

def get_element_attribute_by_clsname(driver, classname, attr, pose=0):
	command = 'return document.getElementsByClassName("' + classname + '")[0]'
	#command += '.attributes.getNamedItem("class").' + attr #if JavaScript needs to be modified, use this format
	elem = driver.execute_script(command)
	res =  elem.get_attribute(attr)
	time.sleep(pose)
	return res	

def get_element_text_by_id(driver, id, pose=0):
	elem = driver.find_element_by_id(id)
	res = elem.get_attribute('textContent')
	if res == "undefined" or res == "None": res = elem.get_attribute('innerHTML')
	time.sleep(pose)
	return res	

def get_element_text_by_clsname(driver, classname, pose=0):
	command = 'return document.getElementsByClassName("' + classname + '")[0]'
	elem = driver.execute_script(command)
	res = elem.get_attribute('textContent')
	if res == "undefined" or res == "None": res = elem.get_attribute('innerHTML')
	time.sleep(pose)
	return res

def is_element_visible(driver, item, by='id'):
	try:
		if "//" in item or by == "xpath": elem = driver.find_element_by_xpath(item)
		elif by == "name": elem = driver.find_element_by_name(item)
		elif by == "clsname": elem = driver.find_element_by_class_name(item)
		else: elem = driver.find_element_by_id(item)
		return elem.is_displayed()
	except Exception as e:
		#print e
		return False


