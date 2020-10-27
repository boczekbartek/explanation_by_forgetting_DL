#!/usr/bin/env bash

for i in 1 5 10 25; do 
        method=random
   	# for method in most_freq random; do 
        python main.mamo.py $i --method $method 2>&1 | tee mamo_ontology/workdir_${i}_${method}.log 
   done
done
