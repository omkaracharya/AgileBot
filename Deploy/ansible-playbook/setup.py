#!/usr/bin/env/python
import sys
import os

sys.stderr.write("############################################\n")
sys.stderr.write("You need python 3.5 or later to run AgileBot\n")
sys.stderr.write("############################################\n")
os.system('wget http://python.org/ftp/python/3.6.3/Python-3.6.3.tar.xz > /dev/null 2>&1');
os.system('tar xf Python-3.6.3.tar.xz; cd Python-3.6.3 > /dev/null 2>&1');
os.system('./configure --prefix=/usr/local --enable-shared LDFLAGS="-Wl,-rpath /usr/local/lib" > /dev/null 2>&1');
os.system('make  > /dev/null 2>&1 && make altinstall > /dev/null 2>&1');
os.system('pip3.6 install --user slackclient request nose selenium pyral networkx flask pytz > /dev/null 2>&1');a
