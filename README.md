# messager App

**Que hace messager app** :speech_balloon:

Messager apps en una API que  contiene distintos endpoints que permiten interactuar con Redis.

**Como usar messager app**

 >REQUISITOS
  La aplicación se encuentra en Docker usando alpine3:12, para su correcta ejecución se debe contar con los siguientes componentes
   **Docker 19.03.13
 	 **Docker-compose 1.8.0

  Los siguientes elementos se encuentran definidos en requirements.txt como parte de la ejecución de la aplicación. Se mencionan en caso de querer usar la aplicación fuera de  } 
  Docker.

  **Python3-dev
  **Pip3
  **Redis 3.5.3
  **Flask 1.1.2

 ## IMPLEMENTACIÓN
 
 La aplicación consta de 4 endpoints que permiten ejecutar distintas operaciones en redis


> Endpoint POST /api/queue/pop
 Este endpoint que solo acepta metodos POST va a permitir ver el contenido del primer mensaje en una lista de redis, una vez el mensaje es leido este se borra de la lista. Para  hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized. Se hace uso del método lpop de redis para obtener el primer mensaje de una lista y borrarlo tras se leído.  Como resultado el mensaje es entregado en formato json.

    ```
    @app.route("/api/queue/pop", methods=["POST"]) # Solo acepta POST
    @auth_required # Solicitud de autenticacion basica
    def pop():
     try:
      data = r_con.lpop("main1").decode('utf-8') # # Decodificacion de respuesta de redis para lpop
      return jsonify({"message":data})
     except Exception as exception:
      abort(500, description=("No se puede obtener el valor"))

    ```

 > Endpoint POST /api/queue/push
 Este endpoint que solo acepta metodos POST va a permitir agregar un  mensaje en una lista de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Como principal parámetro de entrada se espera el key “message” y como valor un string. En caso de no usar el key message se genera un error  404.
 
 ```
@app.route("/api/queue/push", methods=["POST"])
@auth_required
def push():
  data = request.args.get("message")
  if not data: # Se debe ingresar message como parameto
   abort(404,description=("Parametros incorrectos."),)
  try:
   r_con.lpush("main1",data) # Adicion de mensaje a main1 en redis
   data=r_con.lindex("main1",0).decode('utf-8') # Obtencion del parametro ingresado
   return jsonify({"message":data})
  except Exception as exception:
   abort(500, description=exception)
```

> Endpoint GET /api/queue/count
 Este endpoint que solo acepta metodos GET  va a conocer la cantidad de elementos existentes en la cola de mensajes de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Se hace uso del método llen de redis para obtener la longitud de  main1.  Como resultado el mensaje es entregado en formato json. En caso de cualquier excepción  se generará un error 500.
```
@app.route("/api/queue/count", methods=["GET"])
@auth_required
def count():
 try:
  data=r_con.llen("main1") # Longitud de la lista
  return jsonify({"count":data})
 except Exception as exception:
  abort(404, description=exception)
 ``` 
> 	Endpoint GET /api/queue/healthchk

 Este endpoint que solo acepta metodos GET  va a conocer la cantidad de elementos existentes en la cola de mensajes de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Se hace uso del método llen de redis para obtener la longitud de  main1.  Como resultado el mensaje es entregado en formato json. En caso de cualquier excepción  se generará un error 500.
 ```
 @app.route("/api/queue/healthchk", methods=["GET"])
@auth_required
def healthchk():
 try:
  return (health()) # Lllamada a healthchk
 except Exception as exception:
  abort(500, description=("Redis en estado de error))
```

## Probando la aplicacion  ⚙️

Para ejecutar la aplicación se debe contar con los siguientes prerrequisitos:
	Docker 19.03.13
	Docker-compose 1.8.0

En caso de no contar con Docker seguir las instrucciones del siguiente recurso oficial
https://docs.docker.com/engine/install/
En caso de no contar con Docker compose seguir las instrucciones del siguiente recurso oficial
https://docs.docker.com/compose/install/

Se debe en primer lugar clonar el repositorio, este es un repositorio privado por lo cual debes ser invitado a este y autenticarte para poder clonarlo.

`git clone https://github.com/endanielgcp/messager.git`

Dirigirse al directorio en el cual se descargó el repositorio

`cd messager`

Ejecutar Docker compose

`Docker-compose build`

Se debe obtener un mensaje de creación exitosa
 
Posteriormente ejecutar 

`docker-compose up`
 
Si los procesos anteriores culminan exitosamente ya se puede utilizar la messager app.

Para hacer uso de los endpoints de la aplicación se debe realizar una autenticación básica http, así:

`Usuario: brand`

`Password: Ford`

 
Las siguientes son las funciones aceptadas con los parámetros de autenticación:
`POST /api/queue/pop`
   Parámetros: none
`POST /api/queue/push`
    Parámetros {message: “pusheo un mensaje”}
`GET /api/queue/count`
   Parámetros: none
`GET /api/queue/healthchk`
   Parámetros: none
