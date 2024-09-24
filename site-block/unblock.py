#!/usr/bin/python3

import sys
import os

PATTERN = "127.0.0.1    {}\n"
HOSTS = "/etc/hosts"

if __name__ == "__main__":
    if os.geteuid() != 0:
        raise AttributeError("Run this program as root")
    if len(sys.argv) != 2:
        raise AttributeError("Pass the URL of the site to unblock as the first argument")

    to_remove = PATTERN.format(sys.argv[1])
    with open(HOSTS, "r") as f:
        lines = f.readlines()
    try:
        index = lines.index(to_remove)
    except ValueError:
        raise ValueError("The site given is not in the blocked list")

    lines.pop(index)
    with open(HOSTS, "w") as f:
        f.writelines(lines)
    print("Site unblocked!!")
