#!/bin/bash

filename=$(basename -- "$1")
filename="${filename%.*}"
imp_name="${filename}.uni"
lin_name="${filename}.lssa.uni"
ext_name="${filename}.ext.uni"
alt_name="${filename}.alt.uni"
json_name="${filename}.json"
ext_json_name="${filename}.ext.json"


uni import $1 -o $imp_name --goal=speed
uni linearize $imp_name -o $lin_name
uni extend $lin_name -o $ext_name
uni augment $ext_name -o $alt_name
uni model $alt_name -o $json_name -b $2
echo "Starting presolver"
gecode-presolver -t 20000 -o $ext_json_name $json_name
