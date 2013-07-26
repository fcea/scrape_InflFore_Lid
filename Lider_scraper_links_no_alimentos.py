from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools
import csv
from math import ceil
import datetime 
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

def get_urls_from_menu_bar(urrs):
	driver = webdriver.Firefox()
	driver.get(urrs)
	element2 = driver.find_elements_by_class_name('seccion')
	i=0
	urls=[]
	while i <len(element2):
		texto= element2[i].get_attribute("innerHTML").encode('utf-8').strip()
		pos_ini = texto.find('hreflang')+11
		pos_fin = texto.find('"',23)
		urls.append(urrs + texto[pos_ini:pos_fin])
		i=i+1
	driver.close()
	return urls

def get_category_siblings(link_url):
	soup2 = make_soup(link_url)
	prod_list = soup2.find("div", class_="pages-search").find("div", class_ = "pages-shopping").find("p", class_ = "info") #Busco el tag "p" con class= "prod_referencia"
	num2str= prod_list.contents[3].encode('utf-8')[prod_list.contents[3].encode('utf-8').find(">")+1:prod_list.contents[3].encode('utf-8').find("<",8)]
	return  int(num2str)

if __name__ == '__main__':
	tod =datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	l = open(tod+'_Links_Lider_noAli.txt', 'w')
	links = get_urls_from_menu_bar('http://www.lider.cl/')
	full_links = []
	for link in links:
		try:
			pages = get_category_siblings(link)
			if link.find("navCount")!=-1:
				print link
				full_links.append(link + "&goToPage=1&pageSize=" + str(pages))
		except AttributeError:
			pass
	for link in full_links:
		l.write("%s\n" % link)