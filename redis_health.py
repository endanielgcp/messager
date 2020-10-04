import json
from redis_con import r_con
def health():
 stat=r_con.ping()
 if stat: 
  info=r_con.info()
  info=json.dumps({"stat":stat,"version":info['redis_version'],"conectados":info['connected_clients'],"cpu":info['used_cpu_sys'],"memoria":info['used_memory_peak']})
  return (info)
  return (str(info['used_cpu_sys']))
