#!/usr/bin/env python

import os
import sys
from threading import Thread
import time
import urllib, urllib2
import re

class WorkerThread(Thread):
    def __init__(self, cmd):
        super(WorkerThread, self).__init__()

        self.cmd = cmd

    def run(self):
      os.popen(self.cmd)

class ProgressThread(Thread):
    def __init__(self, worker):
        super(ProgressThread, self).__init__()
        self.worker = worker

    def run(self):
        while True:
            if not self.worker.is_alive():
                return True
            print '.',
            time.sleep(1.0)

def banner():
  print 'Tor Pi Setup\n\n'

def sysupdate():
  print '[+] Updating apt repos'
  os.popen('apt-get update')
  print '  [+] Done'
  print '[+] Upgrading system'
  os.popen('apt-get -y upgrade')
  print '  [+] Done'
  print '[+] Installing Prereqs'
  os.popen('apt-get -y install libevent-dev')

def downloadtor(tordir):
  print '[+] Downloading and Installing Tor'
  versions = []
  distdir = urllib2.urlopen('https://dist.torproject.org/')
  ver = re.findall('\"tor-.*\.tar\.gz\"', distdir.read())
  for i in ver:
    versions.append(str(i).strip('"'))
  latest = versions[-1]
  print '  [+] Latest Tor Version: ' + latest
  url = 'https://dist.torproject.org/' + latest
  print '  [+] Downloading ' + url
  urllib.urlretrieve(url, tordir + '/' + latest)
  print '    [+] Done'
  print '  [+] Extracting file'
  path = str(tordir + '/' + latest).strip('.tar.gz')
  os.popen('tar -xzf ' + tordir + '/' + latest + ' -C ' + tordir)
  print '    [+] Done'
  print '  [+] Configuring Tor'
  cmd = path + '/configure --prefix=/opt/tor'
  os.popen('cd ' + path + ' && ./configure --prefix=' + tordir + ' > /dev/null')
  print '    [+] Done'
  print '  [+] Compiling Tor'
  os.popen('cd ' + path + ' && make > /dev/null')
  print '    [+] Done'
  print '  [+] Installing Tor'
  os.popen('cd ' + path + ' && make install')
  print '  [+] Done'

def main():
#  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
  tordir = '/opt'
  banner()
  if not os.getuid() == 0:
    sys.exit('Need root due to apt-get usage')
#  try:
#    sysupdate()
#  except Exception as e:
#    print '[!] Error while trying to use apt-get'
#    print str(e)
  downloadtor(tordir)

main()
