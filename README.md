# messager App

**Que hace messager app** :speech_balloon:

Messager apps en una API que  contiene distintos endpoints que permiten interactuar con Redis.

**Como usar messager app**

>Endpoint 1: POST /api/queue/pop
 Este endpoint que solo acepta metodos POST va a permitir ver el contenido del primer mensaje en una lista de redis, una vez el mensaje es leido este se borra de la lista.

>Endpoint 2: POST /api/queue/push
 Este endpoint que solo acepta metodos POST va a permitir agregar un mensaje a una lista de redis.

>Endpoint 3: GET /api/queue/count
 Este endpoint que solo acepta metodos GET va a permitir visualizar la cantidad de mensajes que existen en una lista de reds.
 APLICACIÓN MESSAGER
 Messager app es una aplicación web basada en flask  que  contiene distintos endpoints que permiten interactuar con los datos en memoria de Redis.

 REQUISITOS
 La aplicación se encuentra en Docker usando alpine3:12, para su correcta ejecución se debe contar con los siguientes componentes
 	Docker 19.03.13
 	Docker-compose 1.8.0

 Los siguientes elementos se encuentran definidos en requirements.txt como parte de la ejecución de la aplicación. Se mencionan en caso de querer usar la aplicación fuera de Docker.

 	Python3-dev
 	Pip3
 	Redis 3.5.3
 	Flask 1.1.2

 IMPLEMENTACIÓN
 La aplicación consta de 4 endpoints que permiten ejecutar distintas operaciones en redis, el proceso de implemenacion de la aplicación se detalla a continuación :

 1.	Importación de módulos
 Se importan los módulos para la aplicación así :
 Flask: Ejecución de la aplicación web
 Json: Manejo de datos en formato json
 Redis: Conexión e interacción con redis
 Functools : Decoradores necesarios para la autenticación
 Hashlib: Generador de hashes para comparar contraseña s

 2.	Definición de conector con redis
 Se crea un modulo adicional llamado redis_con.py, el cual permitirá realizar una conexión con contraseña hacia redis, esto para evitar que de manera no autorizada se utilice este servicio. Se define el parámetro rcon como host ya que es el nombre que se dio a este host al poner la aplicación en Docker, si se desea utilizar fuera de Docker la aplicación se debe reemplazar host por la dirección ip del host que contiene el servicio de redis.

 3.	Manejo de excepciones
 Se hace uso del manejo de excepciones de flask.


 4.	Endpoint POST /api/queue/pop
 Este endpoint que solo acepta metodos POST va a permitir ver el contenido del primer mensaje en una lista de redis, una vez el mensaje es leido este se borra de la lista. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized. Se hace uso del método lpop de redis para obtener el primer mensaje de una lista y borrarlo tras se leído.  Como resultado el mensaje es entregado en formato json.


 En caso de no poner obtener el valor se retorna un error 500, los errores se pueden presentar si el servicio de redis no esta disponible o la lista no existe.




 5.	Endpoint POST /api/queue/push
 Este endpoint que solo acepta metodos POST va a permitir agregar un  mensaje en una lista de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Como principal parámetro de entrada se espera el key “message” y como valor un string. En caso de no usar el key message se genera un error  404.

 Se hace uso del método lpush de redis para agregar el mensaje a una lista denominada main1.  Como resultado el mensaje es entregado en formato json. En caso de cualquier error se generará un error 500.


 6.	Endpoint GET /api/queue/count
 Este endpoint que solo acepta metodos GET  va a conocer la cantidad de elementos existentes en la cola de mensajes de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Se hace uso del método llen de redis para obtener la longitud de  main1.  Como resultado el mensaje es entregado en formato json. En caso de cualquier excepción  se generará un error 500.


 7.	Endpoint GET /api/queue/healthchk

 Este endpoint que solo acepta metodos GET  va a conocer la cantidad de elementos existentes en la cola de mensajes de redis. Para hacer uso de este endpoint se debe proveer una autenticacion HTTP básica, en caso de no estar autenticado se obtendrá un error 401 unauthorized.

 Se hace uso del método llen de redis para obtener la longitud de  main1.  Como resultado el mensaje es entregado en formato json. En caso de cualquier excepción  se generará un error 500.
