#!/bin/sh
KE_EPT_ChatGPT=localhost:3005
TEXT="What is the melting point of silver?"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $KE_EPT_ChatGPT
