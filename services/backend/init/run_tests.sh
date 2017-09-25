#!/usr/bin/env bash

${BACKEND_PATH}/init/wait_for_db.sh
make -C ${BACKEND_PATH} test