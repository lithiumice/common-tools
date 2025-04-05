rsync -av --exclude="*.pyc" \
"Astribot:/home/lianghualin/code/RLM/src/audio_streamer" \
"./remote/RLM/"


rsync -av -e "ssh -v" --exclude="*.pyc" \
"Astribot:/home/lianghualin/code/RLM/src/audio_streamer" \
"./remote/RLM/"


scp -r Astribot:/home/lianghualin/code/RLM/src/audio_streamer ./remote/RLM/