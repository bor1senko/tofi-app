#!/usr/bin/env bash


echo  -e "\033[34mRunning celery beat ... \033[0m"
celery beat -A jupiter --pidfile= -l INFO --detach
