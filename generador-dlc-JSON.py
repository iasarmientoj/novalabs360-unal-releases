

import os
import json

package = 'novalabs360unal'
link_s3 = "https://assetbundles-nl360.s3.us-west-2.amazonaws.com" + '/' + package

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
		size = os.path.getsize(carpeta + "/" + nombre_dlc)
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
	lista_archivos = [f for f in os.listdir( carpeta ) if os.path.isfile(os.path.join(carpeta, f)) and os.path.splitext(f)[1] != ".dlc"]
	for archivo in lista_archivos:
		url = link_s3 + "/" + carpeta + "/" + archivo
		type = "ERRORRRRRRRRRRRRRRRRR"
		if os.path.splitext(archivo)[1] == ".mp4":
			type = "video"
		elif os.path.splitext(archivo)[1] == ".jpg":
			type = "image"
		elif os.path.splitext(archivo)[1] == ".zip":
			type = "zip"
		size = os.path.getsize(carpeta + "/" + archivo)
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











