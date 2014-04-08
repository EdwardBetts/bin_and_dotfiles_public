#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to change the target of symbolic links or replace them with hard links to a new target.
The target is renamed based on the current target using python's re.sub for pattern substitution.
TODO: Update doc
Add option to find broken symlinks
Add option to remove broken symlinks
'''

import argparse
import sys
import re
import os

def get_argument_parser():
  '''
  command-line option handling
  '''

  parser = argparse.ArgumentParser(description = 'Tool to work with links.')
  parser.add_argument('-v','--verbose', action="count", dest="verbosity", default=0, help='verbosity level')
  parser.add_argument("-n", "--no-act", action="store_true", dest="no_act", default=False, help="No Action: show what links would have been retargeted or removed.")
  parser.add_argument('--not-interactive', help='do not prompt before overwriting/removing', action="store_true", default=False)

  subparsers = parser.add_subparsers(help='Available subcommands')

  # parser for retarget_links
  parser_retarget_links = subparsers.add_parser('retarget', help='replace a symbolic link with a symbolic or hard link and a new target')

  parser_retarget_links.add_argument('--use_sub', action="store_true", default=False, help='Use re.sub(pattern, repl) instead of str.replace(pattern, repl), i.e. basically use regular expressions instead of normal text.')
  parser_retarget_links.add_argument('-s','--symbolic', action="store_true", default=False, help='create symbolic links instead of hard links')
  parser_retarget_links.add_argument('-p','--pattern', required=True, help='pattern in link target to look for')
  parser_retarget_links.add_argument('-r','--repl', required=True, help='string with which to replace the matched pattern')
  parser_retarget_links.add_argument('link_name', nargs='+', help='The links you want to retarget.')
  
  parser_retarget_links.set_defaults(func=retarget_links)

  # parser for listBrokenSymlinks
  parser_listBrokenSymlinks = subparsers.add_parser('list', help='list broken symbolic links and eventually remove them.')
  parser_listBrokenSymlinks.add_argument("-r", "--remove", action="store_true", default=False, help="Remove found broken links.")
  parser_listBrokenSymlinks.add_argument('DIR', nargs='+', help='The directories you want to search.')
  
  parser_listBrokenSymlinks.set_defaults(func=listBrokenSymlinks)
  
  return parser

def listBrokenSymlinks(arguments):
  '''
  TODO: Should return a list of broken symlinks to be processed by other stuff.
  # skip/select files based on pattern?
  # only look for dir symlinks?
  '''

  broken_symlinks = []
  dirs_with_broken_symlinks = set()

  for current_directory in arguments.DIR:
    for root, dirs, filenames in os.walk(current_directory, followlinks=True):
      for f in filenames:
        fullpath = os.path.join(root, f)
        if os.path.islink(fullpath):
          target = os.readlink(fullpath)
          if not os.path.exists(target) and not os.path.exists(os.path.join(root, target)):
            broken_symlinks.append((fullpath,target))
            dirs_with_broken_symlinks.add(root)
            print('broken symlink: {} -> {}'.format(fullpath, target))
            if arguments.remove:
              if arguments.not_interactive:
                ans = 'y'
              else:
                ans = input('Remove broken symlink: {} -> {}? (y/n): '.format(fullpath, target)).strip()
              if ans == 'y':
                if not arguments.no_act:
                  os.remove(fullpath)
                else:
                  print('Removing ' + fullpath)
          else:
            if arguments.verbosity > 1:
              print('working symlink: {} -> {}'.format(fullpath,target))
  
  if arguments.verbosity > 0:
    print('The following {} directories contain broken symlinks:'.format(len(dirs_with_broken_symlinks)))
    for i in dirs_with_broken_symlinks:
      print(i)
  
  return( (broken_symlinks, dirs_with_broken_symlinks) )

def retarget_links(arguments):
  for link_name in arguments.link_name:
    print('--> Processing ' + link_name)
    if not os.path.lexists(link_name):
      print(link_name+' does not exist.', file=sys.stderr)
      continue
    if not os.path.islink(link_name):
      print(link_name+' is not a symbolic link.', file=sys.stderr)
      continue

    old_target = os.readlink(link_name)
    if arguments.use_sub:
      new_target = re.sub(arguments.pattern, arguments.repl, old_target)
    else:
      new_target = old_target.replace(arguments.pattern, arguments.repl)
    
    if arguments.verbosity > 0:
      print('link_name = ' + link_name)
      print('old_target = ' + old_target)
      print('new_target = ' + new_target)
    if os.path.exists(new_target):
      if arguments.not_interactive:
        ans = 'y'
      else:
        ans = input('Relink {} from {} to {}? (y/n): '.format(link_name,old_target,new_target)).strip()
      if ans == 'y':
        if not arguments.no_act:
          os.remove(link_name)
          if arguments.symbolic:
            os.symlink(new_target, link_name)
          else:
            os.link(new_target, link_name)
      else:
        print('Skipping ' + link_name)
    else:
      print(new_target + ' not found. Skipping ' + link_name, file=sys.stderr)
  return
  
def main():
  parser = get_argument_parser()
  arguments = parser.parse_args()

  if arguments.verbosity > 0:
    print('---------')
    print(arguments)
    print('---------')
  
  if not len(sys.argv) > 1:
    parser.print_help()
  else:
    arguments.func(arguments)

  return(0)

if __name__ == "__main__":
  main()
