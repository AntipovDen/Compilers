#!/usr/bin/env bash
python main.py $1 $2
python2 Krakatau/assemble.py -out out/ -r -q out/
