from flask import Flask, abort, jsonify, request
import redis
import json
from redis_health import health # Health check de redis
from redis_con import r_con # Conexion a redis
from functools import wraps # Decorators para autenticacion
from hashlib import sha256

app = Flask(__name__)

#Decorator de autenticacion
def auth_required(f):
 @wraps(f)
 def decorator(*args, **kwargs):
  with open('users.db') as json_file: #abre base de datos de usuarios local
   data = json.load(json_file)
   auth = request.authorization # Header de autenticacion
   passw = sha256(auth.password.encode('utf-8')).hexdigest() # generacion de sha256 de password ingresado
   try:
    if auth and data[auth.username] ==  passw:  # comparacion de hashes
     return f( *args,  **kwargs)
    abort(401, description=("No autorizado"))
   except KeyError as exception:
    abort(401, description=("No autorizado")) # Excepcion para usuario no existente
   except AttributeError as exception:
    abort(500, description=("No se puede consultar"))

 return decorator

#### Manejo de excepciones
@app.errorhandler(404)
def resource_not_found(exception):
 return jsonify(error=str(exception)), 404

@app.errorhandler(500)
def resource_unavailable(exception):
 return jsonify(error=str(exception)),500

#####Endpoint pop
@app.route("/api/queue/pop", methods=["POST"]) # Solo acepta POST
@auth_required # Solicitud de autenticacion basica
def pop():
 try:
  data = r_con.lpop("main1").decode('utf-8') # # Decodificacion de respuesta de redis para lpop
  return jsonify({"message":data})
 except Exception as exception:
  abort(500, description=("No se puede obtener el valor"))

#####Endpoint push
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
#####Endpoitn count
@app.route("/api/queue/count", methods=["GET"])
@auth_required
def count():
 try:
  data=r_con.llen("main1") # Longitud de la lista
  return jsonify({"count":data})
 except Exception as exception:
  abort(404, description=exception)
#####Endpoint healthcheck
@app.route("/api/queue/healthchk", methods=["GET"])
@auth_required
def healthchk():
 try:
  return (health()) # Lllamada a healthchk
 except Exception as exception:
  abort(500, description=exception)

# Ejecucion de flask en todas las interfaces por puerto 5000
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,  debug=True)
