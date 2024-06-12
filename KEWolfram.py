import os
import requests

KE_KEY = os.environ["KE_KEY"]
KE_URI = "https://api.wolframalpha.com/v1/result"

def ke(text):
  prms = {"appid":KE_KEY,"i":text}
  rsp = requests.get(KE_URI,params=prms)
  if rsp.status_code == 200:
    return rsp.text
  else:
    return None

if __name__ == "__main__":
  t = "What is the melting point of silver?"
  u = ke(t)
  if u != None: print(u)
