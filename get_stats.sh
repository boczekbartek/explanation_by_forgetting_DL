#!/usr/bin/env bash
RESULTS=$1
if [[ -z "$RESULTS" ]]; then echo "usage $0 results_dir" && exit 1; fi

STATS=$RESULTS.stats.tsv

last_num=$(find $RESULTS -type f -name '*exp*' | xargs basename | sed 's/\.\///g' | sort -n | tail -n1 | sed "s/exp\.omn//g")

>&2 echo "Saving stats to: $STATS" 
echo -e "Iteration\tLength\tExplanation_File" > $STATS
for i in $(seq 0 $last_num); do
	f="$RESULTS/${i}exp.omn"
	echo -e "$i\t$(cat $f | wc -l)\t$f" 
done >> $STATS
