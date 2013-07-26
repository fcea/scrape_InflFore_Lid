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

def get_info(urrs):
	driver = webdriver.Firefox()
	driver.get(urrs)
	dis_distinto = 0 #es 1 solo en caso en que element = 0

	nombre_cat = driver.find_elements_by_xpath(r'/html/body/div[6]/div[3]/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/div/ul/li[3]')
	element = driver.find_elements_by_xpath(r'/html/body/div[6]/div[3]/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/div[3]/div[2]/ul/li/a[3]')
	element2 = driver.find_elements_by_class_name('prod_referencia')
	element3 = driver.find_elements_by_class_name('price')
	i=0
	#VALIDACION PARA CAMBIOS DE DISENO EN PAGINAS PARTICULARES
	if len(element)==0:
		dis_distinto=1
		element= driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div/div[2]/ul/li/a[3]')
	code = nombre_cat[0].get_attribute("innerHTML").encode('utf-8').strip()
	code2 =code[code.find(' '):].strip()
	precios_unit = []
	#SACO LOS DATOS DE LOS ELEMENTOS QUE VIENEN COMO TABLAS
	error =-1
	precios_unit2=[]
	tope =urrs[urrs.find('pageSize')+9:]
	maxx = min(len(element3),int(tope)) #cuento numero de elementos en la pagina	
	j=1
	while j<=maxx:
		ss= '[' + str(j) + ']'
		text=''
		if dis_distinto == 0:
			element_name = driver.find_elements_by_xpath(r'/html/body/div[6]/div[3]/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/declareparam/div[3]/div[2]/ul/li' + ss+ r'/a[3]')
		else:
			element_name = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div/div[2]/ul/li' + ss+ r'/a[2]/strong')
		text= element_name[0].get_attribute("innerHTML").encode('utf-8').strip()
		print text
		j=j+1
		precios_unit2.append(text)
	#SACO LOS DATOS DE LOS ELEMENTOS QUE VIENEN COMO BLOQUES
	while i < len(element):
		x = element[i].get_attribute("innerHTML").encode('utf-8').strip()
		aux = element2[i].get_attribute("innerHTML").encode('utf-8').strip()
		z= aux[aux.find(";")+1:-1]
		y = element3[i].get_attribute("innerHTML").encode('utf-8').strip()
		precios_unit.append(code2+'\\'+z+'\\'+x+'\\'+y+'\\'+precios_unit2[i])
		i=i+1
	driver.close()
	return precios_unit

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

if __name__ == '__main__':
	data1 = []
	data2 = []
	data3 = []
	data4 = []
	links = []
	tod =datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
	w1 = open(tod + '_WS_Lider_noAli.txt', 'w')
	l = open('_Links_Lider_noAli.txt', 'r+')
	count = 0
	max_Count = file_len('_Links_Lider_noAli.txt')
	rl = l.readlines()
	while  count<max_Count:
		print str(count) + " " + rl[count]
		data1.extend(get_info(rl[count]))
		count = count +1
	for dato in data1:
		w1.write("%s\n" % dato)