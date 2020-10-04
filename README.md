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
