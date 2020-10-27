#!/usr/bin/env bash

for i in 5 10 25; do 
    for method in most_freq random; do 
	python main.fish.py $i --method $method 2>&1 | tee fish_ontology/workdir_${i}_${method}.log 
    done
done
