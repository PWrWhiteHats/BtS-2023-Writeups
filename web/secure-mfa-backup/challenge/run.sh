#!/usr/bin/env bash

( python $(dirname "$0")/app/bot.py )&

pid=$?

python $(dirname "$0")/app/app.py || kill -9 $pid
