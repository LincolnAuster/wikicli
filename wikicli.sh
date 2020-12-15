#!/bin/bash
# just wraps parse.py
./parse.py "$@" | par -j -w80 | less
