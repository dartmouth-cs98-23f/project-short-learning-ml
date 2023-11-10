#!/usr/bin/env bash

# Just a few scripts bc I hate redoing stuff.
# usage: ./script.sh [action] [dest (if applicable)]

# run the app


function launch() {
  cd app && {
    # conda activate senior-design
    uvicorn main:app --reload
  }
}

function export() {
  if (( $# == 0 )); then
    printf "Invalid usage\n"
    printf "Usage: ./script.sh export [dest-file]"
    exit 2
  fi

  dest_file = "$1"
  conda env export --file "$dest_file" -n senior-design --no-builds
}

function rebuild() {
  if (( $# == 0 )); then
    printf "Invalid usage\n"
    printf "Usage: ./script.sh rebuild [source-file]"
    exit 3
  fi

  source_file = "$1"
  conda env create --file "$source_file" -y
}


if (( $# == 0 )); then
  printf "Invalid usage.\n"
  printf "Please refer to usage instructions.\n"
  exit 1

fi

case "$1" in
  launch)
    launch
    run "$@"
    ;;
  
  export)
    shift
    export "$@"
    ;;
  
  rebuild)
    shift
    rebuild "$@"
    ;;
  
  *)
    echo "Unknown command: $1"
    exit 4

esac

