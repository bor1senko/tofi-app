#!/usr/bin/env bash

run_command() {
    if [ "$1" = true ]; then
        echo -e "\033[34mRunning $2 command...\033[0m"
        $2
        echo -e "\033[32mCommand $2 complete\033[0m"
    else
        echo -e "\033[33mCommand $2 skipped\033[0m"
    fi
}

${BACKEND_PATH}/init/wait_for_db.sh
run_command ${COLLECTSTATIC:-true} ${BACKEND_PATH}'/manage.py collectstatic --noinput'
run_command ${MIGRATE:-true} ${BACKEND_PATH}'/manage.py migrate --noinput'
run_command ${CRON:-true} ${BACKEND_PATH}'/init/cron.sh'
run_command ${TEST:-false} ${BACKEND_PATH}'/manage.py test'
run_command ${RUNSERVER:-true} ${BACKEND_PATH}'/manage.py runserver 0.0.0.0:8000'
run_command ${SLEEP:-false} 'sleep 1000000000'