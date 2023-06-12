#!/bin/bash

# Helper script to run challenge locally in docker. Not needed for kctf
# It will not run kctf container, but regular one (`--target app` for specifying multistage build before kctf)
# so image before hardening it for kctf 
CHAL_NAME=$(basename $(realpath ..))
docker buildx build . --target app -t "$CHAL_NAME" --load && docker run  -p 8080:80 --rm --name "$CHAL_NAME" -it "$CHAL_NAME"