#!/bin/sh

if [ "${1#-}" != "$1" ]; then
  set -- getlatestdownloadbinary "$@"
fi

exec "$@"