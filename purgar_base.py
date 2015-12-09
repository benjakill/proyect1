import sqlite3
data=sqlite3.connect("usr.db")
c=data.cursor()
c.execute("DROP TABLE IF EXISTS tarjetas")
c.execute('''CREATE TABLE tarjetas
			(uid text, nombre text)''')
data.commit()
data.close()
