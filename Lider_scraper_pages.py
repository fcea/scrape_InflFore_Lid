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
	nombre_cat = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div/ul/li[3]')
	element = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div[2]/ul/li/a[3]')
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
			element_name = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div[2]/ul/li' + ss+ r'/a[2]/strong')
			element_price = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div[2]/ul/li' +ss + '/small')
		else:
			element_name = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div/div[2]/ul/li' + ss+ r'/a[2]/strong')
			element_price = driver.find_elements_by_xpath(r'/html/body/div[6]/declareparam/declareparam/declareparam/declareparam/div/declareparam/declareparam/declareparam/declareparam/div[3]/div/div[2]/ul/li' +ss + '/small')
		try:
			if len(element_price) == 1:
				text= element_name[0].get_attribute("innerHTML").encode('utf-8').strip() + "\\" +element_price[0].get_attribute("innerHTML").encode('utf-8').strip()
			elif len(element_price) == 2:
				text= element_name[0].get_attribute("innerHTML").encode('utf-8').strip() + "\\" + "duplicar"
			elif len(element_price) == 3:
				text=  element_name[0].get_attribute("innerHTML").encode('utf-8').strip() + "\\" + element_price[1].get_attribute("innerHTML").encode('utf-8').strip()
			else:
				text=  element_name[0].get_attribute("innerHTML").encode('utf-8').strip() + "\\" + "sin valor"
			j=j+1
			precios_unit2.append(text)
		except IndexError: #esto se hace en caso de que existan espacios sin productos.. existe la grilla pero no el producto
			j=j+1
			maxx=maxx+1 
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
	tod = datetime.datetime.now().strftime("%Y-%m-%d")
	w1 = open(tod + '_WS_Lider1.txt', 'w')
	w2 = open(tod + '_WS_Lider2.txt', 'w')
	w3 = open(tod +'_WS_Lider3.txt', 'w')
	w4 = open(tod + '_WS_Lider4.txt', 'w')
	l = open(tod+'_Links_Lider.txt', 'r+')
	count = 0
	max_Count = file_len(tod+'_Links_Lider.txt')
	rl = l.readlines()
	while count <100 and count<max_Count:
		print str(count) + " " + rl[count]
		data1.extend(get_info(rl[count]))
		count = count +1
	for dato in data1:
		w1.write("%s\n" % dato)
	while count <200 and count<max_Count:
		print str(count) + " " + rl[count]
		data2.extend(get_info(rl[count]))
		count = count +1
	for dato in data2:
		w2.write("%s\n" % dato)
	while count <300 and count<max_Count:
		print str(count) + " " + rl[count]
		data3.extend(get_info(rl[count]))
		count = count +1
	for dato in data3:
		w3.write("%s\n" % dato)
	while count <500 and count<max_Count:
		print str(count) + " " + rl[count]
		data4.extend(get_info(rl[count]))
		count = count +1
	for dato in data4:
		w4.write("%s\n" % dato)