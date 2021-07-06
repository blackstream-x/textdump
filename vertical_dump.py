#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""

vertical_dump.py

Dump the provided unicode text vertically

"""


import argparse
import logging
import sys

import textdump

#
# Constants
#

MESSAGE_FORMAT_PURE = '%(message)s'
MESSAGE_FORMAT_WITH_LEVELNAME = '%(levelname)-8s\u2551 %(message)s'

LINE_FORMAT = '{0:>8s} | {1:<8s} | {2}'

RETURNCODE_OK = 0
RETURNCODE_ERROR = 1


#
# Functions
#


def __get_arguments():
    """Parse command line arguments"""
    argument_parser = argparse.ArgumentParser(
        description='Dumps the unicode codepoint of each character'
        ' in the given text, all vertically.')
    argument_parser.set_defaults(loglevel=logging.INFO)
    argument_parser.add_argument(
        '-v', '--verbose',
        action='store_const',
        const=logging.DEBUG,
        dest='loglevel',
        help='Output all messages including debug level')
    argument_parser.add_argument(
        '-q', '--quiet',
        action='store_const',
        const=logging.WARNING,
        dest='loglevel',
        help='Limit message output to warnings and errors')
    argument_parser.add_argument(
        'text',
        nargs=argparse.REMAINDER,
        help='The text to dump. If this is omitted,'
        'the script reads text from stdin.')
    return argument_parser.parse_args()


def main(arguments):
    """Main routine, calling functions from above as required.
    Returns a returncode which is used as the script's exit code.
    """
    logging.basicConfig(format=MESSAGE_FORMAT_WITH_LEVELNAME,
                        level=arguments.loglevel)
    if arguments.text:
        source_text = ' '.join(arguments.text)
    else:
        source_text = sys.stdin.read()
    #
    dumper = textdump.TextDumper()
    print(LINE_FORMAT.format('Hex Code', 'Repr.', 'Unicode name'))
    print(LINE_FORMAT.format('-' * 8, '-' * 8, '-' * 48))
    for (representation, codepoint, unicode_name) in dumper.dump(source_text):
        if codepoint > 0xffff:
            hex_codepoint = '%08x' % codepoint
        else:
            hex_codepoint = '%04x' % codepoint
        #
        print(LINE_FORMAT.format(hex_codepoint, representation, unicode_name))
    #
    return RETURNCODE_OK


if __name__ == '__main__':
    # Call main() with the provided command line arguments
    # and exit with its returncode
    sys.exit(main(__get_arguments()))


# vim: fileencoding=utf-8 sw=4 ts=4 sts=4 expandtab autoindent syntax=python:
