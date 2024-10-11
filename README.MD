# API de Administración de Usuarios

## Índice

1. [Instalación](#instalación)
2. [Configuración del entorno de desarrollo](#configuración-del-entorno-de-desarrollo)
3. [Instalación de requerimientos](#instalación-de-requerimientos)
4. [Uso de la API con Postman](#uso-de-la-api-con-postman)
5. [Endpoints disponibles](#endpoints-disponibles)
6. [Pruebas](#pruebas)

## Instalación

Para instalar la API, sigue los siguientes pasos:

1. Clona el repositorio en tu máquina local utilizando el comando `git clone` o descarga el .zip.
2. Cambia al directorio del proyecto utilizando el comando `cd`.
3. Crea un entorno virtual utilizando el comando `python -m venv venv` (para Windows) o `python3 -m venv venv` (para Linux y Mac).
4. Activa el entorno virtual utilizando el comando `venv\Scripts\activate` (para Windows) o `source venv/bin/activate` (para Linux y Mac).

## Configuración del entorno de desarrollo

### Windows

1. Abre la terminal de Windows y ejecuta el comando `python -m venv venv` para crear un entorno virtual.
2. Activa el entorno virtual ejecutando el comando `venv\Scripts\activate`.
3. Instala los requerimientos ejecutando el comando `pip install -r requirements.txt`.

### Linux

1. Abre la terminal de Linux y ejecuta el comando `python3 -m venv venv` para crear un entorno virtual.
2. Activa el entorno virtual ejecutando el comando `source venv/bin/activate`.
3. Instala los requerimientos ejecutando el comando `pip install -r requirements.txt`.

### Mac

1. Abre la terminal de Mac y ejecuta el comando `python3 -m venv venv` para crear un entorno virtual.
2. Activa el entorno virtual ejecutando el comando `source venv/bin/activate`.
3. Instala los requerimientos ejecutando el comando `pip install -r requirements.txt`.

## Uso de la API con Postman

Para utilizar la API con Postman, sigue los siguientes pasos:

1. Abre Postman y crea un nuevo entorno.
2. Agrega la URL de la API (`http://localhost:8000`) como la URL base del entorno.
3. Utilizando el tipo de body de: `x-www-form-urlencoded` ingresa las credenciales de administración por defecto [Credenciales de administrador por defecto](#credenciales-de-administrador-por-defecto) y copia el token que obtengas al iniciar sesión.
4. En la autentificación de postman:
   * cambia el tipo de autenticación a Bearer Token.
   * reemplaza `<token>` con el token de acceso obtenido al iniciar sesión.

## Credenciales de administrador por defecto

La API viene con un usuario administrador por defecto, que puede ser utilizado para acceder a la API y realizar acciones administrativas. Las credenciales de este usuario son:

* `username`: `admin@example.com`
* `password`: `securepassword`

Puedes utilizar estas credenciales para iniciar sesión y obtener un token de acceso.

## Endpoints disponibles

* **GET /**: Obtiene la lista de usuarios.
* **POST /**: Crea un nuevo usuario.
* **GET /{user_id}**: Obtiene un usuario por ID.
* **PUT /{user_id}**: Actualiza un usuario.
* **DELETE /{user_id}**: Elimina un usuario.
* **POST /login**: Inicia sesión y obtiene un token de acceso.
* **POST /register**: Crea un nuevo administrador.

## Ejemplos de uso

* Obtener la lista de usuarios: `GET /`
* Crear un nuevo usuario: `POST /` con el cuerpo `{ "name": "Juan", "email": "juan@example.com", "password": "password" }`
* Iniciar sesión: `POST /login` con el cuerpo `{ "username": "admin@example.com", "password": "securepassword" }`

## Pruebas

Para corroborar el funcionamiento del sistema, puedes usar los archivos de prueba ubicados en `./test/test_admin_user.py` y `./test/test_user.py`. Para ejecutar las pruebas, asegúrate de tener `pytest` instalado en tu entorno y luego ejecuta el siguiente comando:

```bash
pytest ./test/test_admin_user.py
pytest ./test/test_user.py
