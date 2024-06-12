import os
import requests

TTS_KEY = os.environ["TTS_KEY"]
TTS_REG = "uksouth"
TTS_URI = "https://" + TTS_REG + ".tts.speech.microsoft.com/" \
      "cognitiveservices/v1"

def ssml(text):
  return "<?xml version='1.0'?>" \
         "<speak version='1.0' xml:lang='en-US'>" \
         "  <voice xml:lang='en-US' name='en-US-JennyNeural'>" \
         + text + \
         "  </voice>" \
         "</speak>"

def tts(text):
  hdrs = {
    "Content-Type":"application/ssml+xml",
    "X-Microsoft-OutputFormat":"riff-16khz-16bit-mono-pcm",
    "Ocp-Apim-Subscription-Key":TTS_KEY,
  }
  rsp = requests.post(TTS_URI,headers=hdrs,data=ssml(text))
  if rsp.status_code == 200:
    return rsp.content
  else:
    return None

if __name__ == "__main__":
  t = "961.78 degrees Celsius"
  u = tts(t)
  if u != None: open("answer.wav","wb").write(u)
