from flask import Flask, abort, jsonify, request
import redis
import json
from redis_health import health
from redis_con import r_con
from functools import wraps
from hashlib import sha256

app = Flask(__name__)

def auth_required(f):
 @wraps(f)
 def decorator(*args, **kwargs):
  with open('users.db') as json_file:
   data = json.load(json_file)
   auth = request.authorization
   passw = sha256(auth.password.encode('utf-8')).hexdigest()
   try:
    if auth and data[auth.username] ==  passw:
     return f( *args,  **kwargs)
    abort(401, description=("No autorizado"))
   except Exception as exception:
    abort(401, description=("No autorizado"))
 return decorator

@app.errorhandler(404)
def resource_not_found(exception):
 return jsonify(error=str(exception)), 404

@app.errorhandler(500)
def resource_unavailable(exception):
 return jsonify(error=str(exception)),500

@app.route("/api/queue/pop", methods=["POST"])
@auth_required
def pop():
 try:  
  data = r_con.lpop("main1").decode('utf-8') 
  return jsonify({"message":data})
 except Exception as exception:
  abort(500, description=("No se puede obtener el valor"))

@app.route("/api/queue/push", methods=["POST"])
@auth_required
def push():
  data = request.args.get("message")
  if not data:
   abort(404,description=("Parametros incorrectos."),)    
  try:
   r_con.lpush("main1",data)
   data=r_con.lindex("main1",0).decode('utf-8')
   return jsonify({"message":data})
  except Exception as exception:
   abort(500, description=exception)

@app.route("/api/queue/count", methods=["GET"])
@auth_required
def count():
 try:
  data=r_con.llen("main1")
  return jsonify({"count":data})
 except Exception as exception:
  abort(500, description=exception)

@app.route("/api/queue/healthchk", methods=["GET"])
@auth_required
def healthchk():
 try:
  return (health())
 except Exception as exception:
  abort(500, description=exception)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,  debug=True)
