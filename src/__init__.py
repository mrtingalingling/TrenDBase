#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# 	Name    : coinbaseAPI
# 	Author  : Ting
#   Version : 1
#   Purpose : Access Coinbase Trading Platform
#
###############################################################################

import sys
import os
from pathlib import Path
import importlib
import logging

# PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
# sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# Add secret path
secrets_dir = Path(SCRIPT_DIR) / ".creds"
# sys.path.insert(0, secrets_dir)
print(secrets_dir)


# https://www.programcreek.com/python/example/1311/importlib.import_module
def import_creds(secrets_dir):
    """Import the modules in secrets_dir, if provided."""
    if not secrets_dir:
        try:
            secrets_dir = Path(SCRIPT_DIR) / ".creds"
        except Exception as e:
            print(e)
            return

    dir_path = os.path.abspath(os.path.expanduser(secrets_dir).rstrip("/"))
    module_list = os.listdir(dir_path)
    print(module_list)
    logging.info("Importing user module %s from path %s", module_list, dir_path)
    sys.path.insert(0, dir_path)
    for module_name in module_list:
        if ".py" in module_name:
            importlib.import_module(module_name)
    sys.path.pop(0)


def checkSubPath(dir_path):
    for f in os.listdir(dir_path):
        if S_ISDIR(f.st_mode):
            folders.append(f.filename)
        else:
            files.append(f.filename)
    if files:
        yield path, files
    for folder in folders:
        new_path = os.path.join(dir_path, folder)
        for x in sftp_walk(new_path):
            yield x


def main():
    pass


if __name__ == "__main__":
    import_creds(secrets_dir)
    # main()
