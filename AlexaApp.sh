#!/bin/sh
ALEXA_EPT=localhost:3000
SPEECH=`base64 -i question.wav`
echo "{\"speech\":\"$SPEECH\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js -o ts \
     $ALEXA_EPT
cut -d '"' -f4 ts | base64 -d > answer.wav
