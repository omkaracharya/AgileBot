#!/usr/bin/env/python
import sys
import os

if sys.version_info < (3,5,0):
  sys.stderr.write("You need python 3.5 or later to run AgileBot\n")
  exit(1)

os.system("pip install slackclient request nose selenium pyral");
