#!/usr/bin/env python3
"""
Simple script to run pytest with the correct PYTHONPATH.
"""

import subprocess
import sys
import os

# Set PYTHONPATH to current directory
env = os.environ.copy()
env['PYTHONPATH'] = '.'

# Run pytest with any arguments passed to this script
result = subprocess.run(['pytest'] + sys.argv[1:], env=env)
sys.exit(result.returncode)
