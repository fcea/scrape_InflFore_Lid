import csv
from math import ceil
import datetime 
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from bs4 import UnicodeDammit
import MySQLdb as mdb
import time
import sys
import random 

#METODO QUE CREA LA TABLA SQL  EN CASO DE QUE NO EXISTA
def create_Table_Productos(name):
	con = mdb.connect('localhost', 'root', 'password', 'LiderWebscraping');
	with con:
	    
	    cur = con.cursor()
	    #cur.execute("DROP TABLE IF EXISTS "+tableName)
	    cur.execute("CREATE TABLE IF NOT EXISTS "+name+"(SKU VARCHAR(50),\
	                Categoria VARCHAR(200) ,\
	                Cod_Categoria INT ,\
					Marca VARCHAR(200) ,\
	                Producto VARCHAR(1000) ,\
  					FechaEjecucion VARCHAR(20) ,\
				  	Disponibilidad INT ,\
				  	PrecioProducto INT  ,\
				  	PrecioGranel INT ,\
				  	PrecioNormal INT)")
	con.close()

def lets_Scrape_Non_Supermarket(url, fecha_ejec, tableName):
	driver = webdriver.Firefox()
	driver.get(url)
	links = driver.find_elements_by_css_selector(".cursorpointer.alertCheck")
	linksTmp =[]
	nombresTmp = []
	cont=0
	for ref in links:
		temp = ref.get_attribute("outerHTML").encode('utf-8').strip()
		if temp.find("productList") > 0:
			linksTmp.append("http://www.lider.cl" + get_Link(temp))
			nombresTmp.append(str(cont) + "|" + ref.get_attribute("innerHTML").encode('utf-8').strip())
			cont=cont +1

	print len(linksTmp)
	print len(nombresTmp)
	driver.close()
	sys.exit(0)

	cont = 0
	



	#busco id categoria del link mas alta ingresada, asigno el valor al contador e itero desde ese punto
	cont = data_Inserted(tableName)
	while cont < len(linksTmp):
		print "Ejecuto es " + nombresTmp[cont]
		resuPart = get_info_Supermarket(driver, linksTmp[cont], fecha_ejec, nombresTmp[cont], tableName) #recupero 7 elementos a insertar, falta la fecha, categoria y cod_cate, pero estan ya aca
		cont = cont + 1 
	driver.close()









#METODO QUE COORDINA EL SCRAPING DE TODO EL SITIO WEB
#RECORRE LOS LINKS, DETERMINA LOS QUE SIRVEN. 
#DE LOS QUE SIRVEN VERIFICA CUALES AUN NO HAN SIDO VISITADOS
#HACE LA REVISION Y DESPUES LLAMA A LA FUNCION QUE INSERTA EN LA TABLA

def lets_Scrape_Supermarket(url, fecha_ejec, tableName):
	driver = webdriver.Firefox()
	driver.get(url)
	superRef = driver.find_element_by_xpath('/html/body/div[3]/div[3]/ul/li/a')
	superRef.click()
	links = driver.find_elements_by_css_selector(".cursorpointer.alertCheck")
	linksTmp =[]
	nombresTmp = []
	cont=0
	for ref in links:
		temp = ref.get_attribute("outerHTML").encode('utf-8').strip()
		if temp.find("categoryFood") == -1 and temp.find("specialCategoryFood") == -1 and temp.find("CAT_GM") == -1:
			linksTmp.append("http://www.lider.cl" + get_Link(temp))
			nombresTmp.append(str(cont) + "|" + ref.get_attribute("innerHTML").encode('utf-8').strip())
			cont = cont+1
	#driver.close()
	cont = 0
	#busco id categoria del link mas alta ingresada, asigno el valor al contador e itero desde ese punto
	cont = data_Inserted(tableName)
	while cont < len(linksTmp):
		print "Ejecuto es " + nombresTmp[cont]
		resuPart = get_info_Supermarket(driver, linksTmp[cont], fecha_ejec, nombresTmp[cont], tableName) #recupero 7 elementos a insertar, falta la fecha, categoria y cod_cate, pero estan ya aca
		cont = cont + 1 
	driver.close()
	
#METODO QUE SIRVE PARA CAMBIAR EL FORMATO DE LOS NUMEROS QUE RECUPERO DESDE LIDER
#RETORNA LA FECHA SIN SIGNOS $ NI PUNTOS 
def modify_Prices(formPrice):
	form1 = formPrice.replace(".","")
	form2 = form1.replace("$","")
	return form2

#METODO QUE SIRVE PARA VERIFICAR EL ULTIMO DATO INSERTADO EN LA TABLA SQL 
#RETORNA 0 SI LA TABLA ESTA VACIA. DE LO CONTRARIO RETORNA EL CODIGO MAS ALTO INGRESADO.
def data_Inserted(tableName):
	con = mdb.connect('localhost', 'root', 'password', 'LiderWebscraping');
	with con:
	    
	    cur = con.cursor()
	    cur.execute("SELECT Cod_Categoria FROM " +tableName)
	    #Esto me hace pasar la lista a un arreglo
	    row = [item[0] for item in cur.fetchall()]
	con.close()
	try:
		maxim = max(row)
		return maxim
	except ValueError:
		return 0

#METODO AUXILIAR PARA DEJAR EL LINK CON EL FORMATO APROPIADO
#RETORNA EL LINK CON TRIMS
def get_Link(unfText):
	st = unfText.find('lang')+6
	nd = unfText.find('"', unfText.find('lang')+6)
	return unfText[st:nd]

#METODO QUE HACE EL INSERT DENTRO DE LA TABLA SQL 

def word_to_SQL_insertion(concatString, tableName):

	con = mdb.connect('localhost', 'root', 'password', 'LiderWebscraping');
	with con:    
	    cur = con.cursor()
	    if cur.execute("SELECT * FROM "+tableName+" WHERE SKU=%s",concatString.split("|")[0]) == 0:
	    	cur.execute("INSERT INTO  "+tableName+" VALUES (%s,%s,%s,%s, %s,%s,%s,%s,%s, %s)",(concatString.split("|")[0],concatString.split("|")[1],int(concatString.split("|")[2]), concatString.split("|")[3],concatString.split("|")[4],concatString.split("|")[5],int(concatString.split("|")[6]),int(concatString.split("|")[7]),int(concatString.split("|")[8]),int(concatString.split("|")[9])))
	    else:
	    	#print 'Nada que hacer con ' + str(concatString.split("|")[0])
	    	pass
	con.close()


#METODO QUE RECUPERA LA INFORMACION DESDE LA PAGINA (HACE EL WEBSCRAPE )
#RETORNA 7 PARAMETROS DE INFORMACION AL METODO PRINCIPAL. VAN SEPARADOS POR "|" PARA SPLITEAR DESPUES

def get_info_Supermarket(driver, urls, fecha_ejec, doubleParam, tableName): 
	#genero la url correcta con todos los elementos cargados
	#driver = webdriver.Firefox()
	driver.get(urls)
	longit = driver.find_element_by_class_name('pages-shopping').find_element_by_class_name('info')
	numUnclean = longit.get_attribute("innerHTML").encode('utf-8').strip().split('<strong>')[2]
	numElem = numUnclean[:numUnclean.find('<')]
	urrs = urls[:urls.find('&')]+ '&pageSize=' + str(numElem) + '&goToPage=1'
	#tengo la url nueva correcta 
	driver.get(urrs)
	#Recupero informacion
	element2 = driver.find_elements_by_class_name('prod_referencia') #sku
	element3 = driver.find_elements_by_class_name('price') #precio rojo
	elementemp = driver.find_elements_by_css_selector('.product.ech_prod') #recupero la marca, detalle y si tiene stock.
	for ele1 in elementemp:
		#Obtengo el SKU. No hay metodo eficiente, solo busqueda en string
		auxText = ele1.get_attribute("outerHTML").encode('utf-8').strip()
		skuProd =  auxText[auxText.find("skuId=")+6:auxText.find("&",auxText.find("skuId=")) ]
		#Saco ahora la informacion de los precios y otros. Aprovecho la estructura del texto.
		info = ele1.find_elements_by_tag_name("a")
		#info[0] -> data inutil
		#info[1] -> marca
		#info[2] -> detalle		
		#info[3] -> carro de compras
		#info[4] -> carro de compras
		#info[5] -> solo los productos que estan disponibles
		#De este modo, obtengo la marca y el detalle
		marcaDirt = info[1].get_attribute("innerHTML").encode('utf-8').strip()
		marcaProd = marcaDirt[marcaDirt.find(">")+1:marcaDirt.find("<",marcaDirt.find(">"))]
		detalleProd = info[2].get_attribute("innerHTML").encode('utf-8').strip()
		#El largo del arreglo me indica finalmente para cada producto si esta disponible. Los de largo 5 no estan, los de 6 si.
		if len(info) == 5:
			availInd = 0
		elif len(info) == 6:
			availInd = 1
		else:
			print "Hay un caso no considerado"
			sys.exit(0)
		try:
			tiposPrecios = ele1.find_elements_by_class_name("retail")
			if len(tiposPrecios)==0: #significa que hay solo precio primario
				mainPrice =   modify_Prices(ele1.find_element_by_class_name("price").get_attribute("innerHTML").encode('utf-8').strip())
				granelPrice = modify_Prices(ele1.find_element_by_class_name("price").get_attribute("innerHTML").encode('utf-8').strip())
				normalPrice = modify_Prices(ele1.find_element_by_class_name("price").get_attribute("innerHTML").encode('utf-8').strip())
			elif len(tiposPrecios)==1: #significa que hay precio primario y precio granel
				auxPrice=tiposPrecios[0].get_attribute("innerHTML").encode('utf-8').strip()
				mainPrice =   modify_Prices(ele1.find_element_by_class_name("price").get_attribute("innerHTML").encode('utf-8').strip())
				granelPrice = modify_Prices(auxPrice[auxPrice.find("$")+1:auxPrice.find(" ",auxPrice.find("$")+1)])
				normalPrice = modify_Prices(auxPrice[auxPrice.find("$")+1:auxPrice.find(" ",auxPrice.find("$")+1)])
			elif len(tiposPrecios)==2: #significa que hay precio primario, granel y normal (ergo el primario esta en oferta)
				#el precio no lo puedo sacar directamente, tengo que hacer un parser manual sobre el texto outer completo
				hiddenPrice = ele1.get_attribute("outerHTML").encode('utf-8').strip().split('<small class="retail">')
				maskedPrice = tiposPrecios[1].get_attribute("outerHTML").encode('utf-8').strip()
				mainPrice =   modify_Prices(ele1.find_element_by_class_name("price").get_attribute("innerHTML").encode('utf-8').strip())
				granelPrice = modify_Prices(maskedPrice[maskedPrice.find('$'):maskedPrice.find(' ', maskedPrice.find('$'))])
				normalPrice = modify_Prices(hiddenPrice[1][hiddenPrice[1].find('$'):].strip())
			else: #caso no determinado
				print 'Hay un caso que no se esta capturando!'
				sys.exit(0)
		except: #significa que no hay ningun tag con ese nombre
			print "Hay un error en el metodo"
			sys.exit(0)
		#Proceso los parametros que no tengo 	
		codeCategory = doubleParam.split("|")[0]
		nameCategory = doubleParam.split("|")[1]
		#Hago el llamado a la funcion que inserta en la base de datos
		inputSQL = skuProd +"|"+ nameCategory +"|"+ str(codeCategory) +"|"+ marcaProd +"|"+ detalleProd +"|"+ fecha_ejec +"|"+ str(availInd) +"|"+ str(mainPrice) +"|"+ str(granelPrice) +"|"+ str(normalPrice)
		word_to_SQL_insertion(inputSQL, tableName)
	#driver.close()
	return  

#MAIN
if __name__ == '__main__':
	#fecha del dia
	d = datetime.datetime.now().strftime("%Y-%m-%d") 
	d_name = d.replace("-","")
	#inicializo tabla en MySQL
	LiderSupermarket =  d_name + '_Lider_Supermarket'
	create_Table_Productos(LiderSupermarket)
	#ejecuto el proceso 
	#lets_Scrape_Supermarket('http://www.lider.cl/dys/',d,LiderSupermarket)
	lets_Scrape_Non_Supermarket('http://www.lider.cl/dys/catalog/category.jsp?id=CAT_GM_00096&amp;navAction=jump&amp;navCount=0',d,LiderSupermarket)

