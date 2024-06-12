#!/bin/sh
STT_EPT=localhost:3002
SPEECH=`base64 -i question.wav`
echo "{\"speech\":\"$SPEECH\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $STT_EPT
