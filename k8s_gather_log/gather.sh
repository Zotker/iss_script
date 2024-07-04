#!/bin/bash

TAIL=300
DATE=$(date +%d.%m.%y)




if [ -d ./"$DATE" ]; then
	echo Directory for logs already exist
else
	echo Creating directory "$DATE" for logs
	mkdir ./"$DATE"
fi

cd ./"$DATE"

S0=$(kubectl get pod -A | sed -e 's/\s\+/,/g' | cut -d ',' -f 1,2)
S1=$(echo "$S0" | cut -d ',' -f 1)
S2=$(echo "$S0" | cut -d ',' -f 2)
ARRAY1=($S1)
ARRAY2=($S2)

COUNT=$((${#ARRAY1[@]} - 1))

echo Gathering logs from "$COUNT" pods, last "$TAIL" strings:

for ((i=1; i <= "$COUNT"; i++))
do
	echo Gathering "$i" log from NAMESPACE "${ARRAY1[$i]}", POD "${ARRAY2[$i]}"
	kubectl logs -n ${ARRAY1[$i]} --tail="$TAIL" ${ARRAY2[$i]} | grep -e WARN -e ERROR > "$i"_"${ARRAY1[$i]}"__"${ARRAY2[$i]}".log
done 2>system_errors.log

find . -size 0 -delete

echo Gathering complete

if [ -f ./system_errors.log ]; then
        echo You have some system errors in k8s. Check "system_errors.log" in ./"$DATE" directory.
fi
