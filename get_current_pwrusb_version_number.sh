#!/bin/bash

source activate pwrusb-dev
cd /Users/hroe/Dropbox/py/pwrusb
python -c "from __about__ import __version__; print(__version__)"
