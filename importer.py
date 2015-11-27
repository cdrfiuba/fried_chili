# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import os
from subprocess import call


def main():
  global dbEngine
  base_dir = "/home/ernesto/test/repotest/"
  
  # Cargar credenciales para la base de datos desde un archivo externo
  fName = "mysql-credentials.txt"
  if os.path.isfile(fName):
    credentialFile = open(fName, "r")

  if credentialFile:
    dbUser = credentialFile.readline()
    dbUser = dbUser.strip(" \n\r\t")
    dbPassword = credentialFile.readline()
    dbPassword = dbPassword.strip(" \n\r\t")
    credentialFile.close()

  # Conectarse a la base de datos
  dbEngine = create_engine("mysql://%s:%s@localhost/chiliproject" % (dbUser, dbPassword))
  connection = dbEngine.connect()

  # Cargar información de los proyectos
  projects = dbEngine.execute("select id, name, identifier, description, is_public from projects")

  # Obtener todos los proyectos
  for project in projects:
    if project["is_public"]:
      create_file_struct(os.path.join(base_dir, "public"), project["identifier"])
    else:
      create_file_struct(os.path.join(base_dir, "private"), project["identifier"])

  projects.close()


# generar todas las wikis para un proyecto
def generate_wikis(wiki_base_path):
  # para cada proyecto, obtener sus wikis
  wikis = dbEngine.execute("select id from wikis where project_id = %s" % project_id)
  
  for wiki in wikis:
    # obtener las páginas que integran la wiki
    wiki_pages = dbEngine.execute("select id, title from wiki_pages where wiki_id = %s" % wiki["id"])
    
    for page in wiki_pages:
      wiki_file = open()
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
  
  # Crear las carpetas si es que no existen
  if not os.path.exists(wiki_path):
    os.makedirs(wiki_path)
  if not os.path.exists(src_path):
    os.makedirs(src_path)
  
  # Iniciar el repositorio de git para el wiki
  call(["git", "init", wiki_path])


if __name__ == "__main__":
  main()



