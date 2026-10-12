

import os
import json

# las URLs apuntan a GitHub Releases: una release por lab, con tag = codigo del lab
link_s3 = "https://github.com/iasarmientoj/novalabs360-unal-releases/releases/download"

# carpeta con una subcarpeta por lab (.dlc, .zip, .jpg). Va fuera del repo: esos archivos se suben a Releases, no a git
ruta_labs = "../DLC Geotecnia"

# LEER DEL ARCHIVO codin-nombres-version-disp-orden.txt, ese da el orden y los laboratorios disponibles

class LabSettingsObjeto:
	def __init__(self,codin,version,category,nombre):
		self.codin = codin
		self.version = version
		self.category = category
		self.nombre = nombre
		
class ExperienceObjeto:
	def __init__(self,id,name,version,content,category):
		self.id = id
		self.version = version
		self.name = name
		self.content = content
		self.category = category
		self.additionalSources = []
		
class ContentObjeto:
	def __init__(self,url,type,size,key):
		self.url = url
		self.type = type
		self.size = size
		self.key = key
		


orden_labs = []
with open('codin-nombres-version-disp-orden.txt' ,'r' , encoding='utf-8') as my_file:
	for line in my_file:
		nuevoLab = LabSettingsObjeto( line.split("\t")[0], line.split("\t")[1], line.split("\t")[2], line.split("\t")[3].split("\n")[0] )
		orden_labs.append(nuevoLab)


experienceList = []

# HACER TODO EL PROCESO EN EL ORDEN DEL ARRAY
for experiencia in orden_labs:
	
	contentList = []
	
	carpeta = experiencia.codin
	nombre_dlc =  carpeta + ".dlc"
	
	#agregar a content el android dlc
	#el archivo se lee suelto en la carpeta del lab (sin subcarpeta android),
	#pero el key conserva "/android/" porque la app elige el dlc con key.Contains(plataforma)
	url = link_s3 + "/" + carpeta + "/" + nombre_dlc
	type = "dlc"
	try:
		size = os.path.getsize(os.path.join(ruta_labs, carpeta, nombre_dlc))
	except:
		size = 0
	key = carpeta + "/android/" + nombre_dlc
	
	contentList.append(ContentObjeto(url, type, size, key))
	
	#agregar a content el ios dlc
	url = link_s3 + "/" + carpeta + "/ios/" + nombre_dlc
	type = "dlc"
	try:
		size = os.path.getsize(carpeta + "/ios/" + nombre_dlc)
	except:
		size = 0
	key = carpeta + "/ios/" + nombre_dlc
	
	contentList.append(ContentObjeto(url, type, size, key))
	
	# obtener cada archivo con su peso
	#el .dlc ya se agrego arriba como android, no se repite como contenido
	lista_archivos = [f for f in os.listdir( os.path.join(ruta_labs, carpeta) ) if os.path.isfile(os.path.join(ruta_labs, carpeta, f)) and os.path.splitext(f)[1] != ".dlc"]
	#con zip los videos van dentro de el: un .mp4 suelto (copia, archivo de camara) no se lista, o la app lo bajaria aparte
	tiene_zip = any(os.path.splitext(f)[1] == ".zip" for f in lista_archivos)
	for archivo in lista_archivos:
		url = link_s3 + "/" + carpeta + "/" + archivo
		extension = os.path.splitext(archivo)[1]
		if extension == ".zip":
			type = "zip"
		elif extension == ".jpg":
			type = "image"
		elif extension == ".mp4" and not tiene_zip:
			type = "video"
		else:
			continue   # .meta de Unity, .MP4 de camara, etc.: antes salian como "ERRORRRR" y la app intentaba bajarlos
		size = os.path.getsize(os.path.join(ruta_labs, carpeta, archivo))
		key = carpeta + "/" + archivo
		contentList.append(ContentObjeto(url, type, size, key))
	
	
	cont = []
	for c in contentList:
		cont.append(json.dumps(c.__dict__, ensure_ascii=False))
	
	
	
	experienceList.append(ExperienceObjeto(carpeta, experiencia.nombre, experiencia.version, cont, experiencia.category))
	
	

op = []
for operacion in experienceList:
	op.append(json.dumps(operacion.__dict__, ensure_ascii=False))

with open('ExperiencesList_.json', 'w', encoding='utf-8') as f:
	json.dump(op, f, ensure_ascii=False, indent=4)



#arreglar json
with open('ExperiencesList_.json', 'r', encoding='utf-8') as file :
  filedata = file.read()

filedata = filedata.replace('\\\\\\"', '#')
filedata = filedata.replace('\\"', '#')
filedata = filedata.replace('#{', '{')
filedata = filedata.replace('}#', '}')
filedata = filedata.replace('"', '')
filedata = filedata.replace('#', '"')

with open('ExperiencesList_.json', 'w', encoding='utf-8') as file:
  file.write(filedata)











