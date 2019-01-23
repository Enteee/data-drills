#!/usr/bin/env python3
# vim: set fenc=utf8 ts=4 sw=4 et :

import sys
import inspect
import importlib
import random
import argparse
import os
import logging
import codecs
import multiprocessing
import itertools
import math

from master.drill import Drill
import drills

COLUMN_HEADER_START = '% '
COLUMN_SEPARATOR = '\t'
LOG_FORMAT = '%(asctime)-15s %(message)s'
DEFAULT_LOG_LEVEL = logging.WARNING
READ_CHUNKS = 100000

parser = argparse.ArgumentParser(description="Password data miner")
parser.add_argument("files", metavar="file", type=str, nargs="*", help="input data", default=[])
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('--strict', '-s', action='store_true', help="forces strict codec parsing")
parser.add_argument('--progress', '-p', action='count', default=-1, help="print progress")

class Miner():
    instance = None

    @staticmethod
    def get_instance():
        if Miner.instance == None:
            Miner.instance = Miner()
        return Miner.instance

    def __init__(self):
        self.__logger = logging.getLogger(__name__)
        self.__drill_classes = []      # All miner modules
        self.__drills = []

        self.__logger.info("Discover drills:")
        for drill_name in drills.__all__:
            module_path= "{}.{}".format(drills.__name__, str(drill_name))
            drill = importlib.import_module(module_path)
            self.__logger.info("{}".format(drill))
            for name, member in inspect.getmembers(drill):
                if ( 
                    inspect.isclass(member)                 # is a class
                    and issubclass(member, Drill)           # is a drill
                    and drill == inspect.getmodule(member)  # only if define in this module
                    and not inspect.isabstract(member)      # not abstract
                ):
                    self.__drill_classes.append(member)
                    self.__logger.info("    {}".format(member))

        self.__logger.info("Initialize drills")
        for drill_class in self.__drill_classes:
            self.__logger.info("{}".format(drill))
            drill = drill_class()
            self.__drills.append(drill)

    def print_headers(self):
        headers = []
        for drill in self.__drills:
            headers += drill.get_headers()
        print('{}{}'.format(
            COLUMN_HEADER_START,
            COLUMN_SEPARATOR.join(headers)
        ))

    def mine(self, line):
        data = []
        for drill in self.__drills:
            data += [ str(d) for d in drill.drill(line) ]
        return COLUMN_SEPARATOR.join(data)

def do_mine(line):
    return Miner.get_instance().mine(line)

def main(argv=sys.argv):
    args = parser.parse_args()
    random.seed()

    log_level = DEFAULT_LOG_LEVEL
    if args.verbose:
        if args.verbose > 0: log_level -= 10 * args.verbose
        if log_level <= 0: log_level = 1

    if args.progress >= 0 and log_level > logging.INFO: log_level = logging.INFO

    logging.basicConfig(format=LOG_FORMAT, level=log_level)
    logger = logging.getLogger(__name__)

    Miner.get_instance().print_headers()

    def process(fd, lines_count=-1):
        last_progress = 0
        lines_printed = 0
        while True:
            lines = [ l.strip() for l in itertools.islice(fd, READ_CHUNKS) if len(l.strip()) > 0 ]
            if not lines:
                break
            for data in multiprocessing.Pool().map(do_mine, lines):
                print(data)

                # print progress
                lines_printed += 1
                if lines_count > 0:
                    progress = lines_printed/lines_count * 100
                    if round(progress, args.progress) > round(last_progress, args.progress):
                        last_progress = progress
                        logger.info(
                            "{} %".format(
                                round(progress, args.progress)
                            )
                        )

    for fname in args.files:
        with codecs.open(fname, mode="r", encoding="utf-8", errors="ignore" if not args.strict else "strict" ) as fd:
            def file_len():
                if args.progress < 0:
                    return -1
                count = 0
                for i, l in enumerate(fd):
                    count += 1 if len(l.strip()) > 0  else 0
                fd.seek(0) # rewind file
                return count
            try:
                process(fd, file_len())
            except Exception as e:
                logger.error("file: {}, position: {}, error: {}".format(fname, fd.tell(), e))

    if len(args.files) == 0:
        process(sys.stdin)

if __name__ == "__main__":
  main()
