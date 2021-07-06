# -*- coding: utf-8 -*-

"""

textdump

Return representations and codepoints of unicode string parts

"""

import unicodedata


#
# Consants
#


CARRIAGE_RETURN = '\r'
HORIZONTAL_TAB = '\t'
LINE_FEED = '\n'

CONTROLS_NAMES = {
    '\u0000': 'NULL',
    '\u0001': 'START OF HEADING',
    '\u0002': 'START OF TEXT',
    '\u0003': 'END OF TEXT',
    '\u0004': 'END OF TRANSMISSION',
    '\u0005': 'ENQUIRY',
    '\u0006': 'ACKNOWLEDGE',
    '\u0007': 'BELL',
    '\u0008': 'BACKSPACE',
    '\u0009': 'CHARACTER TABULATION',
    '\u000A': 'LINE FEED (LF)',
    '\u000B': 'LINE TABULATION= vertical tabulation (VT)',
    '\u000C': 'FORM FEED (FF)',
    '\u000D': 'CARRIAGE RETURN (CR)',
    '\u000E': 'SHIFT OUT',
    '\u000F': 'SHIFT IN',
    '\u0010': 'DATA LINK ESCAPE',
    '\u0011': 'DEVICE CONTROL ONE',
    '\u0012': 'DEVICE CONTROL TWO',
    '\u0013': 'DEVICE CONTROL THREE',
    '\u0014': 'DEVICE CONTROL FOUR',
    '\u0015': 'NEGATIVE ACKNOWLEDGE',
    '\u0016': 'SYNCHRONOUS IDLE',
    '\u0017': 'END OF TRANSMISSION BLOCK',
    '\u0018': 'CANCEL',
    '\u0019': 'END OF MEDIUM',
    '\u001A': 'SUBSTITUTE',
    '\u001B': 'ESCAPE',
    '\u001C': 'INFORMATION SEPARATOR FOUR (FS)',
    '\u001D': 'INFORMATION SEPARATOR THREE (GS)',
    '\u001E': 'INFORMATION SEPARATOR TWO (RS)',
    '\u001F': 'INFORMATION SEPARATOR ONE (US)',
    '\u007f': 'DELETE',
    '\u0082': 'BREAK PERMITTED HERE',
    '\u0083': 'NO BREAK HERE',
    '\u0084': '• formerly known as INDEX',
    '\u0085': 'NEXT LINE (NEL)',
    '\u0086': 'START OF SELECTED AREA',
    '\u0087': 'END OF SELECTED AREA',
    '\u0088': 'CHARACTER TABULATION SET',
    '\u0089': 'CHARACTER TABULATION WITHJUSTIFICATION',
    '\u008A': 'LINE TABULATION SET',
    '\u008B': 'PARTIAL LINE FORWARD',
    '\u008C': 'PARTIAL LINE BACKWARD',
    '\u008D': 'REVERSE LINE FEED',
    '\u008E': 'SINGLE SHIFT TWO',
    '\u008F': 'SINGLE SHIFT THREE',
    '\u0090': 'DEVICE CONTROL STRING',
    '\u0091': 'PRIVATE USE ONE',
    '\u0092': 'PRIVATE USE TWO',
    '\u0093': 'SET TRANSMIT STATE',
    '\u0094': 'CANCEL CHARACTER',
    '\u0095': 'MESSAGE WAITING',
    '\u0096': 'START OF GUARDED AREA',
    '\u0097': 'END OF GUARDED AREA',
    '\u0098': 'START OF STRING',
    '\u009A': 'SINGLE CHARACTER INTRODUCER',
    '\u009B': 'CONTROL SEQUENCE INTRODUCER',
    '\u009C': 'STRING TERMINATOR',
    '\u009D': 'OPERATING SYSTEM COMMAND',
    '\u009E': 'PRIVACY MESSAGE',
    '\u009F': 'APPLICATION PROGRAM COMMAND',
}

ESCAPES = {
    CARRIAGE_RETURN: r'\r',
    HORIZONTAL_TAB: r'\t',
    LINE_FEED: r'\n',
}

MARKS = 'M'
SEPARATORS = 'Z'
OTHERS = 'C'


#
# Helper classes
#


def codepoint_representation(codepoint):
    """Return the U+... representaton of the codepoint"""
    if codepoint > 0xffff:
        return 'U+%X' % codepoint
    #
    return 'U+%04X' % codepoint


#
# Classes
#


class TextDumper:

    """Class used to dump unicode text, character by character"""

    def __init__(self, escapes_map=None):
        """Allocate the escapes mapping. Default to ESCAPES."""
        if escapes_map is None:
            self.__escapes = ESCAPES
        else:
            self.__escapes = escapes_map
        #

    def representation(self, character):
        """Return the representation of a single character"""
        category = unicodedata.category(character)[0]
        #
        # Special treatment of non-visible characters
        if category in (MARKS, SEPARATORS, OTHERS):
            # Return the associated escape where defined
            try:
                return self.__escapes[character]
            except KeyError:
                pass
            #
            # Return a control picture if appropriate
            codepoint = ord(character)
            if codepoint <= 0x20:
                # C0 controls
                return chr(0x2400 + codepoint)
            #
            if codepoint == 0x7f:
                # DEL
                return chr(0x2421)
            #
            # Return the codepoint representation
            return codepoint_representation(codepoint)
        #
        return character

    def dump(self, text):
        """Yield tuples containing the character representation,
        the code point, and the unicode name if defined
        """
        for character in text:
            codepoint = ord(character)
            try:
                unicode_name = unicodedata.name(character)
            except ValueError:
                try:
                    unicode_name = CONTROLS_NAMES[character]
                except KeyError:
                    unicode_name = 'unnamed unicode character %s' % (
                        codepoint_representation(codepoint))
                #
            #
            yield (self.representation(character), codepoint, unicode_name)
        #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
