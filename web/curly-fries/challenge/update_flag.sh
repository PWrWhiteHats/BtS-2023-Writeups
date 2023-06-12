#!/bin/bash

db_file="/home/user/webapp/db.py"

flag_value=$(cat /home/user/flag)

sed -i "s/flag{fake_flag_for_testing}/$flag_value/g" "$db_file"
