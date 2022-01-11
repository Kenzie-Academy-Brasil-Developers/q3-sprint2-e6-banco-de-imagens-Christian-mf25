import os

def check_directory(directory_name):
	try:
		return os.mkdir(f"../../files/{directory_name}")
	except:
		return "existe"

def check_file_exist(file_name, extension):
	if (os.path.isfile(f"../../files/{extension}/{file_name}")):
		return False
	else:
		return True

def all_files():
	files = {}
	folders = os.listdir("./files")
	
	for dir in folders:
		files[dir] = os.listdir(f"./files/{dir}")
	
	return files

def soma(a, b):
	return a + b


##
# quando roda uma função aqui escrita em outro lugar
# ela cria uma pasta __pycache__ e o flask run para de funcionar
# até apagar a pasta __pycache__ e tirar a pasta kenzie
# de dentro da app 
###