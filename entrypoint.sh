#!/bin/bash
start() {
  python dns_resolver.py
}

asyncRun() {
    "$@" &
    pid="$!"
    trap "echo 'Stopping PID $pid'; kill -SIGTERM $pid" SIGINT SIGTERM

    while kill -0 $pid > /dev/null 2>&1; do
        wait
    done
    cp ${HOST_PATH}.backup ${HOST_PATH}
}

cp ${HOST_PATH} ${HOST_PATH}.backup
asyncRun start $@
