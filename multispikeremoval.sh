#!/bin/bash
IFS=$'\n'

pid=$$
#echo $pid
mv php.txt "${pid}.txt"
#echo "${pid}.txt"
a=$pid{'.txt'}

sed -r -i '/^\s*$/d' "${pid}.txt"
while read line
do
        /usr/bin/python /xxx/cacti/spike.py $line

done < "${pid}.txt"

rm /xxx/cacti/"${pid}.txt"