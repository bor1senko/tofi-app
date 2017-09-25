#!/usr/bin/env bash

echo -e "\033[34mWaiting for db connection...\033[0m"
for i in {0..50}
do
    nc -z ${DB_HOST:-db} ${DB_PORT:-6000} >/dev/null 2>&1
    if [ "$?" -eq 0 ]
    then
        echo -e "\033[32mConnected to db is succeeded\033[0m"
        exit 0
    fi
    sleep 1
done
echo -e "\033[31mConnection to db is failed\033[0m"
exit 1