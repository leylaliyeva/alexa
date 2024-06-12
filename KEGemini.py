import google.generativeai as genai

API_KEY = 'AIzaSyDNYqhsOH7w8tBBXk-Y7yfPxOTTTqFe1Ow'
model = genai.GenerativeModel('gemini-pro')

# Endpoint for generating text
ENDPOINT = "https://language.googleapis.com/v1beta1/projects/-/locations/global/models/gemini-pro:generateText"
genai.configure(api_key=API_KEY)

def ke(prompt):
    response = model.generate_content(prompt)
    
    if response.text:
        return response.text
    else:
        return "Sorry, but I think Gemini didn't want to answer that!"

if __name__ == "__main__":
  t = "What is the melting point of silver?"
  u = ke(t)
  if u != None: print(u)

