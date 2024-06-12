#!/bin/sh
TTS_EPT=localhost:3003
TEXT="What is the melting point of silver?"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $TTS_EPT
