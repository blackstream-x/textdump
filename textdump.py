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
                unicode_name = '–'
            #
            yield (self.representation(character), codepoint, unicode_name)
        #


# vim:fileencoding=utf-8 autoindent ts=4 sw=4 sts=4 expandtab:
