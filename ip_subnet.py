#!/usr/bin/env python3
# vim: set fenc=utf8 ts=4 sw=4 et :

import sys
import argparse
import logging
import codecs
import itertools
import ipaddress

from network_mapper import network_mapper

COLUMN_HEADER_START = '% '
COLUMN_HEADERS = ['IP', 'Network']
COLUMN_SEPARATOR = '\t'
LOG_FORMAT = '%(asctime)-15s %(message)s'
DEFAULT_LOG_LEVEL = logging.WARNING
READ_CHUNKS = 100000

parser = argparse.ArgumentParser(description="Network mapper")
parser.add_argument('network_file', metavar='network_file', type=str, nargs=1, help='file defining networks')
parser.add_argument('files', metavar='file', type=str, nargs='*', help='input data', default=[])
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('--strict', '-s', action='store_true', help='forces strict codec parsing')

def main(argv=sys.argv):
    args = parser.parse_args()

    log_level = DEFAULT_LOG_LEVEL
    if args.verbose:
        if args.verbose > 0: log_level -= 10 * args.verbose
        if log_level <= 0: log_level = 1

    logging.basicConfig(
        format=LOG_FORMAT,
        level=log_level
    )
    logger = logging.getLogger(__name__)

    # load network file
    fname = args.network_file[0]
    with codecs.open(
        fname,
        mode="r",
        encoding="utf-8",
        errors="ignore" if not args.strict else "strict"
    ) as fd:
        try:
            networks = [
                ipaddress.ip_network(
                    l.strip()
                )
                for l in itertools.islice(fd, READ_CHUNKS) if len(l.strip()) > 0
            ]
        except Exception as e:
            logger.error(
                "network file: {}, position: {}, error: {}".format(
                    fname,
                    fd.tell(),
                    e
                )
            )
            sys.exit(-1)


    # print headers
    print('{}{}'.format(
        COLUMN_HEADER_START,
        COLUMN_SEPARATOR.join(COLUMN_HEADERS)
    ))

    def process(fd, lines_count=-1):
        nm = network_mapper.NetworkMapper(networks)
        while True:
            lines = [
                l.strip() 
                for l in itertools.islice(fd, READ_CHUNKS) if len(l.strip()) > 0
            ]
            if not lines:
                break
            for line in lines:
                ip = ipaddress.ip_address(line)

                print(
                    COLUMN_SEPARATOR.join([
                        str(ip),
                        str(
                            nm.map(
                                ipaddress.ip_address(line)
                            )
                        )
                    ])
                )

    for fname in args.files:
        with codecs.open(
            fname,
            mode='r',
            encoding='utf-8',
            errors='ignore' if not args.strict else 'strict'
        ) as fd:
            try:
                process(fd)
            except Exception as e:
                logger.error("file: {}, position: {}, error: {}".format(fname, fd.tell(), e))

    if len(args.files) == 0:
        process(sys.stdin)

if __name__ == "__main__":
  main()
