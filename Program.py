import hashlib
import threading
import os
import sys

MAX_THREAD_COUNT = 10

file_system = os.walk(os.getcwd()) #only current warking directory
fiel_data = {}

def check_files(file_hash,file_name):
	if file_hash in fiel_data.keys():
		fiel_data[file_hash].append(file_name)
	else:
		fiel_data[file_hash] = [file_name]

def getHash(fileName): # claculate hash value of input
	h = hashlib.sha1()
	with open(fileName,'rb') as file:
		chunk = 0;
		while chunk !=b'':
			chunk = file.read(1024)
			h.update(chunk)
	if threading.activeCount() < MAX_THREAD_COUNT:
		thread = threading.Thread(target=check_files,args=(h.hexdigest(),fileName))
		thread.start()


for dir_path, dir_name, file_names in file_system:
	if len(file_names) >= 1:
		for file_name in file_names:
			if threading.activeCount() < MAX_THREAD_COUNT:
				thread = threading.Thread(target=getHash(os.path.join(dir_path,file_name)))

for key in fiel_data.keys():
	if len(fiel_data[key]) > 1:
		print(key,'{')
		for file in fiel_data[key]:
			print(f'\t{file}')
		print('}') 
			
