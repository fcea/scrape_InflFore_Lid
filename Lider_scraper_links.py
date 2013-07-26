from bs4 import BeautifulSoup
from urllib2 import urlopen
import itertools
import csv
from math import ceil
import datetime 
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

BASE_URL = "http://www.lider.cl"

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")


def get_category_links(section_url):
	soup = make_soup(section_url)
	boccat = soup.find_all("a", "cursorpointer alertCheck") #Busco el tag "ul" con class= "sub"
	category_links = [BASE_URL + tag["hreflang"] for tag in boccat]	
	return category_links


def get_category_siblings(link_url):
	soup2 = make_soup(link_url)
	prod_list = soup2.find("div", class_="pages-search").find("div", class_ = "pages-shopping").find("p", class_ = "info") #Busco el tag "p" con class= "prod_referencia"
	num2str= prod_list.contents[3].encode('utf-8')[prod_list.contents[3].encode('utf-8').find(">")+1:prod_list.contents[3].encode('utf-8').find("<",8)]
	return  int(num2str) 


if __name__ == '__main__':
	data = []
	links = []
	tod = datetime.datetime.now().strftime("%Y-%m-%d")
	food_n_drink = ("http://www.lider.cl"
                    "/dys/catalog/categoryFood.jsp?id=CF_Nivel0_000001&navAction=jump")
	l = open(tod+'_Links_Lider.txt', 'w')
	categories = get_category_links(food_n_drink)
	for category in categories:
		try:
			pages = get_category_siblings(category)
			if category.find("navCount")!=-1:
				print category
				links.append(category + "&goToPage=1&pageSize=" + str(pages))
			time.pause(5)
		except AttributeError:
			pass
	for link in links:
		l.write("%s\n" % link)