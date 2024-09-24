#!/usr/bin/env python
import sys
import os

# First, parse the commands
# only one command at first, unnamed search term


def find_by_query(query: str):
    print()
    # for tup in os.walk(os.getcwd()):
    #     dir = tup[0]
    #     folders = tup[1]
    #     files = tup[0]

    #     if query in files:
    #         file = files.find(query)
    #         print(f"Found {query} in {dir}: {file}")
    #     else:
    #         print("No file found")


def parse_commands(arg_list):
    query = arg_list[0]
    find_by_query(query)


FILE_DIR = os.path.dirname(os.path.realpath(__file__))
cmds = sys.argv
# cmds = ["test.txt"]
parse_commands(cmds)
