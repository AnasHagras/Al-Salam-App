#!/bin/bash

# Check if running inside VSCode
if [ -n "$TERM_PROGRAM" ] && [ "$TERM_PROGRAM" == "vscode" ]; then
    # Run the script using the default shell configured in VSCode
    exec "$SHELL" "$0" "$@"
else
    # Run the script as usual
    :
fi

# Define functions
make_migrations() {
    python manage.py makemigrations
}

migrate() {
    python manage.py migrate
}

runserver() {
    python manage.py runserver
}

# Execute functions
if [ $# -eq 1 ]; then
    if declare -f "$1" > /dev/null; then
        "$1"
    else
        echo "Function '$1' does not exist."
        exit 1
    fi
elif [ $# -gt 1 ]; then
    echo "Only one function name should be provided."
    exit 1
else
    for func in make_migrations migrate; do
        $func
    done
fi
