# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import os
from subprocess import call

def main():
  global dbEngine
  base_dir = "/home/ernesto/test/repotest/"
  
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

  #fsalida = open("salida.txt", "w")

  # Ejecutar un query
  projects = dbEngine.execute("select id, name, identifier, description from projects")

  # obtener todos los proyectos
  for project in projects:
    #fsalida.write("Project name: %s\n" % project['name'])
    #fsalida.write("Project description: %s\n" % project['description'])
    #print_wikis(fsalida, project["id"])
    #fsalida.write("\n-----------------------------------\n\n")
    create_file_struct(base_dir, project["identifier"])

  projects.close()
  #fsalida.close()

def print_wikis(fsalida, project_id):
  # para cada proyecto, obtener sus wikis
  wikis = dbEngine.execute("select id from wikis where project_id = %s" % project_id)
  
  for wiki in wikis:
    # obtener las páginas que integran la wiki
    wiki_pages = dbEngine.execute("select id, title from wiki_pages where wiki_id = %s" % wiki["id"])
    
    for page in wiki_pages:
      fsalida.write("Wiki page title: %s\n" % page['title'])
      # para cada página, obtener su contenido
      contents = dbEngine.execute("select text from wiki_contents where page_id = %s" % page["id"])
      for content in contents:
        fsalida.write("%s\n" % content["text"])
      contents.close()    
    
    wiki_pages.close()
  
  wikis.close()

def create_file_struct(base_dir, project_name):
  wiki_path = os.path.join(base_dir, project_name, "wiki")
  src_path = os.path.join(base_dir, project_name, "src")
  
  if not os.path.exists(wiki_path):
    os.makedirs(wiki_path)
  if not os.path.exists(src_path):
    os.makedirs(src_path)
  
  # iniciar el repo del wiki
  call(["git", "init", wiki_path])
  

if __name__ == "__main__":
    main()
