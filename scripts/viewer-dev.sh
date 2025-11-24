#!/usr/bin/bash
set -e
set -o xtrace
pip install -e /home/xf07id1/nsls-ii-sst/nbs-viewer
$(dirname "$0")/viewer-start.sh
