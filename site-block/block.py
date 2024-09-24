#!/usr/bin/python3

import sys
import os

PATTERN = "127.0.0.1    {}\n"
HOSTS = "/etc/hosts"

if __name__ == "__main__":
    if os.geteuid() != 0:
        raise AttributeError("Run this program as root")
    if len(sys.argv) != 2:
        raise AttributeError("Pass the URL of the site to block as the first argument")

    to_add = PATTERN.format(sys.argv[1])
    with open(HOSTS, "r") as f:
        lines = f.readlines()
    if to_add in lines:
        raise ValueError("The site given is already in the blocked list")
    new_lines = lines + [to_add]

    with open(HOSTS, "w") as f:
        f.writelines(new_lines)
    print("Site blocked!!")
