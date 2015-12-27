#!/bin/bash 
. bin/activate
now=$(date +"%m_%d_%Y")
file="$now.dat"
if [ -z "$1" ]
  then
   ./manage.py display_models 2> $file
else
  ./manage.py display_models --app "$1" 2> $file
fi
