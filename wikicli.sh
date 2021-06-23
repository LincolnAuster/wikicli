#!/usr/bin/env bash
./parse.py "$@" | par -j -w80 | less
