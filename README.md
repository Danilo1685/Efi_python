## Efi_python
Este repositorio contiene un proyecto de gestión de inventario de teléfonos y accesorios desarrollado con `Flask`, `Flask-SQLAlchemy` y `Flask-Migrate`. El sistema permite gestionar información sobre teléfonos y sus accesorios compatibles, ofreciendo una interfaz web para interactuar con la base de datos.

## Descripción del Proyecto
El proyecto consiste en una aplicación web que permite gestionar teléfonos y accesorios de manera eficiente. Las funcionalidades principales incluyen:

`Visualización de Teléfonos:` Muestra una lista de teléfonos disponibles en el inventario.
`Gestión de Stock:` Permite agregar stock a los teléfonos existentes.
`Accesorios Compatibles:` Muestra los accesorios compatibles para cada teléfono seleccionado.

## Tecnologías Utilizadas
`Python`: Lenguaje de programación principal.
`Flask`: Framework para el desarrollo de aplicaciones web.
`Flask-SQLAlchemy`: ORM para la gestión de la base de datos.
`Flask-Migrate`: Herramienta para la gestión de migraciones de la Base de datos.
`HTML/CSS:` Para la creación de la interfaz de usuario.

## INSTALACION
Clonar el Repositorio:
`git clone git@github.com:Danilo1685/Efi_python.git`

## Crear un Entorno Virtual:
`python3 -m venv env`
`source env/bin/activate`  # En Windows: env\Scripts\activate
`pip install Flask`
`pip install requests`
`pip install Flask Flask-SQLAlchemy Flask-Migrate PyMySQL`

## Instalar Dependencias:
`pip freeze>requierements.txt`

## Crear una Base de datos:
`-Con el entorno activo`
`flask db init `
`sudo /opt/lampp/lampp start `
`flask db migrate -m "Nombre de la Migracion"`
`flask db upgrade` #Para subir los cambios a la base de datos

`flask run` #Corre el proyecto
`flask run --reload` #Corre el proyecto sin tener que parar flask con cada modificacion que se hace






