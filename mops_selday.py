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
import re


day = timedelta(1)

if len(sys.argv) != 3:
    print "Input error."
    sys.exit(0)

else:
    if not re.search("\d\d\d\d/\d\d/\d\d", sys.argv[1]):
        print "Input error."
        sys.exit(0)
    elif not re.search("\d\d\d\d/\d\d/\d\d", sys.argv[2]):
        print "Input error."
        sys.exit(0)
    else:
        try:
            sdate = time.strptime(sys.argv[1], "%Y/%m/%d")
            edate = time.strptime(sys.argv[2], "%Y/%m/%d")
        except:
            print "Input error."
            sys.exit(0)
        start = date(sdate[0], sdate[1], sdate[2])
        end = date(edate[0], edate[1], edate[2])
        if end < start:
            print "Input error."
            sys.exit(0)
        now = start

print "Get message from " + start.strftime("%Y-%m-%d") + " to " + end.strftime("%Y-%m-%d")+"."
#第一行：公司代號
#第二行：公司簡稱
#第三行：主旨
#第四行：發言人
#第五行：發言人職稱
#第六行：說明


browser = webdriver.Chrome('chromedriver') 
browser.implicitly_wait(10)
browser.window_handles
browser.get('http://mops.twse.com.tw/mops/web/t05st02') 

while(now != end+day):

	#nb = webdriver.Chrome('chromedriver')

	#switch windows handle
	#browser.window_handles

	

	inputy = browser.find_element_by_id('year')
	inputm = browser.find_element_by_id('month')
	inputd = browser.find_element_by_id('day')
	keys = now.strftime("%Y%m%d")
	print "Retrieve date: " + keys
	inputy.send_keys(str(int(keys[0:4])-1911))
	inputm.send_keys(str(int(keys[4:6])))
	inputd.send_keys(str(int(keys[6:8])))

	browser.find_element_by_xpath('//input[@value=" 搜尋 "]').click()
	time.sleep(2)


	# 0 1 4
	#title = browser.find_elements_by_xpath('//table[@class="hasBorder"]/tbody/tr/td')

	#content = browser.find_elements_by_xpath('//input[@value="詳細資料"]')
	count = len(browser.find_elements_by_xpath('//input[@value="詳細資料"]'))

	while(count == 0):
		warning = browser.find_element_by_xpath('//h3').text
		if u"查無" in warning:
			print keys + ": No item."
			break
		else:
			count = len(browser.find_elements_by_xpath('//input[@value="詳細資料"]'))


	if not os.path.exists("mops"):
			os.makedirs("mops")
	for i in range(count):

		item = browser.find_elements_by_xpath('//div[@id="table01"]/form/table/tbody/tr/td')

		nnum = item[i*6+2].text.replace(" ","")
		nname = item[i*6+3].text.replace(" ","")
		ndate = str(int(item[i*6].text.replace("/",""))+19110000).replace(" ","")
		ntime = item[i*6+1].text.replace(":","").replace(" ","")
		nsub = item[i*6+4].text.replace(" ","")
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

		while (True):
			try:

				browser.find_elements_by_xpath('//input[@value="詳細資料"]')[i].click()

				#title[i].text
				#content[i].click()
				time.sleep(1.5)
				break;
			except:
				time.sleep(1)
				#print "Waiting." + nsub

		while(True):
			try:
				content_in = browser.find_element_by_xpath('//pre/font[@size="2"]').text+"\n"
				inside = browser.find_elements_by_xpath('//td[@style="text-align:left !important;"]')
				#print browser.find_element_by_xpath('//pre[@style="font-family:細明體; !important;"]').text+"\n"
				
				content += inside[3].text.replace(" ","")+"\n"+inside[4].text.replace(" ","") +"\n"+content_in
				break
			except:
				time.sleep(1)
				#print "waiting.." + nsub


		#print browser.find_element_by_xpath('//pre/font[@size="2"]')
		while(True):
			try:
				browser.find_element_by_xpath('//a[@onclick="ajax_back();"]').click()
				break
			except:
				time.sleep(1)
				#print "Waiting..." + nsub



		f = codecs.open(fn, "w+", "utf-8")
		f.write(content)
		f.close()
		time.sleep(1.5)
	
	now += day

browser.quit()








