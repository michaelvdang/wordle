#!/bin/sh
array=()
for i in {a..z} {A..Z}; 
   do
   array[$RANDOM]=$i
done
printf %s ${array[@]::8} $'\n'