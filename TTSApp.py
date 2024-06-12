import TTS 
from flask import Flask, request
import base64

app = Flask(__name__)

@app.route("/",methods=["POST"])
def slash():
  js = request.get_json()
  t = js.get("text")
  if t != None:
    u = TTS.tts(t) 
    if u != None:
      v = base64.b64encode(u).decode("ascii")
      return {"speech":v},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

if __name__ == "__main__":
  app.run(host="localhost",port=5003)
