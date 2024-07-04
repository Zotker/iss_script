#!/bin/bash

username=admin
password=admin
url=http://10.4.2.171:8080

curl --cookie-jar cookies.txt -X POST "$url"/wist/api/auth/login -d "username=$username&password=$password"

for f in *.zip
do
  curl \
    -F "file=@./$f" \
    --cookie cookies.txt \
    --cookie-jar cookies.txt \
    "$url"/wist/api/widgets/import
done

rm ./cookies.txt
