import STT 
from flask import Flask, request
import base64

app = Flask(__name__)

@app.route("/",methods=["POST"])
def slash():
  js = request.get_json()
  t = js.get("speech")
  if t != None:
    u = base64.b64decode(t)
    v = STT.stt(u) 
    if v != None:
      return {"text":v},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

if __name__ == "__main__":
  app.run(host="localhost",port=5002)
