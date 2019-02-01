#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

if [[ -z "${RQ_WORKERS}" ]]; then
  N=1
else
  N="${RQ_WORKERS}"
fi

if [[ -z "${REDIS_URL}" ]]; then
  URL="redis://"
else
  URL="${REDIS_URL}"
fi

echo "Runing $N RQ workers"

for ((i = 1 ; i <= $N ; i++ )); 
do
  nohup rq worker -u $URL > /dev/null 2>&1 &
  pids[${i}]=$!
done

for pid in ${pids[*]}; do
    wait $pid
done
