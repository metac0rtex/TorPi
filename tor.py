#!/usr/bin/env python

import os
import sys
import time
import urllib, urllib2
import re

def banner():
  print 'Tor Pi Setup\n'

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
  versions = []
  distdir = urllib2.urlopen('https://dist.torproject.org/')
  ver = re.findall('\"tor-.*\.tar\.gz\"', distdir.read())
  for i in ver:
    versions.append(str(i).strip('"'))
  latest = versions[-1]
  print '[+] Latest Tor Version: ' + latest
  url = 'https://dist.torproject.org/' + latest
  print '[+] Downloading ' + url
  urllib.urlretrieve(url, tordir + '/' + latest)
  print '  [+] Done'
  print '[+] Extracting file'
  os.popen('tar -xzf /opt/' + latest + ' -C ' + tordir)
  print '  [+] Done'


def main():
  sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
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
