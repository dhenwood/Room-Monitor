from flask import Flask
from flask import request
from flask import jsonify
import requests
import json

app = Flask(__name__)

### Obtain the session cookie needed for the Remote Monitoring image ###
def authVideo(ipAddress, username, password):
    url = "https://" + ipAddress + "/web/signin/open?"
    payload="username=" + username + "&password=" + password

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
        
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    cookie = response.headers["Set-Cookie"]    
    return cookie


### Obtain Remote Monitoring Image blob ###
def getImage(ipAddress, cookie):
    url = "https://" + ipAddress + "/web/api/snapshot/get_b64?SourceType=localInput&SourceId=1&AutoRefresh=true"

    headers = {
      'Cookie': cookie
    }

    response = requests.request("GET", url, headers=headers, verify=False)
    jsonResponse = json.loads(response.text)
    imageBlob = jsonResponse["data"]
    return imageBlob


### Send image to Google ###
def getObjectDetails(imageBlob):
    # I use Google Vision API for object detection. More details on this in the README file
    googleApiKey = "<removed>"
    url = "https://vision.googleapis.com/v1/images:annotate?key=" + googleApiKey

    data = {
    "requests": [
      {
        "image":{
          "content": imageBlob
        },
        "features":[
          {
            "maxResults": 50,
            "type": "LANDMARK_DETECTION"
          },{
            "maxResults": 50,
            "type": "FACE_DETECTION"
          },{
            "maxResults": 50,
            "type": "OBJECT_LOCALIZATION"
          },{
            "type":"LABEL_DETECTION",
            "maxResults":20
          },{
            "maxResults": 50,
            "model": "builtin/latest",
            "type": "DOCUMENT_TEXT_DETECTION"
          }
        ]
      }
    ]}

    json_object = json.dumps(data, indent = 4) 

    headers = {
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json_object)
    googleResponse = response.text
    googleJson = json.loads(googleResponse)

    chairCount = 0; tableCount = 0
    for item in googleJson['responses'][0]['localizedObjectAnnotations']:
        itemName = item['name']
        print("itemName: " + itemName)
        # Additional objects can be added here and subsequently returned
        if itemName == "Chair":
            chairCount = chairCount + 1
        elif itemName == "Table":
            tableCount = tableCount + 1

    summary = jsonify({'chairs': chairCount, 'tables': tableCount})
    return summary

@app.route("/")
def home():
    ipAddress = request.remote_addr
    username = request.args.get('username')
    password = request.args.get('password')
    cookie = authVideo(ipAddress, username, password)

    imageBlob = getImage(ipAddress, cookie)

    googleResponse = getObjectDetails(imageBlob)
    return googleResponse

    
if __name__ == "__main__":
    app.run(host='0.0.0.0')

