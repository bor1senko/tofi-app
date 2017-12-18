#!/usr/bin/env bash

echo -e "\033[34mRUN Celery worker .....\033[0m"
celery -A jupiter worker --detach -l info
