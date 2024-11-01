### # Documentación del Endpoint Login

### # 1. Autenticar usuario

###  URL:: `/login`  
###  Método: `POST`  
###  Descripción: Permite autenticar a un usuario mediante su nombre de usuario y contraseña. Si la autenticación es exitosa, se genera un token de acceso con una duración de 20 minutos, el cual se utiliza para autenticar futuras solicitudes.

 ###  Parámetros de Entrada:
   ###  Authorization (Header): Los datos de autenticación en formato `Basic`, que incluyen el nombre de usuario y la contraseña.

 ###  Ejemplo de Solicitud:

  ```http
    POST /login HTTP/1.1
    Host: tu_api.com
    Authorization: Basic base64(username:password)
  ```

 ###  Respuestas:
   ###  200 OK: Autenticación exitosa. Se devuelve un token de acceso.
   ###  Token (string): El token JWT en formato Bearer Token.

    ```json
    {
      "Token": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    }
    ```

   ###  401 Unauthorized: Credenciales incorrectas. No se pudo autenticar al usuario.

    ```json
    {
      "Mensaje": "El usuario y la contraseña al parecer no coinciden"
    }
    ```

###  Nota: Este endpoint devuelve un JWT que expira después de 20 minutos. El token también incluye una reclamación adicional (`administrador`), que indica si el usuario tiene permisos de administrador (`True` o `False`).



### # 2. Crear y listar usuarios

###  URL:: `/users`  
###  Métodos permitidos: `GET`, `POST`  
###  Requiere JWT: Sí  
###  Rol requerido: Solo un administrador puede crear usuarios.

###  GET: Retorna una lista de todos los usuarios.
   Si el usuario autenticado es administrador, se devuelve la lista completa con detalles de cada usuario.
   Si el usuario no es administrador, se devuelve una versión mínima de los datos del usuario.

###  POST: Crea un nuevo usuario.
   ###  Requiere: Que el usuario autenticado sea administrador.
   ###  Parámetros JSON:
     `username`: Nombre de usuario (string).
     `password`: Contraseña del usuario (string).
     `is_admin`: Indicador de si el usuario es administrador (`1` para administrador, `0` para usuario regular).
   ###  Respuesta Exitosa:

    ```json
    {
      "Mensaje": "Usuario creado correctamente",
      "Usuario": {
        "username": "nuevo_usuario",
        "is_admin": true
      }
    }
    ```

   ###  Errores:
     `403 Forbidden`: Solo los administradores pueden crear usuarios.
     `500 Internal Server Error`: Fallo en la creación del usuario.



### # 3. Eliminar usuario

###  URL: `/users/<int:id>/delete`  
###  Método: `DELETE`  
###  Requiere JWT: Sí  
###  Rol requerido: Administrador

 ###  Función: Elimina el usuario especificado.
 ###  Parámetros de URL:
   `id`: ID del usuario a eliminar.
 ###  Respuesta Exitosa:

  ```json
  {
    "Mensaje": "Usuario eliminado correctamente"
  }
  ```

 ###  Errores:
   `403 Forbidden`: Solo los administradores pueden eliminar usuarios.
   `404 Not Found`: Usuario no encontrado.
   `500 Internal Server Error`: Fallo en la eliminación del usuario.



### # 4. Actualizar usuario

###  URL: `/users/<int:id>/update`  
###  Método: `PUT`  
###  Requiere JWT: Sí  
###  Rol requerido: Administrador

 ###  Función: Actualiza los datos de un usuario existente.
 ###  Parámetros de URL:
   `id`: ID del usuario a actualizar.
 ###  Parámetros JSON
   `username`: Nuevo nombre de usuario (opcional).
   `password`: Nueva contraseña (opcional).
   `is_admin`: Indicador de si el usuario es administrador (opcional).

 ###  Respuesta Exitosa:

  ```json
  {
    "Mensaje": "Usuario actualizado correctamente",
    "Usuario": {
      "username": "nombre_actualizado",
      "is_admin": true
    }
  }
  ```

 ###  Errores:
   `403 Forbidden`: No tiene permiso para actualizar usuarios.
   `404 Not Found`: Usuario no encontrado.
   `500 Internal Server Error`: Fallo en la actualización del usuario.



### #  1. Listar y Crear Accesorios 

###  URL: `/api/accesorios_list`
###  Métodos: `GET`, `POST`
###  Autenticación: Requiere autenticación JWT y permisos de administrador para el método `POST`.

###  Descripción: 
Este endpoint permite listar todos los accesorios existentes con el método `GET`. Si se envía una solicitud `POST`, permite crear un nuevo accesorio, siempre y cuando el usuario autenticado tenga permisos de administrador.

###  Parámetros:

###  GET: No requiere parámetros adicionales.
###  POST:
   `nombre` (string, requerido): Nombre del accesorio a crear.

###  Respuestas:

###  GET:
   ###  200 OK: Devuelve una lista de todos los accesorios.
    ```json
    {
      "accesorios": [
        {"id": 1, "nombre": "Accesorio A"},
        {"id": 2, "nombre": "Accesorio B"}
      ]
    }
    ```
  
###  POST:
   ###  201 Created: Accesorio creado exitosamente.
    ```json
    {
      "message": "Accesorio creado exitosamente"
    }
    ```
   ###  403 Forbidden: El usuario no está autorizado para crear un accesorio.
    ```json
    {
      "Mensaje": "No está autorizado para crear accesorio"
    }
    ```
   ###  400 Bad Request: Error en la validación del formulario.
    ```json
    {
      "errors": {
        "nombre": ["Este campo es requerido"]
      }
    }
    ```


### #  2. Eliminar un Accesorio

###  URL: `/api/accesorio/<id>/eliminar`
###  Métodos: `POST`
###  Autenticación: Requiere autenticación JWT y permisos de administrador.

###  Descripción: 
Este endpoint permite eliminar un accesorio específico, siempre que el usuario autenticado sea administrador.

###  Parámetros:

 `id` (int, requerido): ID del accesorio a eliminar.

###  Respuestas:

   ###  200 OK: Accesorio eliminado exitosamente.
```json
{
    "message": "Accesorio eliminado exitosamente"
}
```
###  403 Forbidden: El usuario no tiene autorización para eliminar un accesorio.
```json
{
    "Mensaje": "No está autorizado para eliminar accesorio"
}
```

### #  3. Editar un Accesorio

###  URL: `/api/accesorio/<id>/editar`
###  Métodos: `GET`, `POST`
###  Autenticación: Requiere autenticación JWT y permisos de administrador.

###  Descripción: 
Este endpoint permite obtener los datos de un accesorio específico con el método `GET` y actualizarlos usando el método `POST`, siempre que el usuario tenga permisos de administrador.

###  Parámetros:

 `id` (int, requerido): ID del accesorio a editar.
###  POST:
   `nombre` (string, requerido): Nuevo nombre del accesorio.

###  Respuestas:

###  GET:
   ###  200 OK: Devuelve los datos actuales del accesorio.
    ```json
    {
      "accesorio": {
        "id": 1,
        "nombre": "Accesorio A"
      }
    }
    ```
  
###  POST:
   ###  200 OK: Accesorio actualizado exitosamente.
    ```json
    {
      "message": "Accesorio actualizado exitosamente",
      "accesorio": {
        "id": 1,
        "nombre": "Nuevo nombre"
      }
    }
    ```
   ###  403 Forbidden: El usuario no está autorizado para editar un accesorio.
    ```json
    {
      "Mensaje": "No está autorizado para editar accesorio"
    }
    ```
   ###  400 Bad Request : Error en la validación del formulario.
    ```json
    {
      "errors": {
        "nombre": ["Este campo es requerido"]
      }
    }
    ```


### # Obtener todos los datos###  

###  URL: `/main/data`
###  Método: `GET`
###  Autenticación: No se requiere autenticación.

###  Descripción:  
Este endpoint permite obtener información de todas las entidades principales de la base de datos, incluyendo teléfonos, accesorios, marcas y tipos. Además, calcula y proporciona el stock total de los teléfonos.

###  Respuesta:

 ###  200 OK: Devuelve un objeto JSON con los datos de las siguientes entidades:
   `telefonos`: Lista de teléfonos con sus detalles.
   `accesorios`: Lista de accesorios con sus detalles.
   `marcas`: Lista de marcas con sus detalles.
   `tipos`: Lista de tipos con sus detalles.
   `total_stock_telefonos`: Suma total del stock de todos los teléfonos.

###  Ejemplo de respuesta:
```json
{
  "telefonos": [
    {
      "id": 1,
      "nombre": "Teléfono A",
      "precio": 300,
      "stock": [
        {"id": 1, "cantidad": 10},
        {"id": 2, "cantidad": 5}
      ]
    },
    {
      "id": 2,
      "nombre": "Teléfono B",
      "precio": 450,
      "stock": [
        {"id": 3, "cantidad": 8}
      ]
    }
  ],
  "accesorios": [
    {
      "id": 1,
      "nombre": "Accesorio A"
    },
    {
      "id": 2,
      "nombre": "Accesorio B"
    }
  ],
  "marcas": [
    {
      "id": 1,
      "nombre": "Marca A"
    },
    {
      "id": 2,
      "nombre": "Marca B"
    }
  ],
  "tipos": [
    {
      "id": 1,
      "nombre": "Tipo A"
    },
    {
      "id": 2,
      "nombre": "Tipo B"
    }
  ],
  "total_stock_telefonos": 23
}
```

### # Endpoint: Editar Marca

###  URL:`/api/marca/<id>/editar`

###  Métodos: `GET`, `POST`

###  Descripción:

Este endpoint permite editar una marca existente. Requiere que el usuario esté autenticado y tenga privilegios de administrador para poder realizar la modificación. 

###  Requisitos de Autenticación:

 El acceso a este endpoint está protegido por JWT (JSON Web Token). Se requiere que el usuario esté autenticado y tenga el rol de administrador (`is_admin`).

###  Respuestas:

###  Código 200###  : Si la marca se edita correctamente, se redirige a la lista de marcas y se devuelve un JSON con los datos de la marca editada.
###  Código 403###  : Si el usuario no tiene privilegios de administrador, se devuelve un mensaje de error: `{"Mensaje": "No está autorizado para editar marca"}`.
###  Código 404###  : Si la marca con el `id` especificado no existe, se devuelve un error 404.

###  Parámetros de Entrada:

###  URL: 
   `<id>`: ID de la marca que se desea editar.

###  Formulario (POST):
   `nombre`: El nuevo nombre de la marca que se desea establecer.

###  Ejemplo de Uso:

1. ###  GET###  : Para obtener la información de la marca específica:
    ###  Request: `GET /api/marca/1/editar`
    ###  Response: 
     ```json
     {
       "marca": {
         "id": 1,
         "nombre": "Nombre de la Marca"
       }
     }
     ```

2. ###  POST###  : Para editar la marca con un nuevo nombre:
    ###  Request: 
     ```
     POST /api/marca/1/editar
     Form Data:
       nombre: "Nuevo Nombre de la Marca"
     ```
     ###  Response: Redirección a la lista de marcas.


### # URL: `/api/stock`

### ###  Método: `GET` / `POST`

### ### # Descripción
Este endpoint permite gestionar el stock de teléfonos. Los usuarios autenticados pueden obtener la lista de teléfonos y sus cantidades de stock, así como agregar stock a un teléfono específico.

### ### # Requisitos
 ###  Autenticación JWT: Este endpoint requiere que el usuario esté autenticado mediante un token JWT. Además, se verifica que el usuario tenga privilegios de administrador.

### ### # Parámetros
###  GET: No se requieren parámetros adicionales.
###  POST:
   `telefono_id`: ID del teléfono al que se desea agregar stock (requerido).
   `cantidad`: Cantidad de stock que se desea agregar (requerido).

### ### # Respuestas
###  200 OK###   (GET): Devuelve un JSON con la lista de teléfonos y su cantidad de stock.
  ```json
  [
    {
      "telefono": "Modelo del teléfono",
      "stock": cantidad
    },
    ...
  ]
  ```
  
###  302 Found###   (POST): Redirige a la misma ruta después de agregar stock exitosamente.

###  403 Forbidden: Si el usuario no tiene permisos de administrador.
  ```json
  {
    "Mensaje": "No está autorizado para acceder a esta ruta"
  }
  ```

###  400 Bad Request: Si faltan parámetros requeridos o si la cantidad no es un número entero.
  ```json
  {
    "Mensaje": "Debe proporcionar 'telefono_id' y 'cantidad'"
  }
  ```
  o
  ```json
  {
    "Mensaje": "Cantidad debe ser un número entero"
  }
  ```



### # URL: `/api/restar_stock`

### ###  Método: `POST`

### ### # Descripción
Este endpoint permite restar una cantidad de stock de un teléfono específico. Solo los usuarios autenticados con privilegios de administrador pueden utilizar esta función.

### ### # Requisitos
 ###  Autenticación JWT: Este endpoint requiere que el usuario esté autenticado mediante un token JWT. Además, se verifica que el usuario tenga privilegios de administrador.

### ### # Parámetros
 Se espera que los datos sean enviados a través de un formulario que contenga:
   `telefono`: ID del teléfono del que se desea restar stock (requerido).
   `cantidad`: Cantidad de stock a restar (requerido).

### ### # Respuestas
 ###  200 OK: Si el stock se ha restado correctamente.
  ```json
  {
    "Mensaje": "Stock restado correctamente"
  }
  ```

 ###  403 Forbidden: Si el usuario no tiene permisos de administrador.
  ```json
  {
    "Mensaje": "No está autorizado para borrar stock"
  }
  ```

 ###  400 Bad Request: Si los datos enviados son inválidos o no se han proporcionado correctamente.
  ```json
  {
    "Mensaje": "Datos inválidos"
  }
  ```



### # 1. Endpoint:  Listar y Crear Teléfonos

###  URL: `/api/telefono_list`
###  Métodos: `POST`, `GET`
###  Autenticación: Requiere JWT (usuario autenticado).
  
### ###  Descripción:
Este endpoint permite listar todos los teléfonos y crear nuevos teléfonos. Solo los administradores tienen permiso para crear teléfonos.

### ###  Respuesta:
 ###  GET: Devuelve una lista de teléfonos, marcas, tipos y accesorios disponibles.
   ###  Ejemplo de respuesta:
    ```json
    {
        "telefonos": [
            {
                "id": 1,
                "modelo": "iPhone 14",
                "anio_fabricacion": 2022,
                "precio": 999.99,
                "marca": {"id": 1, "nombre": "Apple"},
                "tipo": {"id": 1, "nombre": "Smartphone"}
            },
            ...
        ],
        "marcas": [
            {"id": 1, "nombre": "Apple"},
            ...
        ],
        "tipos": [
            {"id": 1, "nombre": "Smartphone"},
            ...
        ],
        "accesorios": [
            {"id": 1, "nombre": "Funda"},
            ...
        ]
    }
    ```
  
###  POST: Crea un nuevo teléfono si los datos del formulario son válidos. 
   ###  Ejemplo de respuesta exitosa:
    ```json
    {"message": "Teléfono creado exitosamente"}
    ```
   ###  Ejemplo de error:
    ```json
    {"error": "Error al crear el teléfono: <mensaje de error>"}
    ```



### # 2. Endpoint: Eliminar Teléfono


###  URL: `/api/telefono/<id>/eliminar`
###  Método: `POST`
###  Autenticación: Requiere JWT (usuario autenticado).

### ###  Descripción:
Este endpoint permite eliminar un teléfono por su ID. Solo los administradores pueden realizar esta acción.

### ###  Respuesta:
###  POST: Elimina el teléfono especificado por el ID.
     ###  Ejemplo de respuesta exitosa:
    ```json
    {"message": "Teléfono eliminado con éxito"}
    ```
     ###  Ejemplo de error:
    ```json
    {"Mensaje": "No está autorizado para eliminar teléfonos"}
    ```



### # 3. Endpoint: Obtener Teléfono y Accesorios

###  URL: `/telefono/<id>`
###  Método: `GET`
###  Autenticación: Requiere JWT (usuario autenticado).

### ###  Descripción:
Este endpoint devuelve los detalles de un teléfono específico y sus accesorios asociados. Solo los administradores pueden acceder a esta información.

### ###  Respuesta:
###  GET: Devuelve el teléfono y sus accesorios.
     ###  Ejemplo de respuesta:
    ```json
    {
        "telefono": {
            "id": 1,
            "modelo": "iPhone 14",
            "anio_fabricacion": 2022,
            "precio": 999.99,
            "marca": {"id": 1, "nombre": "Apple"},
            "tipo": {"id": 1, "nombre": "Smartphone"}
        },
        "accesorios": [
            {"id": 1, "nombre": "Funda"},
            ...
        ]
    }
    ```



### # 4. Endpoint: Eliminar Teléfono (Método Alternativo)  
###  URL: `/api/telefono/<int:telefono_id>`
###  Método: `DELETE`
###  Autenticación: Requiere JWT (usuario autenticado).

### ###  Descripción:
Este endpoint permite eliminar un teléfono por su ID. Similar al anterior, pero utiliza el método `DELETE`.

### ###  Respuesta:
###  DELETE: Elimina el teléfono especificado.
     ###  Ejemplo de respuesta exitosa:
    ```json
    {"message": "Teléfono eliminado con éxito"}
    ```
     ###  Ejemplo de error:
    ```json
    {"error": "<mensaje de error>"}
    ```



Claro, aquí tienes la documentación en español para los endpoints del `tipo_app_bp`:



###  URL: `/api/tipo_list`

### # Método: `GET`, `POST`

### # Autenticación: Requiere JWT

### # Descripción:
Este endpoint permite obtener una lista de tipos y, si el usuario está autenticado como administrador, también permite crear un nuevo tipo.

### # Respuestas:

###  GET: 
###  Código 200: Devuelve una lista de tipos.
   ###  Ejemplo de respuesta:
    ```json
    {
      "tipos": [
        {
          "id": 1,
          "nombre": "Tipo A"
        },
        {
          "id": 2,
          "nombre": "Tipo B"
        }
      ]
    }
    ```

###  POST: 
###  Código 201: Si el tipo se crea exitosamente.
   ###  Ejemplo de respuesta:
    ```json
    {
      "message": "Tipo creado exitosamente"
    }
    ```
   ###  Código 403: Si el usuario no está autorizado (no es administrador).
   ###  Ejemplo de respuesta:
    ```json
    {
      "Mensaje": "No está autorizado para crear tipos"
    }
    ```


###  URL: `/api/tipo/<int:id>/eliminar`

### # Método: `POST`

### # Autenticación: Requiere JWT

### # Descripción:
Este endpoint permite eliminar un tipo existente, siempre y cuando el usuario esté autenticado como administrador.

### # Respuestas:

###  Código 200: Si el tipo se elimina exitosamente.
   ###  Ejemplo de respuesta:
  ```json
  {
    "message": "Tipo eliminado exitosamente"
  }
  ```

###  Código 403: Si el usuario no está autorizado (no es administrador).
   ###  Ejemplo de respuesta:
  ```json
  {
    "Mensaje": "No está autorizado para eliminar tipos"
  }
  ```

 ###  Código 404: Si el tipo con el ID especificado no se encuentra.
   ###  Ejemplo de respuesta:
  ```json
  {
    "error": "Tipo no encontrado"
  }
  ```


### # Notas Generales:
 Todos los endpoints requieren que el usuario esté autenticado y tenga permisos de administrador para realizar acciones específicas.
 En caso de errores, se proporcionan mensajes claros que indican el problema.

