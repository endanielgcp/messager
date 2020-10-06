import json
from redis_con import r_con
def health():
 stat=r_con.ping()
 if stat:  #verificar estado redis
  info=r_con.info() # Obtencion de parametros de salud redis
  info=json.dumps({"stat":stat,"version":info['redis_version'],"conectados":info['connected_clients'],"cpu":info['used_cpu_sys'],"memoria":info['used_memory_peak']})
  return (info)
