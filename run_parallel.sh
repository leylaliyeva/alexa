#!/bin/bash

for i in {1..200}; do
  ./KEApp.sh &
#   ./STTApp.sh &
#   ./TTSApp.sh & 
#   ./AlexaApp.sh &
done

wait
