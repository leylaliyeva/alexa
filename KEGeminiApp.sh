#!/bin/sh
KE_EPT_Gemini=localhost:3006
TEXT="What is the melting point of silver?"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $KE_EPT_Gemini
