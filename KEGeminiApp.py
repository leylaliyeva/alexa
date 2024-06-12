from flask import Flask, request
import KEGemini

app = Flask(__name__)

@app.route("/",methods=["POST"])
def slash():
  js = request.get_json()
  t = js.get("text")
  if t != None:
    u = KEGemini.ke(t)
    if u != None:
      return {"text:":u},200 # OK
    else:
      return "",500 # Internal Server Error
  else:
    return "",400 # Bad Request

if __name__ == "__main__":
  app.run(host="localhost",port=5006)
