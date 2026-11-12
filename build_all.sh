#!/bin/sh
cd "$(dirname "$0")"
python3 build_th.py
for c in fr es de pt ru he; do [ -f langcfg/$c.py ] && [ -f /home/claude/lang/PelvisPower-for-Women_$(echo $c | tr a-z A-Z).txt ] && python3 build_lang.py $c; done
python3 build_site.py
python3 sidebar.py
