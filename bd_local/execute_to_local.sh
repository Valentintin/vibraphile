#!/bin/bash

# this script execute a script.sql to the local postgres containner of the project #

if docker ps | grep -q "postgres"; then

    if [ -n "$1" ] && [ -f "$1" ] && [[ "$1" == *".sql" ]]; then
        psql -h 0.0.0.0 -p 5432 -U postgres -d postgres -f "$1"
    else
        echo "Give a script sql as first parameters"
    fi
else
    echo "The server Postgresql isn't running... nothing to do"
fi