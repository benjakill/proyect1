import RPi.GPIO as GPIO
import MFRC522
import time
import signal
import sqlite3
from operator import methodcaller
#----------------------------importaciones
continuar_leyendo=True
data=sqlite3.connect("usr.db")
c=data.cursor()
GPIO.setup(17, GPIO.OUT)#verde
GPIO.setup(21,GPIO.OUT)#rojo
#----------------------------variables importantes

def salida(signal,frame):
    global continuar_leyendo
    print "Cerrando Programa..."
    continuar_leyendo=False
    GPIO.cleanup()
    return 0

signal.signal(signal.SIGINT, salida)

lector=MFRC522.MFRC522()

while continuar_leyendo:
    (status,Tag)=lector.MFRC522_Request(lector.PICC_REQIDL)
    if status==lector.MI_OK:
        print "Tarjeta detectada"
    (status,uid)=lector.MFRC522_Anticoll()
    if status==lector.MI_OK:
        aux=map(hex,uid[:4])
        aux=map(methodcaller("replace","0x",""),aux)#aux es lista de la id como hex
	idhex="".join(aux)#id en hex como string
	c.execute("SELECT * FROM tarjetas WHERE uid=?", (idhex,))
	a=c.fetchone()
	if a==None:
		print "Acceso denegado"
		GPIO.output(21,True)
		time.sleep(2)
		GPIO.output(21,False)
		#prender leds
	else:
		print "Bienvenido "+str(a[1])
		GPIO.output(17,True)
		time.sleep(2)
		GPIO.output(17,False)
