# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import os.path

# Cargar archivo con usario y contraseña para conectarse a la base de datos
fName = "mysql-credentials.txt"
if os.path.isfile(fName):
  f = open(fName, "r")

if f:
  dbUser = f.readline()
  dbUser = dbUser.strip(" \n\r\t")
  dbPassword = f.readline()
  dbPassword = dbPassword.strip(" \n\r\t")

# Conectarse a la base de datos
dbEngine = create_engine("mysql://%s:%s@localhost/chiliproject" % (dbUser, dbPassword))
connection = dbEngine.connect()

# Ejecutar un query
result = dbEngine.execute("select title from wiki_pages")

for row in result:
  print "Wiki page title:", row['title']

result.close()

