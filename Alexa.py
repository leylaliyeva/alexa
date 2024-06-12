import requests

KE_EPT  = "http://localhost:3001"
STT_EPT = "http://localhost:3002"
TTS_EPT = "http://localhost:3003"

def alexa(x):
  return apply(TTS_EPT,apply(KE_EPT,apply(STT_EPT,x)))

def apply(f,x):
  if x != None:
    hdrs = {"Content-Type":"application/json"}
    rsp = requests.post(f,headers=hdrs,json=x)
    if rsp.status_code == 200:
      return rsp.json() 
    else:
      return None
  else:
    return None 
