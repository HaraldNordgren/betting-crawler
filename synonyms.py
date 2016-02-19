#!/usr/bin/env python3

import re

class synonyms:

    def __init__(self):

        list_from   = "ŞüÉéçčňİışíáñóåäöÅÄÖłŁęøéú"
        list_to     = "SuEeccnIisianoaaoAAOlLeoeu"

        self.trans_list = str.maketrans(list_from, list_to)

        self.characters_to_remove = ["'", "."]

        self.characters_to_replace = [
                ("æ", "ae"),
                ("-", " ")]

    def sanitize_characters(self, string):

        for char in self.characters_to_remove:
            string = string.replace(char, "")

        for (old, new) in self.characters_to_replace:
            string = string.replace(old, new)

        return string.translate(self.trans_list)

    def sanitize_ixes(self, string):

        for (old, new) in self.prefixes:
            string = re.sub("^" + old, new, string, flags=re.IGNORECASE)
        
        for (old, new) in self.suffixes:
            string = re.sub(old + "$", new, string, flags=re.IGNORECASE)

        return string

    def get_synonym(self, string):

        before = string

        string = self.sanitize_characters(string)

        if string in self.synonym_list:
            string = self.synonym_list[string]

        after = self.sanitize_ixes(string)

        if before != after:
            self.log.write("%s -> %s\n" % (before, after))

        return after
