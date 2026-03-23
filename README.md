# Gestion pedidos 4
CRUD de una gestion de pedidos con clientes, productos y pedidos

## Instalación

#### Instalación del repositorio
En alguna carpeta de tu equipo en la terminal ejecutar:
```bash
git clone https://github.com/LechugaCuantica/gestion_pedidos_v4.git
```
Esto hará que se copie todo el repositorio con sus archivos, la seleccionamos y pasamos a los siguientes pasos
#### Crear el entorno virtual
en la raiz del proyecto ejecutar en la terminal
```bash
python -m venv venv
```
esto de creará una carpeta llamada 'venv'

#### Activar el entorno virtual
nuevamente en la raiz del proyecto ejecutar:
```bash
venv/Scripts/activate
```
esto hará que se active el entorno virtual y poder instalar las dependencias

#### Instalar dependencias
y por último ejecutar el siguiente script para instalar todas las dependencias del proyecto
```bash
pip install -r requirements.txt
```
Esto instala todas las dependencias necesarias para el proyecto


## Variables de entorno

Para correr el proyecto correctamente es necesario ingresar las variables de entorno correctamente en la raiz del proyecto creando un .env

`DB_HOST`

el host de la base de de datos, con mysql 'localhost' o '127.0.0.1'

`DB_PORT`

El puerto de la base de datos, con mysql normalmente 3306

`DB_NAME`

el nombre de la base de datos 'gestion_pedidos'

`DB_USER`

el usuario de la base de datos, con mysql normalmente 'root'

`DB_PASSWORD`

la contraseña de la base de datos, con mysql normalmente es vacía ''

### Ejemplo con las credenciales por defecto

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=gestion_pedidos
DB_USER=root
DB_PASSWORD=''
```



## Correr en local

Despues de verificar que se haya instalado correctamente todo, incluido las variables de entorno ejecutamos en local el proyecto
```bash
python manage.py runserver
```

Te enviará unos mensajes y correrá la app en

```
http://127.0.0.1:8000/
```
