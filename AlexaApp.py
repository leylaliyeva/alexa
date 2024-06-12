import Alexa 
from flask import Flask, request

app = Flask(__name__)

@app.route("/",methods=["POST"])
def slash():
  t = request.get_json()
  u = Alexa.alexa(t) 
  if u != None:
    return u,200 # OK
  else:
    return "",500 # Internal Server Error

if __name__ == "__main__":
  app.run(host="localhost",port=5000)
