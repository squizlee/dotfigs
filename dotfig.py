#!/usr/bin/env python3

import argparse
import os.path as path
import subprocess

def init(args):
    print("> setting up system...")
    subprocess.run(f"ln -s ~/dotfigs/zsh/.zshrc ~/.zshrc", shell=True)
    print("> done!")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()


init_parser = subparsers.add_parser("init", help="set up system")
init_parser.set_defaults(func=init)

args = parser.parse_args()
args.func(args)