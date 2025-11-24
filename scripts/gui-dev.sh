#!/usr/bin/bash
set -e
set -o xtrace
pip install -e /home/xf07id1/nsls-ii-sst/nbs-bl
pip install -e /home/xf07id1/nsls-ii-sst/sst_base
pip install -e /home/xf07id1/nsls-ii-sst/ucal
pip install -e /home/xf07id1/nsls-ii-sst/nbs-gui
$(dirname "$0")/gui-start.sh

