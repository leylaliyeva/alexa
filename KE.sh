#!/bin/sh
KE=0.0.0.0:5010
TEXT="What is the melting point of silver?"
echo "{\"text\":\"$TEXT\"}" > js
curl -X POST -H "Content-Type:application/json" -d @js $KE
