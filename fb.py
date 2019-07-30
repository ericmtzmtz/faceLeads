#!/usr/bin/env python3
# Code by Eric Martinez
# for Offhack 2018
#
# El autor no se hace responsable por el uso
# indebido de esta herramienta.

# importaciones
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import csv
import datetime
import sys
import configparser


def configuracion():
	try:
		config = configparser.RawConfigParser()
		config.read('facebook.conf')

		username = config.get('Facebook Creeds', 'username')
		password = config.get('Facebook Creeds', 'password')

		# Ruta del driver de chrome
		# Creamos la instancia de chrome
		chrome_path = r"C:\\chromedriver.exe"
		chrome_options = Options()
		prefs = {"profile.default_content_setting_values.notifications": 2}
		chrome_options.add_experimental_option("prefs", prefs)
		driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)

		# Por lo pronto solo lo usaremos en facebook
		sitio = "https://fb.com"
		driver.get(sitio)

		# Nos logeamos con nuestras passwords
		driver.find_element_by_xpath(
			"""//*[@id="email"]""").send_keys(username)
		driver.find_element_by_xpath("""//*[@id="pass"]""").send_keys(password)
		driver.find_element_by_id("loginbutton").click()

	except Exception as e:
		print(e)
		print("Creaste bien tu archivo facebook.conf ??")
		sys.exit(1)

	return driver


# https://stackoverflow.com/a/43952192
def print_statusline(msg):
	last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
	print(' ' * last_msg_length, end='\r')
	print(msg, end='\r')
	sys.stdout.flush()  
	print_statusline.last_msg = msg


def clearScreen():
	import os
	if os.name == "nt":
		os.system("cls")
	elif os.name == "posix":
		os.system("clear")
	else:
		print ("<-No se pudo borrar la pantalla->")
		raise "No se puede limpiar la pantalla"

# Buscamos la pagina


def buscarPagina(pag):
	pagina = pag + "\n"
	driver.get("https://www.facebook.com/search/pages/?q=" + pagina)
	time.sleep(7)
	driver.find_element_by_css_selector("._pac a").click()


# Obtenemos los seguidores
def seguidores(pag):
	pagina = pag
	facebook_file = pagina + "_facebook.csv"
	print()
	print(("Vamos a crear el archivo " + facebook_file))
	carpeta_trabajo = "facebook_information"

	if not os.path.isdir(carpeta_trabajo):
		try:
			os.mkdir('facebook_information')
		except:
			print("No se puede crear directorio de trabajo \"facebook_information\"")

	username_directory = os.path.dirname(os.path.abspath(
		__file__)) + "\\facebook_information\\" + pagina
	if not os.path.isdir(username_directory):
		os.mkdir(username_directory)

	csvFile = open(username_directory + "/" + facebook_file, "w")
	csvWriter = csv.writer(csvFile)
	csvWriter.writerow(["", "Reporte"])
	csvWriter.writerow(["", "OFFHACK"])
	csvWriter.writerow(["", ""])
	csvWriter.writerow(["", "https://offhack.com"])
	csvWriter.writerow([""])
	csvWriter.writerow(
		["", ">>> Fecha:", datetime.datetime.now().strftime('%Y-%m-%d')])
	csvWriter.writerow(
		["", ">>> Hora:", datetime.datetime.now().strftime('%H:%M')])
	csvWriter.writerow(["", ">>> Usuario Analizado:", pagina])
	csvWriter.writerow(["", ">>> Informacion:", "Facebook seguidores"])
	csvWriter.writerow([""])
	csvWriter.writerow(["#", "Nombre", "Perfil_Facebook",
						"Dato_Resaltado", "Otros_Datos"])

	SCROLL_PAUSE_TIME = 10
	print()
	print("Estamos buscando leads ...\n")
	pagUsuario = 1
	ultimoUsuario = ''
	while True:
		user_info = driver.find_elements_by_class_name("clearfix")
		usuario_lista = []

		for user in user_info:
			try:
				u = user.find_elements_by_class_name(
					"_52eh")[0].text.encode('utf-8')
				usuario_lista.append(u)
			except:
				continue

		ultimoUsuario = usuario_lista[-1]
		driver.execute_script(
			"window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(SCROLL_PAUSE_TIME)
		try:
			fin = driver.find_elements_by_id(
				"browse_end_of_results_footer")
		except:
			fin = False

		texto = "\t{0} \tPagina(s) Analizada(s) \t{1} \tUsuario(s) Encontrado(s)  Ultimo Usuario Encontrado:  {2}".format(str(pagUsuario), str(len(user_info)), ultimoUsuario.decode('utf-8'))
		print_statusline(texto)
		pagUsuario += 1

		masResultados=driver.find_element_by_class_name("hidden_elem")
		if ultimoUsuario == usuario_lista[-2]:
			fin=True
		if not masResultados:
			espera=0
			while True:
				if driver.find_element_by_class_name("hidden_elem"):
					sys.stdout.write("Se encontro mas leads")
					sys.stdout.flush()
					break
				else:
					time.sleep(60)
					espera += 1
					if espera == 10:
						print("Se espero 10 minutos a que cargara mas resultados ...")
						fin=True
						break

		if fin:
			print()
			print()
			print("Good!! Se obtuvieron todos los leads.")
			break

	# Obtenemos la lista de leads
	user_info=driver.find_elements_by_class_name("_glj")

	usuarioNumero=1
	for user in user_info:
		usuario_lista=[]
		u=user.find_elements_by_class_name("_52eh")[0].text.encode('utf-8')
		usuario_lista.append(u)

		url=user.find_element_by_css_selector("._32mo").get_attribute('href')
		usuario_lista.append(url)

		t=user.find_elements_by_class_name("_pac")[0].text.encode('utf-8')
		usuario_lista.append(t)

		numero=0
		for i in range(len(user.find_elements_by_class_name("_52eh"))):
			numero += 1
			if numero in range(len(user.find_elements_by_class_name("_52eh"))):
				datos=user.find_elements_by_class_name(
					"_52eh")[numero].text.encode('utf-8')
				usuario_lista.append(datos)
			else:
				continue

		csvWriter.writerow([usuarioNumero, usuario_lista[0], usuario_lista[1],
							usuario_lista[2], usuario_lista[3:]])
		print_statusline(str(usuarioNumero) + " Usuario(s)")
		usuarioNumero += 1

		clearScreen()
	return usuarioNumero

# banner de comandos


def banner():
	print("Elige una opcion:")
	print()
	print("[1] Buscar Pagina")
	print("[2] Buscar seguidores en la pagina actual")
	print("[3] Salir")

# Banner de seguidores


def banner_leads():
	print("Elige una opcion:")
	print()
	print("[1] Recoger leads")
	print("[2] Volver a buscar pagina")


# Instaciamos Driver
driver=configuracion()

# Mando principal de comandos
while True:
	try:
		clearScreen()
		banner()
		comando=input(">> ")
		# Para buscar la pagina
		if comando == "1":
			pagina=input("Que pagina deseas buscar: ")
			print()
			print("Buscando " + pagina)
			buscarPagina(pagina)
			clearScreen()
			banner_leads()
			comando == input(">> ")
			if comando == "1":
				numeroLeads=seguidores(pagina)
				print()
				print()
				print_statusline(str(numeroLeads) + " Usuario(s) Obtenido(s)")
			else:
				print("Volviendo al menu principal")
		# Para Buscar en la pagina actual
		elif comando == "2":
			pagina=input("Como se llama la pagina? >> ")
			numeroLeads=seguidores(pagina)
			print()
			print()
			print_statusline(str(numeroLeads) + " Usuario(s) Obtenido(s)")
		# Salir del script
		elif comando == "3":
			driver.quit()
			break
	except Exception as e:
		print("\n")
		print(e)
		print()
		print("Algo salio mal")
		time.sleep(5)
		continue
