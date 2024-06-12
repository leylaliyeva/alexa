import os
import requests

STT_KEY = os.environ["STT_KEY"]
STT_REG = "uksouth"
STT_URI = "https://" + STT_REG + ".stt.speech.microsoft.com/" \
        "speech/recognition/conversation/cognitiveservices/v1?" \
        "language=en-US"

def stt(speech):
  hdrs = {
    "Content-Type":"audio/wav;samplerate=16000",
    "Ocp-Apim-Subscription-Key":STT_KEY,
  }
  rsp = requests.post(STT_URI,headers=hdrs,data=speech)
  if rsp.status_code == 200:
    return rsp.json()["DisplayText"]
  else:
    return None

if __name__ == "__main__":
  t = open("question.wav","rb").read()
  u = stt(t)
  if u != None: print(u)
