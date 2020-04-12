#!/usr/bin/python

""" This module implements a dynamic md5 and sha1 verification for Gnu/Archlinux ISO images.

    Author: George Poliovei
    Author Email: poliovei@gmail.com

    License:
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>. 
"""

from bs4 import BeautifulSoup as bs
import sys
import urllib2
import subprocess as sp
import os


def run():

  #Gral. check
  args = sys.argv
  if not (len(args) == 2 and '.iso' in args[1].lower() and os.path.isfile(args[1])):
      print('\nERROR, the file must be a Gnu/Archlinux ISO image.\n')
      sys.exit()

  print("\nConnecting with Gnu/ArchLinux website ... ")

  url="https://www.archlinux.org/download/"
  content = urllib2.urlopen(url).read()
  soup = bs(content, 'html.parser')

  # url logic
  print('\nSearching and downloading md5 and sha1 keys ...')
  site_signatures = []
  lis = soup.find_all('li')
  for li in lis:
    for a in li.find_all('a'):
      if a.get('title') and 'PGP' in a.get('title'):
        for l in li.parent():
          for st in l:
            if len(st) > 30:
              print('key found: %s' % st)
              site_signatures.append(st.strip())

  #local logic
  print('\nVerifying ISO image given.')
  iso_keys = []
  for iso in args[1:]:
    if '.iso' in iso.lower():
      print("\nCalculating md5 ...")
      c1 = sp.Popen("md5sum %s" % iso, shell=True, stdout=sp.PIPE).stdout.read().split()[0]
      print("\nMD5: %s" % c1)
      iso_keys.append(c1)
      print("\nCalculating sha1 ...")
      c2 = sp.Popen("sha1sum %s" % iso, shell=True, stdout=sp.PIPE).stdout.read().split()[0]
      print("\nSHA1: %s" % c2)
      iso_keys.append(c2)

  print("\nInit verification process...")

  valid_keys = 0
  for k in iso_keys:
    if k in site_signatures:
      print('\nValid key: %s' % k)
      valid_keys += 1

  print('\n****************************************')
  if valid_keys > 0:
    print("\n%s Keys successfully validated.\nThe ISO image provided IS RELIABLE!." % valid_keys)
  else:
    print("\nERROR! Validation process failed. The ISO image IS NOT RELIABLE!")
  print('\n****************************************')

if __name__ == "__main__":
  run()
