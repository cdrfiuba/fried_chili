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
  result = dbEngine.execute("select id, name, identifier, description, is_public from projects")
  projects = result.fetchall()

  # Obtener todos los proyectos
  for project in projects:
    parent_name, parent_id = get_root_parent(project["id"])
    print parent_name
    if project["is_public"]:
      project_path = os.path.join(base_dir, parent_name, "public", project["identifier"])
    else:
      project_path = os.path.join(base_dir, parent_name, "private", project["identifier"])
    
    create_file_struct(project_path)
    
    # generar los wikis para este proyecto
    generate_wikis(os.path.join(project_path, "wiki"), project["id"])
  

# Obtener el proyecto padre raíz
def get_root_parent(project_id):
  result = dbEngine.execute("select parent_id, identifier from projects where id = %s" % project_id)
  parent = result.fetchall()[0]
  print parent
  parent_name = parent["identifier"]
  parent_id = parent["parent_id"]
  
  while parent_id:
    parent_name, parent_id = get_root_parent(parent_id)
        
  return parent_name, parent_id
  

# Generar todas las wikis para un proyecto
def generate_wikis(wiki_base_path, project_id):
  # para cada proyecto, obtener sus wikis
  result = dbEngine.execute("select id from wikis where project_id = %s" % project_id)
  wikis = result.fetchall()
  
  for wiki in wikis:
    # obtener las páginas que integran la wiki
    result = dbEngine.execute("select id, title from wiki_pages where wiki_id = %s" % wiki["id"])
    wiki_pages = result.fetchall()
    
    for page in wiki_pages:
      wiki_file = open(os.path.join(wiki_base_path, page["title"] + ".txt"), "w")
      # para cada página, obtener su contenido
      result = dbEngine.execute("select text from wiki_contents where page_id = %s" % page["id"])
      contents = result.fetchall()
      for content in contents:
        wiki_file.write("%s\n" % content["text"])
      wiki_file.close();


# Crea la estructura de carpetas para colocar los proyectos
def create_file_struct(project_dir):
  wiki_path = os.path.join(project_dir, "wiki")
  src_path = os.path.join(project_dir, "src")
  
  # Crear las carpetas si es que no existen
  if not os.path.exists(wiki_path):
    os.makedirs(wiki_path)
  if not os.path.exists(src_path):
    os.makedirs(src_path)
    
  # Iniciar el repositorio de git para el wiki
  call(["git", "init", wiki_path])


if __name__ == "__main__":
  main()



