#!/bin/bash

i=1
sp="/-\|"
echo -n ' '

while read f1
do
   printf "\b${sp:i++%${#sp}:1}"
   f1=$( echo "$f1" | tr -d "\r")
   curl -s -X POST "0.0.0.0:9200/projet_3/_doc" -H "Content-Type: application/json" -d "{ \"csv_line\": \"$f1\" }" > /tmp/output.html
done < top250-00-19_modified.csv
