#!/usr/bin/python3

import argparse
import sys
import os

PATTERN_START = "# Managed by SiteBlocker SECTION-START\n"
PATTERN_END = "# Managed by SiteBlocker SECTION-END\n"
PATTERN = "127.0.0.1    {}\n"
HOSTS = "/etc/hosts"

"""
- block -a <url>
- block -r <url>
- block -l
- block -rn <number>
"""
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='SiteBlocker',
        description='Manage your blocked websites')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--add')
    group.add_argument('-r', '--remove')
    group.add_argument('-l', dest='list', action='store_true')
    # group.add_argument('-r', '--number')
    args = parser.parse_args()
    if os.geteuid() != 0:
        raise AttributeError("Plase run this program as root")

    if not args:
        raise AttributeError("Plase provide an argument")

    with open(HOSTS, "r") as f:
        lines = f.readlines()

    if PATTERN_START and PATTERN_END in lines:
        pre = lines[:lines.index(PATTERN_START)]
        blocked = lines[lines.index(PATTERN_START)+1:lines.index(PATTERN_END)]
        post = lines[lines.index(PATTERN_END)+1:]
    else:
        pre = lines
        blocked = []
        post = []

    dirty = False

    if args.list is True:
        if not blocked:
            print("There are no blocked sites")
        for i, each in enumerate(blocked):
            print(i+1, " - ", each)

    elif args.add is not None:
        to_add = PATTERN.format(args.add)
        if to_add in blocked:
            raise ValueError("The given site is already in the blocked list")
        blocked = blocked + [to_add]
        dirty = True

    elif args.remove is not None:
        to_remove = PATTERN.format(args.remove)
        if to_remove not in blocked:
            raise ValueError("The given site is not in the blocked list")
        blocked.pop(blocked.index(to_remove))
        dirty = True

    if dirty is True:
        to_write = pre + [PATTERN_START] + blocked + [PATTERN_END] + post
        with open(HOSTS, "w") as f:
            f.writelines(to_write)
        print("Updated your blocked list")
