# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import os
from subprocess import call


def main():
  global dbEngine
  global VERBOSE_LEVEL
  
  VERBOSE_LEVEL = 10
  
  # carpeta destino donde se generarán todas las carpetas de proyectos
  base_dir = "/home/ernesto/test/repotest/"
  
  # carpeta fuente donde se encuentran los repositorios de código para 
  # copiar
  src_repo_dir = ""
  
  # carpeta fuente donde se encuentran los documentos y adjuntos para
  # copiar
  doc_dir = ""
  
  # Cargar credenciales para la base de datos desde un archivo externo
  fName = "mysql-credentials.txt"

  talk("Buscando archivo de credenciales...", 1)
  if os.path.isfile(fName):
    credentialFile = open(fName, "r")
  else:
    talk("No se encontró el archivo de credenciales!", 1)

  if credentialFile:
    dbUser = credentialFile.readline()
    dbUser = dbUser.strip(" \n\r\t")
    dbPassword = credentialFile.readline()
    dbPassword = dbPassword.strip(" \n\r\t")
    credentialFile.close()

  # Conectarse a la base de datos
  talk("Abriendo base de datos local...", 1)
  dbEngine = create_engine("mysql://%s:%s@localhost/chiliproject" % (dbUser, dbPassword))
  connection = dbEngine.connect()

  # Cargar información de los proyectos
  talk("Obteniendo información de los proyectos...", 1)
  result = dbEngine.execute("select id, name, identifier, description, is_public from projects")
  projects = result.fetchall()

  # Obtener todos los proyectos
  for project in projects:
    parent_name, parent_id = get_root_parent(project["id"])
    talk("Procesando el proyecto '" + parent_name + "/" + project["identifier"] + "'...", 1)
    if project["is_public"]:
      project_path = os.path.join(base_dir, parent_name, "public", project["identifier"])
    else:
      project_path = os.path.join(base_dir, parent_name, "private", project["identifier"])
    
    wiki_path = os.path.join(project_path, "wiki")
    src_path = os.path.join(project_path, "src")
    create_file_struct(project_path)
    
    generate_project_header(project_path, project["id"])
    
    # generar los wikis para este proyecto
    generate_wikis(wiki_path, project["id"])
        
    # copiar el repositorio de código para este proyecto
    # ...
    
    repo_init(wiki_path, "Commit inicial del wiki.")
    # ignorar los wikis que van en un repo aparte
    create_ignore_file(project_path)
    repo_init(project_path, "Commit inicial del proyecto.")

# Escribir información útil en la salida hacia usuario. El nivel de
# verbosidad es configurable.
def talk(message, level):
  if level <= VERBOSE_LEVEL:
    print message

# Obtener el proyecto padre raíz
def get_root_parent(project_id):
  result = dbEngine.execute("select parent_id, identifier from projects where id = %s" % project_id)
  parent = result.fetchall()[0]
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
    talk("\tProcesando las wikis para este proyecto...", 2)
    result = dbEngine.execute("select id, title from wiki_pages where wiki_id = %s" % wiki["id"])
    wiki_pages = result.fetchall()
    
    for page in wiki_pages:
      talk("\tGenerando la wiki '" + page["title"] + "'...", 3)
      textile_name = os.path.join(wiki_base_path, page["title"] + ".txt")
      markdown_name = os.path.join(wiki_base_path, page["title"] + ".md")
      wiki_file = open(textile_name, "w")
      # para cada página, obtener su contenido
      result = dbEngine.execute("select text from wiki_contents where page_id = %s" % page["id"])
      contents = result.fetchall()
      for content in contents:
        wiki_file.write("%s\n" % content["text"])
      wiki_file.close();
      # convert from textile to markdown wiki format
      convert_to_markdown(textile_name, markdown_name)
      # erase textile file
      os.remove(textile_name)


# Generar un archivo README con la información de la portada del proyecto, incluyendo sus participantes
def generate_project_header(path, project_id):
  # obtener info del proyecto
  result = dbEngine.execute("select description, created_on, updated_on from projects where id = %s" % project_id)
  project_info = result.fetchall()[0]
  
  members_list = get_members(project_id)
  
  textile_name = os.path.join(path, "README.txt")
  markdown_name = os.path.join(path, "README.md")
  
  header_file = open(textile_name, "w")
  
  header_file.write("Project created on: %s\n" % project_info["created_on"])
  header_file.write("Project last updated on: %s\n" % project_info["updated_on"])
  header_file.write("Project members:\n")
  for member in members_list:
    header_file.write("  %s %s <%s>\n" % (member["firstname"], member["lastname"], member["mail"]))
  header_file.write("\n")
  header_file.write("%s\n" % project_info["description"])
  header_file.close()
  
  convert_to_markdown(textile_name, markdown_name)
  os.remove(textile_name)


# Obtener los participantes del proyecto
def get_members(project_id):
  result = dbEngine.execute("select user_id, firstname, lastname, mail from members, users where users.id = members.user_id and members.project_id = %s" % project_id)
  members = result.fetchall()
  return members


# Crea la estructura de carpetas para colocar los proyectos
def create_file_struct(project_dir):
  wiki_path = os.path.join(project_dir, "wiki")
  src_path = os.path.join(project_dir, "src")
  
  # Crear las carpetas si es que no existen
  if not os.path.exists(wiki_path):
    os.makedirs(wiki_path)
  if not os.path.exists(src_path):
    os.makedirs(src_path)

# Convierte las wikis de textile a markdown
def convert_to_markdown(wiki_input, wiki_output):
  call(["pandoc", "-f", "textile", "-t", "markdown_github", "-o", wiki_output, wiki_input])

# Crear el archivo ignore para git
def create_ignore_file(path):
  file_name = os.path.join(path, ".gitignore")
  ignore_file = open(file_name, "a")
  # ignorar la carpeta de wikis porque eso va en su propio repo
  ignore_file.write("wiki/")
  ignore_file.close()

# Iniciar el repositorio. El commit inicial sea realiza con el mensaje
# especificado
def repo_init(path, msg):
  call(["git", "-C", path, "init"])
  call(["git", "-C", path, "add", "."])
  call(["git", "-C", path, "commit", "-m", msg])


if __name__ == "__main__":
  main()



