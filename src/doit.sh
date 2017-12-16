#!/bin/bash

for i in $(seq 0 99); do
    ./step1.py $i 100 &
done
