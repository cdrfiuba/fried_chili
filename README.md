# Fried Chili

![Logo](images/fried_chili.png)

## ¿De qué se trata este proyecto?

El objetivo de este proyecto es automatizar la conversión de un proyecto en formato [Chiliproject](https://www.chiliproject.org/) a un proyecto capaz de ser importado en [Github](https://github.com/). Esto involucra los siguientes pasos:

* Extraer la mayor cantidad de información posible de los wikis del chiliproject y transformarla en forma automática a wikis de Github.
* Recolectar los archivos adjuntos asociados a un proyecto e incluirlos en un repositorio de Git.
* Importar y convertir los repositorios de código Mercurial asociados al proyecto a respositorios en formato Git.

Al finalizar este proceso se tendrá un proyecto que puede ser importado a Github con mínimo esfuerzo.

## ¿Cómo haremos esto?

En primer lugar se necesita realizar un análisis extensivo de la estructura de un proyecto en Chiliproject y luego elegir las herramientas a usar para realizar la conversión:

* [Análisis de la base de datos del Chiliproject](https://github.com/cdrfiuba/fried_chili/wiki/Base-de-datos-del-Chiliproject)
* El formato de wiki usado por Chiliproject es [Textile](https://en.wikipedia.org/wiki/Textile_(markup_language)).
* El formato de wiki usado por Github es [Markdown](https://guides.github.com/features/mastering-markdown/)

### Herramientas

* Paquete para conectarse a la base de datos usando Python: [SQL Alchemy](http://www.sqlalchemy.org/)  

* Herramienta para convertir el wiki Textile a Markdown:  
http://pandoc.org/  
https://github.com/jgm/pandoc

* Herramienta para convertir repositorios de mercurial a git: [Fast-export](https://github.com/frej/fast-export)

## ¿Cómo se usa?

### Requisitos previos

Antes que nada es necesario asegurarse de tener instaladas las dependencias mencionadas arriba en la sección Herramientas:

* Instalar SQL Alquemy y el motor para mysql:  
`$ sudo apt-get install python-sqlalchemy python-mysqldb`

* Instalar Pandoc:
`$ sudo apt-get install pandoc`

Tener una copia local de las cosas del Chiliproject:

* Tener montado un servidor Mysql con la base de datos del Chiliproject importada. (ver [sobre la base de datos](https://github.com/cdrfiuba/fried_chili/wiki/Base-de-datos-del-Chiliproject)
* Una copia de la carpeta `chiliproject/files`
* Una copia de los repositorios Mercurial

Bajar y descomprimir el Fried Chili: https://github.com/cdrfiuba/fried_chili/archive/master.zip

### Configuración

#### Usuario y contraseña

Para acceder a la base de datos se debe especificar las cedenciales de acceso en un archivo de texto plano llamado `mysql-credentials.txt` con sólo dos líneas. En la primer línea va el nombre de usuario y en la segunda la contraseña:
```
nombre_usuario
contraseña
```

### Origen de los archivos

Editando el archivo de script `importer.py` se especifica la ruta completa de destino para los proyectos convertidos, para obtener los archivos adjuntos al proyecto y el repositorio de Mercurial:
```
  base_dir = "/ruta_destino"
  
  src_repo_dir = "/ruta_al_repositorio_hg"
  
  doc_dir = "/ruta_a_los_documentos_"
```

### Ejecución

El script se lanza usando python:  
`$ python importer.py`

### Resultado

Tras correr el script se creará una estructura de carpetas para alojar a todos los proyectos que se encontraron en la base de datos:

```
raiz/
  \
   ---- proyecto_padre_1/
            \
             ---- private/
                     \
                      ---- ...
            \
             ---- public/
                     \
                      ---- proyecto_1/
                               \
                                ---- README.md
                               \
                                ---- wiki/
                               \
                                ---- src_hg/
                               \
                                ---- src_git/
```

* El proyecto padre se divide en proyectos privados y públicos según como estaban especificados en Chiliproject.
* Cada subproyecto tiene un archivo `REAME.md` generado con la portada del proyecto, la fecha de creación y los integrantes del mismo como referencia. NOTA: este archivo está suelto y no se incluye por defecto en ningún repositorio de Git. Se recomienda copiarlo al repositorio src_git para tener como portada en Github.
* La carpeta `wiki` contiene las wikis del proyecto convertidas a formato Markdown. Hay un archivo por cada página del wiki. También contiene todos los archivos adjuntos del proyecto. Esta carpeta es un repositorio de Git ya inicializado y listo para ser subido al [repositorio de wiki del proyecto de Github](https://help.github.com/articles/adding-and-editing-wiki-pages-locally/)
* La carpeta `src_hg` contiene una copia del repositorio de Mecurial original correspondiente a este proyecto y es sólo para referencia.
* La carpeta `src_git` contiene el repositorio de Mercurial convertido a Git y listo para ser subido a Github.

## ¿Y ahora qué?

Si todo anduvo bien sólo queda [crear un repositorio nuevo en Github](https://help.github.com/articles/creating-a-new-repository/) y subir todo el contenido generado. Las wikis se deben crear y subir aparte ya que son otro repositorio vinculado.

Nota: es probable que se deban editar y corregir los links dentro del wiki, especialmente los referidos a archivos adjuntos.

 
