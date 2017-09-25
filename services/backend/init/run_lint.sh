#!/usr/bin/env bash

echo -e "\033[34mChecking for issues...\033[0m"
flake8 ${BACKEND_PATH}
if [ $? -eq 0 ];
then
    echo -e "\033[32mSuccess. Code has no issues\033[0m"
    exit 0
else
    echo -e "\033[31mFailed. Code has some issues\033[0m"
    exit 0
fi