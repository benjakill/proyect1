import sqlite3
import RPi.GPIO as GPIO
import MFRC522
import signal
from operator import methodcaller
data=sqlite3.connect("usr.db")
c=data.cursor()

continuar_leyendo=True
print "Acerque tarjeta para agregar a db."
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
	nombre=str(raw_input("Ingrese nombre del propietario: "))
	linea=(idhex,nombre)
	c.execute("INSERT INTO tarjetas VALUES (?,?)",linea)
data.commit()
data.close()

