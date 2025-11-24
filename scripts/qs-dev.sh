#!/usr/bin/bash
set -e
set -o xtrace
pip install -e /home/xf07id1/nsls-ii-sst/nbs-bl
pip install -e /home/xf07id1/nsls-ii-sst/sst-base
pip install -e /home/xf07id1/nsls-ii-sst/ucal
$(dirname "$0")/qs-start.sh
