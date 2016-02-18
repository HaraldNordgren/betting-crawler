#!/usr/bin/env python3

import re

class synonyms:

    def __init__(self):

        list_from   = "ŞüÉéç"
        list_to     = "SuEec"

        self.trans_list = str.maketrans(list_from, list_to)

        self.characters_to_remove = ["'"]

        self.prefixes = {
                'AA '       : '',
                'AFC '      : '',
                'BK '       : '',
                'Borussia ' : '',
                'FC '       : '',
                'GIF '      : '',
                'IF '       : '',
                'IFK '      : '',
                'IK '       : '',
                'S.C. '     : '',
                'VfL '      : ''}

        self.suffixes = {
                ' A.S.'     : '',
                ' BoIS'     : '',
                ' BK'       : '',
                ' IF'       : '',
                ' IS'       : '',
                ' FF'       : '',
                ' FK'       : '',
                ' FC'       : '',
                ' SK'       : '',
                ' United'   : ' U'}

    def sanitize_characters(self, string):

        for char in self.characters_to_remove:
            string = string.replace(char, "")

        return string.translate(self.trans_list)

    def sanitize_ixes(self, string):

        for prefix in self.prefixes:
            string = re.sub("^" + prefix, self.prefixes[prefix], string)
        
        for suffix in self.suffixes:
            string = re.sub(suffix + "$", self.suffixes[suffix], string)

        return string

    def get_synonym(self, string):

        string = self.sanitize_characters(string)
        string = self.sanitize_ixes(string)

        if string not in self.synonym_list:
            return string
        
        return self.synonym_list[string]
