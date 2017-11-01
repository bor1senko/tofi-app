#!/usr/bin/env bash

echo -e "Copying env variables for PAM..."
env | while read -r LINE; do
    IFS="=" read VAR VAL <<< ${LINE}
    sed --in-place "/^${VAR}/d" /etc/security/pam_env.conf || true
    echo "${VAR} DEFAULT=\"${VAL}\"" >> /etc/security/pam_env.conf
done

echo -e "Running cron service..."
touch /var/log/cron.log
crontab ${BACKEND_PATH}/schedule.cron
cron