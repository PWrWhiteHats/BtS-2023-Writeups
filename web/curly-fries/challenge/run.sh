#!/usr/bin/env bash

chmod +x /home/user/update_flag.sh

/home/user/update_flag.sh

database_file="/home/user/webapp/database.db"

if [ -f "$database_file" ]; then
    rm "$database_file"
fi

python /home/user/runserver.py
