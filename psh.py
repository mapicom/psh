# PSH (Pinos SHell) by Maxim Pinigin
# Copyright (c) Maxim Pinigin
# Lic: ISC

import psh_config
import socket
import time
import os

global enter_password
enter_password = 0

print("Starting PSH server on " + psh_config.ip + ":" + str(psh_config.port) + "...")

while True:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((psh_config.ip,psh_config.port))
	sock.listen(psh_config.maxconnects)
	
	conn, addr = sock.accept()

	print("Connected from: ", addr)
	conn.settimeout(psh_config.timeout)
	conn.send(b"Pinos SHell by Maxim Pinigin\r\n")
	conn.send(b"Hello! Please enter login: ")
	while True:
		data = conn.recv(1024)
		if not data:
			print("Client disconnected, restart server..\n")
			conn.close()
			time.sleep(1)
			time.sleep(10)
			break
			break
		print(data)
		if enter_password == 0 and data == psh_config.userlogin:
			conn.send(b"Ok, enter password: ")
			enter_password = 1
		elif enter_password == 1 and data == psh_config.userpassword:
			#name = psh_config.userlogin.decode("utf-8")
			conn.send(b"Welcome to PSH!\r\n")
			enter_password = 0
			break
		else:
			conn.send(b"You are a fake! Please, retry or press CTRL+C\r\n")
			enter_password = 0
			conn.send(b"Hello! Please enter login: ")
	while True:
		conn.send(b"Pinos $ ")
		data = conn.recv(1024)
		if not data:
			print("Client disconnected, restart server..\n")
			conn.close()
			time.sleep(1)
			time.sleep(10)
			break
		udata = data.decode("utf-8")
		text = udata.replace('\n','')
		command = text.split(' ') # SCS
		print(text)
		if text == "test":
			conn.send(b"Hello, World!\r\n")
		elif text == "exit":
			conn.send(b"Goodbye! :(\r\n")
			print("Client disconnected, restart server..\n")
			conn.close()
			time.sleep(1)
			time.sleep(10)
			break
		elif text == "serverinfo":
			text_to_send = "Socket Timeout: " + str(psh_config.timeout) + "\r\n"
			text_to_send += "Server IP: " +str(psh_config.ip) + "\r\n"
			text_to_send += "Server Port: " + str(psh_config.port) + "\r\n"
			conn.send( text_to_send.encode("utf-8") )
		elif command[0] == "md":
			try:
				os.mkdir(command[1])
			except:
				conn.send(b"Ops, error. Maybe, directory is't exist?\r\n")
		elif command[0] == "rd":
			try:
				os.rmdir(command[1])
			except:
				conn.send(b"Ops, error. Maybe, direcotry is't exist?\r\n")
		elif data == b"\n": prostovar = 0
		else:
			conn.send(b"Undefined command\r\n")
time.sleep(1)
