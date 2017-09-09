# -*- coding: utf-8 -*- 

from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.keys import Keys 

from datetime import *
from datetime import datetime
import time 
import datetime
import os 
import urllib, urllib2
import codecs
import sys

#第一行：公司代號
#第二行：公司簡稱
#第三行：主旨
#第四行：發言人
#第五行：發言人職稱
#第六行：說明


if(True):
	browser = webdriver.Chrome('chromedriver') 
	browser.implicitly_wait(10)
	#nb = webdriver.Chrome('chromedriver')

	#switch windows handle
	browser.window_handles

	browser.get('http://mops.twse.com.tw/mops/web/t05sr01_1') 
	# 0 1 4
	#title = browser.find_elements_by_xpath('//table[@class="hasBorder"]/tbody/tr/td')

	#content = browser.find_elements_by_xpath('//input[@value="詳細資料"]')

	count = len(browser.find_elements_by_xpath('//input[@value="詳細資料"]'))

	if not os.path.exists("mops"):
			os.makedirs("mops")
	for i in range(count):

		item = browser.find_elements_by_xpath('//table[@class="hasBorder"]/tbody/tr/td')
		#print item[i*6+1].text
		nnum = item[i*6].text
		nname = item[i*6+1].text
		ndate = str(int(item[i*6+2].text.replace("/",""))+19110000)
		ntime = item[i*6+3].text.replace(":","")
		nsub = item[i*6+4].text
		#browser.find_elements_by_xpath('//table/tbody/tr').text
		folder = os.path.join("mops", ndate[0:4])
        #                if os.path.isfile(fn):

		if not os.path.exists("mops"):
			os.makedirs("mops")
		if not os.path.exists(folder):
			os.makedirs(folder)
		folder = os.path.join(folder, ndate[4:6])
		if not os.path.exists(folder):
			os.makedirs(folder)

		fn = os.path.join(os.path.dirname(__file__), folder, ndate+"_"+ntime+"_"+nnum+".txt")
		if os.path.isfile(fn):
			continue
		#f = codecs.open(fn, "w+", "utf-8")

		content = nnum+"\n"+nname+"\n"+nsub+"\n"


		browser.find_elements_by_xpath('//input[@value="詳細資料"]')[i].click()
		#title[i].text
		#content[i].click()
		time.sleep(1.5)

		inside = browser.find_elements_by_xpath('//td[@style="text-align:left !important;"]')

		content += inside[2].text+"\n"+inside[3].text +"\n"
		#print browser.find_element_by_xpath('//pre[@style="font-family:細明體; !important;"]').text+"\n"
		content += browser.find_element_by_xpath('//pre[@style="font-family:細明體; !important;"]').text+"\n"

		#print browser.find_element_by_xpath('//pre/font[@size="2"]')
		
		browser.find_element_by_xpath('//a[@onclick="ajax_back();"]').click()

		f = codecs.open(fn, "w+", "utf-8")
		f.write(content)
		f.close()
		time.sleep(1.5)
	


	browser.quit()








