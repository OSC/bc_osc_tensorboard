#!/usr/bin/env bash 

bin/authrevproxy.py \
  --app-port=8080 \
  --proxy-port=80 \
  --bind-host="0.0.0.0" > proxy.log 2>&1 &

tensorboard \
  --logdir $LOG_DIR \
  --port 8080

